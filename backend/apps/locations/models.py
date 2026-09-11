"""
SebaCox Geographic and Location Hierarchy Models.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Hierarchy:
Country
  ↓
Division
  ↓
District
  ↓
Upazila (Sub-district/Thana)
  ↓
Municipality (Pourashava) / City Corporation
  ↓
Union
  ↓
Ward
  ↓
Locality / Area / Para / Moholla
"""
from django.db import models
from django.conf import settings
from .constants import (
    GeographicType,
    UserLocationType,
    ServiceAreaType,
    DEFAULT_SRID,
)
from .validators import (
    validate_latitude,
    validate_longitude,
    validate_location_code,
    validate_radius,
)


class BaseGeographicEntity(models.Model):
    """
    Abstract base model for all administrative and geographic reference units.
    Guarantees consistent naming in Bengali and English, system coding,
    activation status, and audit timestamps.
    """
    id = models.BigAutoField(primary_key=True)
    name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="বাংলায় ভৌগোলিক ইউনিটের নাম (e.g. চট্টগ্রাম, কক্সবাজার সদর)"
    )
    name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Geographic unit name in English (e.g. Chattogram, Cox's Bazar Sadar)"
    )
    code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
        validators=[validate_location_code],
        help_text="Administrative code or BBS geocode"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা (Active status for filtering)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['name_en']

    def __str__(self):
        return f"{self.name_en} ({self.name_bn})"


class Country(BaseGeographicEntity):
    """
    Sovereign state / Country model.
    Enables future expansion across Bangladesh and international regions.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="ISO 3166-1 alpha-2 code (e.g. BD, IN, US)"
    )
    iso3 = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text="ISO 3166-1 alpha-3 code (e.g. BGD)"
    )
    dial_code = models.CharField(
        max_length=10,
        blank=True,
        default='+880',
        help_text="International telephone calling code (e.g. +880)"
    )
    currency_code = models.CharField(
        max_length=5,
        blank=True,
        default='BDT',
        help_text="Currency code (e.g. BDT)"
    )

    class Meta:
        verbose_name = 'দেশ (Country)'
        verbose_name_plural = 'দেশসমূহ (Countries)'
        ordering = ['name_en']


class Division(BaseGeographicEntity):
    """
    Administrative Division (e.g. Chattogram, Dhaka, Sylhet).
    Belongs to a Country.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='divisions'
    )

    class Meta:
        verbose_name = 'বিভাগ (Division)'
        verbose_name_plural = 'বিভাগসমূহ (Divisions)'
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'code'],
                name='unique_division_country_code'
            ),
            models.UniqueConstraint(
                fields=['country', 'name_en'],
                name='unique_division_country_name_en'
            ),
        ]
        ordering = ['name_en']


class District(BaseGeographicEntity):
    """
    Administrative District / Zila (e.g. Cox's Bazar, Chattogram).
    Belongs to a Division.
    """
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    class Meta:
        verbose_name = 'জেলা (District)'
        verbose_name_plural = 'জেলাসমূহ (Districts)'
        constraints = [
            models.UniqueConstraint(
                fields=['division', 'code'],
                name='unique_district_division_code'
            ),
            models.UniqueConstraint(
                fields=['division', 'name_en'],
                name='unique_district_division_name_en'
            ),
        ]
        ordering = ['name_en']


class Upazila(BaseGeographicEntity):
    """
    Sub-district / Thana / Upazila (e.g. Cox's Bazar Sadar, Ramu, Teknaf, Ukhia).
    Belongs to a District.
    """
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='upazilas'
    )

    class Meta:
        verbose_name = 'উপজেলা (Upazila)'
        verbose_name_plural = 'উপজেলাসমূহ (Upazilas)'
        constraints = [
            models.UniqueConstraint(
                fields=['district', 'code'],
                name='unique_upazila_district_code'
            ),
            models.UniqueConstraint(
                fields=['district', 'name_en'],
                name='unique_upazila_district_name_en'
            ),
        ]
        ordering = ['name_en']


class CityCorporation(BaseGeographicEntity):
    """
    City Corporation metropolitan unit (e.g. Chattogram City Corporation).
    """
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='city_corporations'
    )

    class Meta:
        verbose_name = 'সিটি কর্পোরেশন (City Corporation)'
        verbose_name_plural = 'সিটি কর্পোরেশনসমূহ (City Corporations)'
        constraints = [
            models.UniqueConstraint(
                fields=['district', 'code'],
                name='unique_city_corporation_district_code'
            ),
        ]
        ordering = ['name_en']


class Municipality(BaseGeographicEntity):
    """
    Municipality / Pourashava (e.g. Cox's Bazar Pourashava, Chakaria Pourashava).
    Belongs to a District, optionally associated with an Upazila.
    """
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='municipalities'
    )
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='municipalities'
    )

    class Meta:
        verbose_name = 'পৌরসভা (Municipality)'
        verbose_name_plural = 'পৌরসভাসমূহ (Municipalities)'
        constraints = [
            models.UniqueConstraint(
                fields=['district', 'code'],
                name='unique_municipality_district_code'
            ),
        ]
        ordering = ['name_en']


