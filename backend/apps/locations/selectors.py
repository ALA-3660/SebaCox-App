from __future__ import annotations
"""
Location and Geographic Engine Selectors.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from typing import Optional
from django.db.models import QuerySet
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
    UserLocation,
)


def get_active_countries() -> QuerySet[Country]:
    """Returns all active sovereign countries."""
    return Country.objects.filter(is_active=True).order_by('name_en')


def get_divisions_by_country(country_id: Optional[int] = None, country_code: Optional[str] = None) -> QuerySet[Division]:
    """Returns divisions filtered by country."""
    qs = Division.objects.filter(is_active=True)
    if country_id:
        qs = qs.filter(country_id=country_id)
    elif country_code:
        qs = qs.filter(country__code__iexact=country_code)
    return qs.select_related('country').order_by('name_en')


def get_districts_by_division(division_id: Optional[int] = None, division_code: Optional[str] = None) -> QuerySet[District]:
    """Returns districts filtered by division."""
    qs = District.objects.filter(is_active=True)
    if division_id:
        qs = qs.filter(division_id=division_id)
    elif division_code:
        qs = qs.filter(division__code=division_code)
    return qs.select_related('division').order_by('name_en')


def get_upazilas_by_district(district_id: Optional[int] = None, district_code: Optional[str] = None) -> QuerySet[Upazila]:
    """Returns upazilas filtered by parent district."""
    qs = Upazila.objects.filter(is_active=True)
    if district_id:
        qs = qs.filter(district_id=district_id)
    elif district_code:
        qs = qs.filter(district__code=district_code)
    return qs.select_related('district').order_by('name_en')


def get_municipalities(district_id: Optional[int] = None, upazila_id: Optional[int] = None) -> QuerySet[Municipality]:
    """Returns municipalities filtered by district and/or upazila."""
    qs = Municipality.objects.filter(is_active=True)
    if district_id:
        qs = qs.filter(district_id=district_id)
    if upazila_id:
        qs = qs.filter(upazila_id=upazila_id)
    return qs.select_related('district', 'upazila').order_by('name_en')


def get_city_corporations(district_id: Optional[int] = None) -> QuerySet[CityCorporation]:
    """Returns city corporations filtered by district."""
    qs = CityCorporation.objects.filter(is_active=True)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs.select_related('district').order_by('name_en')


def get_unions_by_upazila(upazila_id: Optional[int] = None, upazila_code: Optional[str] = None) -> QuerySet[Union]:
    """Returns union parishads filtered by upazila."""
    qs = Union.objects.filter(is_active=True)
    if upazila_id:
        qs = qs.filter(upazila_id=upazila_id)
    elif upazila_code:
        qs = qs.filter(upazila__code=upazila_code)
    return qs.select_related('upazila').order_by('name_en')


def get_wards(
    municipality_id: Optional[int] = None,
    union_id: Optional[int] = None,
    city_corporation_id: Optional[int] = None
) -> QuerySet[Ward]:
    """Returns wards filtered by municipality, union, or city corporation."""
    qs = Ward.objects.filter(is_active=True)
    if municipality_id:
        qs = qs.filter(municipality_id=municipality_id)
    if union_id:
        qs = qs.filter(union_id=union_id)
    if city_corporation_id:
        qs = qs.filter(city_corporation_id=city_corporation_id)
    return qs.order_by('ward_number')


def get_localities(
    upazila_id: Optional[int] = None,
    ward_id: Optional[int] = None,
    union_id: Optional[int] = None,
    municipality_id: Optional[int] = None
) -> QuerySet[Locality]:
    """Returns localities/areas filtered by parent units."""
    qs = Locality.objects.filter(is_active=True)
    if upazila_id:
        qs = qs.filter(upazila_id=upazila_id)
    if ward_id:
        qs = qs.filter(ward_id=ward_id)
    if union_id:
        qs = qs.filter(union_id=union_id)
    if municipality_id:
        qs = qs.filter(municipality_id=municipality_id)
    return qs.select_related('upazila', 'ward', 'union', 'municipality').order_by('name_en')


def get_postal_locations(
    district_id: Optional[int] = None,
    upazila_id: Optional[int] = None,
    union_id: Optional[int] = None,
    municipality_id: Optional[int] = None,
    post_code: Optional[str] = None,
) -> QuerySet[PostalLocation]:
    """Returns post offices / postal directory records."""
    qs = PostalLocation.objects.filter(is_active=True)
    if district_id:
        qs = qs.filter(district_id=district_id)
    if upazila_id:
        qs = qs.filter(upazila_id=upazila_id)
    if union_id:
        qs = qs.filter(union_id=union_id)
    if municipality_id:
        qs = qs.filter(municipality_id=municipality_id)
    if post_code:
        qs = qs.filter(post_code=post_code.strip())
    return qs.select_related('district', 'upazila', 'union', 'municipality').order_by('post_code', 'post_office_name_en')


def get_user_locations_qs(user, location_type: Optional[str] = None) -> QuerySet[UserLocation]:
    """Returns authenticated user's locations."""
    qs = UserLocation.objects.filter(user=user, is_active=True)
    if location_type:
        qs = qs.filter(location_type=location_type)
    return qs.select_related(
        'geo_location', 'country', 'division', 'district',
        'upazila', 'municipality', 'union', 'ward', 'locality',
        'postal_location'
    ).order_by('-created_at')


def get_child_locations(parent_type: str, parent_id: int):
    """
    Generic cascading child retriever for any level of the geographic hierarchy.
    Supported parent_type: COUNTRY, DIVISION, DISTRICT, UPAZILA, UNION, MUNICIPALITY, CITY_CORPORATION, WARD, POSTAL
    """
    p_type = (parent_type or '').upper().strip()
    if p_type == 'COUNTRY':
        return list(Division.objects.filter(country_id=parent_id, is_active=True).order_by('name_en'))
    elif p_type == 'DIVISION':
        return list(District.objects.filter(division_id=parent_id, is_active=True).order_by('name_en'))
    elif p_type == 'DISTRICT':
        return list(Upazila.objects.filter(district_id=parent_id, is_active=True).order_by('name_en'))
    elif p_type == 'UPAZILA':
        unions = list(Union.objects.filter(upazila_id=parent_id, is_active=True).order_by('name_en'))
        municipalities = list(Municipality.objects.filter(upazila_id=parent_id, is_active=True).order_by('name_en'))
        postal_locations = list(PostalLocation.objects.filter(upazila_id=parent_id, is_active=True).order_by('post_code', 'post_office_name_en'))
        return {
            'unions': unions,
            'municipalities': municipalities,
            'postal_locations': postal_locations,
        }
    elif p_type == 'UNION':
        return list(Ward.objects.filter(union_id=parent_id, is_active=True).order_by('ward_number'))
    elif p_type == 'MUNICIPALITY':
        return list(Ward.objects.filter(municipality_id=parent_id, is_active=True).order_by('ward_number'))
    elif p_type == 'CITY_CORPORATION':
        return list(Ward.objects.filter(city_corporation_id=parent_id, is_active=True).order_by('ward_number'))
    elif p_type == 'WARD':
        return list(Locality.objects.filter(ward_id=parent_id, is_active=True).order_by('name_en'))
    elif p_type == 'POSTAL':
        return list(PostalLocation.objects.filter(upazila_id=parent_id, is_active=True).order_by('post_code'))
    return []

