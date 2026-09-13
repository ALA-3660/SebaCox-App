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

    Args:
        lat1, lon1: Point 1 coordinates in decimal degrees
        lat2, lon2: Point 2 coordinates in decimal degrees
        unit: 'km' (kilometers) or 'm' (meters)

    Returns:
        Distance in requested unit (rounded to 3 decimal places)
    """
    # Convert latitude and longitude from degrees to radians
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))

    # Haversine formula
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
    Used for efficient indexed database pre-filtering prior to exact Haversine calculation.
    """
    lat = float(latitude)
    lon = float(longitude)
    radius = float(radius_km)

    # Approximate degrees delta
    # 1 deg latitude ≈ 111.0 km
    lat_delta = radius / 111.0
    # 1 deg longitude ≈ 111.0 * cos(lat) km
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
    in both Bangla (Unicode NFC) and English (case-folded).
    """
    if not text:
        return ''
    cleaned = unicodedata.normalize('NFC', text.strip())
    return cleaned.lower()


class LocationSearchService:
    """
    Multi-level geographic search engine supporting Bangla and English queries.
    Searches across Districts, Upazilas, Municipalities, Unions, Wards, and Localities.
    """

    @classmethod
    def search(cls, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Executes unified search for administrative and locality units.
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
        ).select_related('division', 'division__country')[:limit]

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
        ).select_related('district', 'district__division')[:limit]

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
        ).select_related('district')[:limit]

        for m in municipalities:
            results.append({
                'id': m.id,
                'type': GeographicType.MUNICIPALITY.value,
                'type_label': 'পৌরসভা',
                'name_bn': m.name_bn,
                'name_en': m.name_en,
                'code': m.code,
                'hierarchy_path': f"{m.name_bn}, {m.district.name_bn}",
                'hierarchy_path_en': f"{m.name_en}, {m.district.name_en}",
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

        # 5. Search Localities
        localities = Locality.objects.filter(
            Q(is_active=True) & (
                Q(name_en__icontains=normalized) |
                Q(name_bn__icontains=normalized)
            )
        ).select_related('upazila', 'upazila__district')[:limit]

        for loc in localities:
            results.append({
                'id': loc.id,
                'type': GeographicType.LOCALITY.value,
                'type_label': 'এলাকা / পাড়া',
                'name_bn': loc.name_bn,
                'name_en': loc.name_en,
                'code': loc.code,
                'hierarchy_path': f"{loc.name_bn}, {loc.upazila.name_bn}, {loc.upazila.district.name_bn}",
                'hierarchy_path_en': f"{loc.name_en}, {loc.upazila.name_en}, {loc.upazila.district.name_en}",
                'parent_id': loc.upazila_id,
                'postal_code': loc.postal_code,
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
        ).select_related('district', 'upazila', 'union', 'municipality', 'ward', 'locality').first()

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
