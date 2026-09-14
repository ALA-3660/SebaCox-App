"""
Location services and geospatial foundation.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import math
import unicodedata
from typing import List, Dict, Any, Optional, Tuple
from django.db.models import Q
from .constants import EARTH_RADIUS_KM, UserLocationType, GeographicType
from .models import (
    Country,
    Division,
    District,
    Upazila,
    Municipality,
    CityCorporation,
    Union,
    Ward,
    Locality,
    PostalLocation,
    GeoLocation,
    UserLocation,
)


def calculate_haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = 'km'
) -> float:
    """
    Computes great-circle distance between two GPS coordinate points
    using the Haversine formula on a spherical Earth.
    """
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))

    a = (
        math.sin(delta_phi / 2.0) ** 2 +
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    distance_km = EARTH_RADIUS_KM * c

    if unit.lower() == 'm':
        return round(distance_km * 1000.0, 2)
    return round(distance_km, 3)


def get_bounding_box(
    latitude: float,
    longitude: float,
    radius_km: float
) -> Dict[str, float]:
    """
    Computes a rough rectangular latitude/longitude bounding box around a center point.
    """
    lat = float(latitude)
    lon = float(longitude)
    radius = float(radius_km)

    lat_delta = radius / 111.0
    cos_lat = math.cos(math.radians(lat))
    lon_delta = radius / (111.0 * abs(cos_lat)) if abs(cos_lat) > 1e-6 else radius / 111.0

    return {
        'min_lat': round(lat - lat_delta, 6),
        'max_lat': round(lat + lat_delta, 6),
        'min_lon': round(lon - lon_delta, 6),
        'max_lon': round(lon + lon_delta, 6),
    }


def normalize_search_text(text: str) -> str:
    """
    Normalizes search query string for robust partial matching
    in both Bangla (Unicode NFC normalization) and English (case-folded).
    """
    if not text:
        return ''
    cleaned = unicodedata.normalize('NFC', text.strip())
    return cleaned.lower()


class LocationSearchService:
    """
    Multi-level geographic search engine supporting Bangla, English, and alias queries.
    Searches across Districts, Upazilas, Municipalities, Unions, Wards, Localities, and Post Offices.
    """

    @classmethod
    def search(cls, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Executes unified search for administrative, locality, and postal units.
        Returns formatted records including type, Bengali name, English name, and hierarchy path.
        """
        normalized = normalize_search_text(query)
        if not normalized or len(normalized) < 2:
            return []

        results: List[Dict[str, Any]] = []

        # 1. Search Districts
        districts = District.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized) |
                Q(code__icontains=normalized)
            )
        ).select_related('division')[:limit]

        for d in districts:
            results.append({
                'id': d.id,
                'type': GeographicType.DISTRICT.value,
                'type_label': 'জেলা',
                'name_bn': d.name_bn,
                'name_en': d.name_en,
                'code': d.code,
                'hierarchy_path': f"{d.name_bn}, {d.division.name_bn}",
                'hierarchy_path_en': f"{d.name_en}, {d.division.name_en}",
                'parent_id': d.division_id,
            })

        # 2. Search Upazilas
        upazilas = Upazila.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized) |
                Q(code__icontains=normalized)
            )
        ).select_related('district')[:limit]

        for u in upazilas:
            results.append({
                'id': u.id,
                'type': GeographicType.UPAZILA.value,
                'type_label': 'উপজেলা',
                'name_bn': u.name_bn,
                'name_en': u.name_en,
                'code': u.code,
                'hierarchy_path': f"{u.name_bn}, {u.district.name_bn}",
                'hierarchy_path_en': f"{u.name_en}, {u.district.name_en}",
                'parent_id': u.district_id,
            })

        # 3. Search Municipalities
        municipalities = Municipality.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized)
            )
        ).select_related('district', 'upazila')[:limit]

        for m in municipalities:
            upazila_str = f", {m.upazila.name_bn}" if m.upazila else ""
            upazila_en = f", {m.upazila.name_en}" if m.upazila else ""
            results.append({
                'id': m.id,
                'type': GeographicType.MUNICIPALITY.value,
                'type_label': 'পৌরসভা',
                'name_bn': m.name_bn,
                'name_en': m.name_en,
                'code': m.code,
                'hierarchy_path': f"{m.name_bn}{upazila_str}, {m.district.name_bn}",
                'hierarchy_path_en': f"{m.name_en}{upazila_en}, {m.district.name_en}",
                'parent_id': m.district_id,
            })

        # 4. Search Unions
        unions = Union.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized)
            )
        ).select_related('upazila', 'upazila__district')[:limit]

        for un in unions:
            results.append({
                'id': un.id,
                'type': GeographicType.UNION.value,
                'type_label': 'ইউনিয়ন',
                'name_bn': un.name_bn,
                'name_en': un.name_en,
                'code': un.code,
                'hierarchy_path': f"{un.name_bn}, {un.upazila.name_bn}, {un.upazila.district.name_bn}",
                'hierarchy_path_en': f"{un.name_en}, {un.upazila.name_en}, {un.upazila.district.name_en}",
                'parent_id': un.upazila_id,
            })

        # 5. Search Localities (with Alias Matching)
        localities = Locality.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized) |
                Q(code__icontains=normalized) |
                Q(aliases__icontains=normalized)
            )
        ).select_related('upazila', 'upazila__district', 'ward', 'union', 'municipality')[:limit]

        for loc in localities:
            parent_unit = loc.municipality.name_bn if loc.municipality else (loc.union.name_bn if loc.union else "")
            parent_unit_en = loc.municipality.name_en if loc.municipality else (loc.union.name_en if loc.union else "")
            ward_str = f", ওয়ার্ড {loc.ward.ward_number}" if loc.ward else ""
            ward_en = f", Ward {loc.ward.ward_number}" if loc.ward else ""
            unit_path = f", {parent_unit}" if parent_unit else ""
            unit_path_en = f", {parent_unit_en}" if parent_unit_en else ""

            results.append({
                'id': loc.id,
                'type': GeographicType.LOCALITY.value,
                'type_label': 'এলাকা / পাড়া',
                'name_bn': loc.name_bn,
                'name_en': loc.name_en,
                'code': loc.code,
                'hierarchy_path': f"{loc.name_bn}{ward_str}{unit_path}, {loc.upazila.name_bn}",
                'hierarchy_path_en': f"{loc.name_en}{ward_en}{unit_path_en}, {loc.upazila.name_en}",
                'parent_id': loc.upazila_id,
                'postal_code': loc.postal_code,
                'aliases': loc.aliases if isinstance(loc.aliases, list) else [],
            })

        # 6. Search Post Offices / Postal Locations (with Postal Code and Alias matching)
        post_locations = PostalLocation.objects.filter(
            Q(is_active=True) & (
                Q(post_office_name_bn__icontains=normalized) |
                Q(post_office_name_en__icontains=normalized) |
                Q(post_code__icontains=normalized) |
                Q(aliases__icontains=normalized)
            )
        ).select_related('upazila', 'district')[:limit]

        for po in post_locations:
            results.append({
                'id': po.id,
                'type': GeographicType.POSTAL.value,
                'type_label': 'ডাকঘর',
                'name_bn': po.post_office_name_bn,
                'name_en': po.post_office_name_en,
                'code': po.post_code,
                'hierarchy_path': f"{po.post_office_name_bn} (পোস্ট কোড: {po.post_code}), {po.upazila.name_bn}, {po.district.name_bn}",
                'hierarchy_path_en': f"{po.post_office_name_en} (Post Code: {po.post_code}), {po.upazila.name_en}, {po.district.name_en}",
                'parent_id': po.upazila_id,
                'postal_code': po.post_code,
                'aliases': po.aliases if isinstance(po.aliases, list) else [],
            })

        return results[:limit]


