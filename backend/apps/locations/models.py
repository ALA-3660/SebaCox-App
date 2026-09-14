"""
SebaCox Geographic and Location Hierarchy Models.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

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
from django.core.exceptions import ValidationError
from .constants import (
    GeographicType,
    LocalityType,
    UserLocationType,
    ServiceAreaType,
    VerificationStatus,
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

    def clean(self):
        pass

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

    def clean(self):
        super().clean()
        if not self.district_id:
            raise ValidationError({'district': 'সিটি কর্পোরেশন অবশ্যই একটি বৈধ জেলার অধীনে হতে হবে।'})


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

    def clean(self):
        super().clean()
        if not self.district_id:
            raise ValidationError({'district': 'পৌরসভা অবশ্যই একটি বৈধ জেলার অধীনে হতে হবে।'})
        if self.upazila and self.district and self.upazila.district_id != self.district_id:
            raise ValidationError({
                'upazila': f"উপজেলা '{self.upazila.name_bn}' অবশ্যই জেলা '{self.district.name_bn}'-এর অন্তর্ভুক্ত হতে হবে।"
            })


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

    def clean(self):
        super().clean()
        if not self.upazila_id:
            raise ValidationError({'upazila': 'ইউনিয়ন অবশ্যই একটি বৈধ উপজেলার অধীনে হতে হবে।'})


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

    @property
    def display_name_bn(self):
        """
        Returns purely the Ward Number formatted in Bengali (e.g. '১ নং ওয়ার্ড').
        Strictly excludes any locality, village, or landmark names.
        """
        bangla_digits = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
        num_str = ''.join(bangla_digits.get(c, c) for c in str(self.ward_number))
        return f"{num_str} নং ওয়ার্ড"

    def clean(self):
        super().clean()
        parents = [p for p in [self.municipality_id, self.city_corporation_id, self.union_id] if p is not None]
        if len(parents) == 0:
            raise ValidationError('ওয়ার্ড অবশ্যই একটি পৌরসভা, সিটি কর্পোরেশন, অথবা ইউনিয়নের অধীনে হতে হবে।')
        if len(parents) > 1:
            raise ValidationError('একটি ওয়ার্ড একাধিক প্রশাসনিক ইউনিটের (পৌরসভা/সিটি কর্পোরেশন/ইউনিয়ন) সাথে যুক্ত হতে পারে না।')


class Locality(BaseGeographicEntity):
    """
    Area / Para / Moholla / Village / Landmark (e.g. Kolatoli, Sugandha Point, Laboni Beach).
    Most granular human-facing reference for service booking and discovery.
    """
    locality_type = models.CharField(
        max_length=20,
        choices=LocalityType.choices,
        default=LocalityType.LOCAL_AREA,
        db_index=True,
        help_text="লোকালিটির প্রকার (পাড়া, মহল্লা, গ্রাম, বাজার, ইত্যাদি)"
    )
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
    aliases = models.JSONField(
        default=list,
        blank=True,
        help_text="বিকল্প নাম বা উপনামসমূহ (e.g. Kolatoli, Kalatali, কলাতলী)"
    )
    source = models.CharField(
        max_length=150,
        default='Field Survey / BBS / Local Verification',
        blank=True,
        help_text="তথ্যসূত্র বা উৎস"
    )
    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.FIELD_VERIFIED,
        db_index=True,
        help_text="যাচাইকরণের অবস্থা"
    )

    class Meta:
        verbose_name = 'এলাকা / পাড়া (Locality)'
        verbose_name_plural = 'এলাকাসমূহ (Localities)'
        ordering = ['name_en']

    def clean(self):
        super().clean()
        if not self.upazila_id:
            raise ValidationError({'upazila': 'লোকালিটি অবশ্যই একটি বৈধ উপজেলার অন্তর্ভুক্ত হতে হবে।'})

        # Validate union hierarchy
        if self.union_id and self.union.upazila_id != self.upazila_id:
            raise ValidationError({
                'union': f"ইউনিয়ন '{self.union.name_bn}' অবশ্যই নির্বাচিত উপজেলা '{self.upazila.name_bn}'-এর অন্তর্ভুক্ত হতে হবে।"
            })

        # Validate municipality hierarchy
        if self.municipality_id and self.municipality.upazila_id and self.municipality.upazila_id != self.upazila_id:
            raise ValidationError({
                'municipality': f"পৌরসভা '{self.municipality.name_bn}' অবশ্যই নির্বাচিত উপজেলা '{self.upazila.name_bn}'-এর অন্তর্ভুক্ত হতে হবে।"
            })

        # Validate ward hierarchy
        if self.ward_id:
            if self.ward.union_id:
                if self.union_id and self.ward.union_id != self.union_id:
                    raise ValidationError({
                        'ward': f"ওয়ার্ড #{self.ward.ward_number} ইউনিয়ন '{self.ward.union.name_bn}'-এর অন্তর্ভুক্ত, যা নির্বাচিত ইউনিয়ন '{self.union.name_bn}'-এর সাথে মেলে না।"
                    })
                if self.ward.union.upazila_id != self.upazila_id:
                    raise ValidationError({
                        'ward': "ওয়ার্ডের অভিভাবক ইউনিয়নটি নির্বাচিত উপজেলার অধীন নয়।"
                    })
            elif self.ward.municipality_id:
                if self.municipality_id and self.ward.municipality_id != self.municipality_id:
                    raise ValidationError({
                        'ward': f"ওয়ার্ড #{self.ward.ward_number} পৌরসভা '{self.ward.municipality.name_bn}'-এর অন্তর্ভুক্ত, যা নির্বাচিত পৌরসভার সাথে মেলে না।"
                    })


class PostalLocation(BaseGeographicEntity):
    """
    Separate Postal Directory / Post Office entity.
    Decoupled from rigid administrative parent-child to reflect actual Bangladesh Post Office delivery zones.
    Maps Post Office Name, Postal Code, and administrative associations.
    """
    post_office_name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="ডাকঘরের নাম বাংলায় (e.g. কক্সবাজার প্রধান ডাকঘর, ঝিলংঝা সাব-পোস্ট অফিস)"
    )
    post_office_name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Post office name in English (e.g. Cox's Bazar Head Post Office, Jhilongjha Sub Post Office)"
    )
    post_code = models.CharField(
        max_length=10,
        db_index=True,
        help_text="৪-সংখ্যার পোস্ট কোড (e.g. 4700, 4701, 4702)"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='postal_locations'
    )
    upazila = models.ForeignKey(
        Upazila,
        on_delete=models.CASCADE,
        related_name='postal_locations'
    )
    union = models.ForeignKey(
        Union,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='postal_locations'
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='postal_locations'
    )
    aliases = models.JSONField(
        default=list,
        blank=True,
        help_text="বিকল্প নাম বা ডাকঘরের পরিচিত উপনামসমূহ"
    )
    source = models.CharField(
        max_length=100,
        default='Bangladesh Post Master / BBS',
        help_text="তথ্যসূত্র বা উৎস"
    )
    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.OFFICIALLY_CONFIRMED,
        db_index=True
    )

    class Meta:
        verbose_name = 'ডাকঘর অবস্থান (Postal Location)'
        verbose_name_plural = 'ডাকঘর অবস্থানসমূহ (Postal Locations)'
        ordering = ['post_code', 'name_en']

    def __str__(self):
        return f"{self.post_office_name_bn} ({self.post_code})"


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
    postal_location = models.ForeignKey(
        PostalLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    detailed_address = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="বিস্তারিত ঠিকানা (ঐচ্ছিক)"
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