class Union(BaseGeographicEntity):
    """
    Union Parishad rural administrative unit (e.g. Jhilongja, Khurushkul, PM Khali).
    Belongs to an Upazila.
    """
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.CASCADE,
        related_name='unions'
    )

    class Meta:
        verbose_name = 'ইউনিয়ন (Union)'
        verbose_name_plural = 'ইউনিয়নসমূহ (Unions)'
        constraints = [
            models.UniqueConstraint(
                fields=['upazila', 'code'],
                name='unique_union_upazila_code'
            ),
        ]
        ordering = ['name_en']


class Ward(BaseGeographicEntity):
    """
    Ward unit inside a Municipality, City Corporation, or Union Parishad.
    """
    ward_number = models.PositiveSmallIntegerField(
        help_text="ওয়ার্ড নম্বর (Ward numerical number e.g. 1, 2, 3)"
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='wards'
    )
    city_corporation = models.ForeignKey(
        CityCorporation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='wards'
    )
    union = models.ForeignKey(
        Union,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='wards'
    )

    class Meta:
        verbose_name = 'ওয়ার্ড (Ward)'
        verbose_name_plural = 'ওয়ার্ডসমূহ (Wards)'
        ordering = ['ward_number']


class Locality(BaseGeographicEntity):
    """
    Area / Para / Moholla / Village / Landmark (e.g. Kolatoli, Sugandha Point, Laboni Beach).
    Most granular human-facing reference for service booking and discovery.
    """
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.CASCADE,
        related_name='localities'
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='localities'
    )
    union = models.ForeignKey(
        Union,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='localities'
    )
    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='localities'
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="ডাকঘর কোড (Postcode e.g. 4700)"
    )

    class Meta:
        verbose_name = 'এলাকা / পাড়া (Locality)'
        verbose_name_plural = 'এলাকাসমূহ (Localities)'
        ordering = ['name_en']


class GeoLocation(models.Model):
    """
    Geospatial coordinate point and physical address reference.
    Ready for PostgreSQL + PostGIS (SRID 4326), with Decimal fields
    ensuring standard database portability across development and production.
    """
    id = models.BigAutoField(primary_key=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude],
        help_text="GPS Latitude (-90.0 to +90.0)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude],
        help_text="GPS Longitude (-180.0 to +180.0)"
    )
    srid = models.IntegerField(
        default=DEFAULT_SRID,
        help_text="Spatial Reference System Identifier (WGS 84 = 4326)"
    )
    address_text = models.TextField(
        blank=True,
        default='',
        help_text="Optional physical street address or landmark notes"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    locality = models.ForeignKey(
        Locality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ভৌগোলিক অবস্থান (GeoLocation)'
        verbose_name_plural = 'ভৌগোলিক অবস্থানসমূহ (GeoLocations)'
        indexes = [
            models.Index(fields=['latitude', 'longitude'], name='idx_geo_lat_lng'),
        ]

    def __str__(self):
        return f"Point({self.latitude}, {self.longitude}) - {self.address_text[:30]}"


class UserLocation(models.Model):
    """
    Relates a User to a location context without bloating the User identity model.
    Crucial architectural distinction:
    - CURRENT: Device GPS sensor coordinates (transient physical position).
    - SELECTED: Active operational service area chosen by user for browsing/services.
    - PREFERRED / HOME / WORK: Saved places.
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_locations'
    )
    location_type = models.CharField(
        max_length=20,
        choices=UserLocationType.choices,
        default=UserLocationType.SELECTED,
        db_index=True
    )
    geo_location = models.ForeignKey(
        GeoLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_associations'
    )
    # Administrative hierarchy associations for fast regional scoping
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    union = models.ForeignKey(
        Union,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    locality = models.ForeignKey(
        Locality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    label = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Custom display label e.g. 'আমার বাসা' or 'অফিস'"
    )
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ব্যবহারকারীর অবস্থান (User Location)'
        verbose_name_plural = 'ব্যবহারকারীর অবস্থানসমূহ (User Locations)'
        indexes = [
            models.Index(fields=['user', 'location_type'], name='idx_user_loc_type'),
        ]

    def __str__(self):
        return f"User #{self.user_id} - {self.location_type} ({self.label or 'Unlabeled'})"


class ServiceArea(models.Model):
    """
    Reusable foundation for future service availability boundaries.
    Allows defining service coverage by administrative boundaries or radial distance,
    WITHOUT prematurely introducing Provider or business modules.
    """
    id = models.BigAutoField(primary_key=True)
    name_bn = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    area_type = models.CharField(
        max_length=20,
        choices=ServiceAreaType.choices,
        default=ServiceAreaType.ADMINISTRATIVE
    )
    # Administrative boundary references
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    union = models.ForeignKey(
        Union,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # Radial boundary reference
    center_geo_location = models.ForeignKey(
        GeoLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    radius_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[validate_radius]
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সেবা এলাকা (Service Area)'
        verbose_name_plural = 'সেবা এলাকাসমূহ (Service Areas)'

    def __str__(self):
        return f"{self.name_en} ({self.area_type})"