class UserLocationService:
    """
    Manages user location context, enforcing strict separation between
    device GPS physical position and user-selected operational area.
    """

    @classmethod
    def set_selected_location(
        cls,
        user,
        district_id: Optional[int] = None,
        upazila_id: Optional[int] = None,
        union_id: Optional[int] = None,
        municipality_id: Optional[int] = None,
        ward_id: Optional[int] = None,
        locality_id: Optional[int] = None,
        postal_location_id: Optional[int] = None,
        detailed_address: str = '',
        label: str = '',
    ) -> UserLocation:
        """
        Sets or updates the user's active SELECTED operational location.
        Deactivates any previous SELECTED record for this user to ensure single active selection.
        """
        UserLocation.objects.filter(
            user=user,
            location_type=UserLocationType.SELECTED,
            is_active=True
        ).update(is_active=False)

        user_loc = UserLocation.objects.create(
            user=user,
            location_type=UserLocationType.SELECTED,
            district_id=district_id,
            upazila_id=upazila_id,
            union_id=union_id,
            municipality_id=municipality_id,
            ward_id=ward_id,
            locality_id=locality_id,
            postal_location_id=postal_location_id,
            detailed_address=detailed_address,
            label=label or 'নির্বাচিত অবস্থান',
            is_default=True,
            is_active=True,
        )
        return user_loc

    @classmethod
    def update_current_location(
        cls,
        user,
        latitude: float,
        longitude: float,
        address_text: str = '',
    ) -> UserLocation:
        """
        Records the user's CURRENT GPS coordinates.
        CRITICAL: This does NOT alter the user's SELECTED service area.
        """
        geo_point = GeoLocation.objects.create(
            latitude=latitude,
            longitude=longitude,
            address_text=address_text,
            is_active=True
        )

        UserLocation.objects.filter(
            user=user,
            location_type=UserLocationType.CURRENT,
            is_active=True
        ).update(is_active=False)

        user_loc = UserLocation.objects.create(
            user=user,
            location_type=UserLocationType.CURRENT,
            geo_location=geo_point,
            label='বর্তমান জিপিএস অবস্থান',
            is_active=True,
        )
        return user_loc

    @classmethod
    def get_selected_location(cls, user) -> Optional[UserLocation]:
        """Returns the user's currently active SELECTED operational location."""
        return UserLocation.objects.filter(
            user=user,
            location_type=UserLocationType.SELECTED,
            is_active=True
        ).select_related(
            'district', 'upazila', 'union', 'municipality', 'ward', 'locality', 'postal_location'
        ).first()

    @classmethod
    def get_current_location(cls, user) -> Optional[UserLocation]:
        """Returns the user's latest recorded CURRENT device location."""
        return UserLocation.objects.filter(
            user=user,
            location_type=UserLocationType.CURRENT,
            is_active=True
        ).select_related('geo_location').first()


class BangladeshLocationImportService:
    """
    Standardized, verified administrative data ingestion pipeline.
    Ensures administrative datasets (e.g. BBS geocodes or government GIS)
    can be imported idempotently and validated without creating fake or mock data.
    """

    @classmethod
    def validate_record(cls, record: Dict[str, Any], level: str) -> Tuple[bool, List[str]]:
        """Validates schema integrity for a location record."""
        errors = []
        if not record.get('name_bn'):
            errors.append(f"{level}: name_bn missing")
        if not record.get('name_en'):
            errors.append(f"{level}: name_en missing")
        if not record.get('code'):
            errors.append(f"{level}: code missing")
        return (len(errors) == 0, errors)

    @classmethod
    def import_country(cls, data: Dict[str, Any]) -> Country:
        """Imports or updates Country record."""
        country, _ = Country.objects.update_or_create(
            code=data['code'].upper(),
            defaults={
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'iso3': data.get('iso3', ''),
                'dial_code': data.get('dial_code', '+880'),
                'currency_code': data.get('currency_code', 'BDT'),
                'is_active': data.get('is_active', True),
            }
        )
        return country

    @classmethod
    def import_division(cls, country: Country, data: Dict[str, Any]) -> Division:
        """Imports or updates Division record."""
        division, _ = Division.objects.update_or_create(
            code=data['code'],
            country=country,
            defaults={
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'is_active': data.get('is_active', True),
            }
        )
        return division

    @classmethod
    def import_district(cls, division: Division, data: Dict[str, Any]) -> District:
        """Imports or updates District record."""
        district, _ = District.objects.update_or_create(
            code=data['code'],
            division=division,
            defaults={
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'is_active': data.get('is_active', True),
            }
        )
        return district

    @classmethod
    def import_upazila(cls, district: District, data: Dict[str, Any]) -> Upazila:
        """Imports or updates Upazila record."""
        upazila, _ = Upazila.objects.update_or_create(
            code=data['code'],
            district=district,
            defaults={
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'is_active': data.get('is_active', True),
            }
        )
        return upazila

    @classmethod
    def import_municipality(cls, district: District, upazila: Optional[Upazila], data: Dict[str, Any]) -> Municipality:
        """Imports or updates Municipality record."""
        municipality, _ = Municipality.objects.update_or_create(
            code=data['code'],
            district=district,
            defaults={
                'upazila': upazila,
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'is_active': data.get('is_active', True),
            }
        )
        return municipality

    @classmethod
    def import_union(cls, upazila: Upazila, data: Dict[str, Any]) -> Union:
        """Imports or updates Union record."""
        union, _ = Union.objects.update_or_create(
            code=data['code'],
            upazila=upazila,
            defaults={
                'name_bn': data['name_bn'],
                'name_en': data['name_en'],
                'is_active': data.get('is_active', True),
            }
        )
        return union

    @classmethod
    def import_ward(
        cls,
        ward_number: int,
        name_bn: str,
        name_en: str,
        code: str,
        municipality: Optional[Municipality] = None,
        union: Optional[Union] = None,
    ) -> Ward:
        """Imports or updates Ward record."""
        filter_kwargs = {'ward_number': ward_number}
        if municipality:
            filter_kwargs['municipality'] = municipality
        elif union:
            filter_kwargs['union'] = union

        ward, _ = Ward.objects.update_or_create(
            **filter_kwargs,
            defaults={
                'name_bn': name_bn,
                'name_en': name_en,
                'code': code,
                'is_active': True,
            }
        )
        return ward

    @classmethod
    def import_locality(
        cls,
        upazila: Upazila,
        name_bn: str,
        name_en: str,
        code: str,
        locality_type: str = 'LOCAL_AREA',
        municipality: Optional[Municipality] = None,
        union: Optional[Union] = None,
        ward: Optional[Ward] = None,
        postal_code: str = '',
        aliases: Optional[List[str]] = None,
        source: str = 'Cox’s Bazar Sadar Upazila Address Master v1',
        verification_status: str = 'FIELD_VERIFIED',
    ) -> Locality:
        """Imports or updates granular Locality record."""
        locality, _ = Locality.objects.update_or_create(
            code=code,
            upazila=upazila,
            defaults={
                'name_bn': name_bn,
                'name_en': name_en,
                'locality_type': locality_type,
                'municipality': municipality,
                'union': union,
                'ward': ward,
                'postal_code': postal_code,
                'aliases': aliases or [],
                'source': source,
                'verification_status': verification_status,
                'is_active': True,
            }
        )
        return locality

    @classmethod
    def import_postal_location(
        cls,
        district: District,
        upazila: Upazila,
        post_office_name_bn: str,
        post_office_name_en: str,
        post_code: str,
        code: str,
        union: Optional[Union] = None,
        municipality: Optional[Municipality] = None,
        aliases: Optional[List[str]] = None,
        source: str = 'Bangladesh Post Master / BBS',
        verification_status: str = 'OFFICIALLY_CONFIRMED',
    ) -> PostalLocation:
        """Imports or updates PostalLocation / Post Office record."""
        postal_loc, _ = PostalLocation.objects.update_or_create(
            code=code,
            district=district,
            upazila=upazila,
            defaults={
                'name_bn': post_office_name_bn,
                'name_en': post_office_name_en,
                'post_office_name_bn': post_office_name_bn,
                'post_office_name_en': post_office_name_en,
                'post_code': post_code,
                'union': union,
                'municipality': municipality,
                'aliases': aliases or [],
                'source': source,
                'verification_status': verification_status,
                'is_active': True,
            }
        )
        return postal_loc
