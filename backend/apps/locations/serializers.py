"""
Serializers for Geographic and Location APIs.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework import serializers
from .validators import validate_latitude, validate_longitude, validate_radius
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
    ServiceArea,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name_bn', 'name_en', 'code', 'iso3', 'dial_code', 'currency_code', 'is_active']


class DivisionSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_en', read_only=True)

    class Meta:
        model = Division
        fields = ['id', 'country', 'country_name', 'name_bn', 'name_en', 'code', 'is_active']


class DistrictSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.name_en', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'division', 'division_name', 'name_bn', 'name_en', 'code', 'is_active']


class UpazilaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name_en', read_only=True)

    class Meta:
        model = Upazila
        fields = ['id', 'district', 'district_name', 'name_bn', 'name_en', 'code', 'is_active']


class MunicipalitySerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name_en', read_only=True)
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)

    class Meta:
        model = Municipality
        fields = ['id', 'district', 'district_name', 'upazila', 'upazila_name', 'name_bn', 'name_en', 'code', 'is_active']


class CityCorporationSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name_en', read_only=True)

    class Meta:
        model = CityCorporation
        fields = ['id', 'district', 'district_name', 'name_bn', 'name_en', 'code', 'is_active']


class UnionSerializer(serializers.ModelSerializer):
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)

    class Meta:
        model = Union
        fields = ['id', 'upazila', 'upazila_name', 'name_bn', 'name_en', 'code', 'is_active']


class WardSerializer(serializers.ModelSerializer):
    display_name_bn = serializers.CharField(read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'ward_number', 'display_name_bn', 'name_bn', 'name_en', 'code', 'municipality', 'city_corporation', 'union', 'is_active']


class LocalitySerializer(serializers.ModelSerializer):
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)
    ward_id = serializers.IntegerField(source='ward.id', read_only=True, allow_null=True)
    ward_number = serializers.IntegerField(source='ward.ward_number', read_only=True, allow_null=True)
    source_type = serializers.CharField(source='locality_type', read_only=True)
    source_reference = serializers.CharField(source='source', read_only=True)

    class Meta:
        model = Locality
        fields = [
            'id', 'upazila', 'upazila_name', 'municipality', 'union', 'ward',
            'ward_id', 'ward_number', 'locality_type', 'source_type', 'source_reference',
            'name_bn', 'name_en', 'code', 'postal_code',
            'aliases', 'source', 'verification_status', 'is_active'
        ]


class PostalLocationSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name_en', read_only=True)
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)

    class Meta:
        model = PostalLocation
        fields = [
            'id', 'post_office_name_bn', 'post_office_name_en', 'post_code',
            'district', 'district_name', 'upazila', 'upazila_name',
            'union', 'municipality', 'aliases', 'source',
            'verification_status', 'is_active'
        ]


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = ['id', 'latitude', 'longitude', 'srid', 'address_text', 'country', 'district', 'upazila', 'locality', 'is_active', 'created_at']


class UserLocationSerializer(serializers.ModelSerializer):
    geo_location = GeoLocationSerializer(read_only=True)
    district_name = serializers.CharField(source='district.name_en', read_only=True)
    district_name_bn = serializers.CharField(source='district.name_bn', read_only=True)
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)
    upazila_name_bn = serializers.CharField(source='upazila.name_bn', read_only=True)
    union_name = serializers.CharField(source='union.name_en', read_only=True)
    municipality_name = serializers.CharField(source='municipality.name_en', read_only=True)
    locality_name = serializers.CharField(source='locality.name_en', read_only=True)
    postal_office_bn = serializers.CharField(source='postal_location.post_office_name_bn', read_only=True)
    post_code = serializers.CharField(source='postal_location.post_code', read_only=True)

    class Meta:
        model = UserLocation
        fields = [
            'id', 'location_type', 'label', 'is_default', 'is_active',
            'district', 'district_name', 'district_name_bn',
            'upazila', 'upazila_name', 'upazila_name_bn',
            'union', 'union_name', 'municipality', 'municipality_name',
            'ward', 'locality', 'locality_name',
            'postal_location', 'postal_office_bn', 'post_code',
            'detailed_address',
            'geo_location', 'created_at'
        ]


class LocationSearchItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    type_label = serializers.CharField()
    name_bn = serializers.CharField()
    name_en = serializers.CharField()
    code = serializers.CharField()
    hierarchy_path = serializers.CharField()
    hierarchy_path_en = serializers.CharField()
    parent_id = serializers.IntegerField(allow_null=True, required=False)
    postal_code = serializers.CharField(allow_null=True, required=False)
    aliases = serializers.ListField(child=serializers.CharField(), required=False, default=list)


class SelectedLocationUpdateSerializer(serializers.Serializer):
    """Payload for updating user's active selected operational location."""
    district_id = serializers.IntegerField(required=False, allow_null=True)
    upazila_id = serializers.IntegerField(required=False, allow_null=True)
    union_id = serializers.IntegerField(required=False, allow_null=True)
    municipality_id = serializers.IntegerField(required=False, allow_null=True)
    ward_id = serializers.IntegerField(required=False, allow_null=True)
    locality_id = serializers.IntegerField(required=False, allow_null=True)
    postal_location_id = serializers.IntegerField(required=False, allow_null=True)
    detailed_address = serializers.CharField(required=False, allow_blank=True, max_length=255)
    label = serializers.CharField(required=False, allow_blank=True, max_length=100)


class CurrentLocationUpdateSerializer(serializers.Serializer):
    """Payload for registering current device GPS coordinates."""
    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_latitude]
    )
    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[validate_longitude]
    )
    address_text = serializers.CharField(required=False, allow_blank=True)


class NearbyCalculateRequestSerializer(serializers.Serializer):
    """Payload for calculating distance and checking proximity."""
    origin_latitude = serializers.DecimalField(max_digits=9, decimal_places=6, validators=[validate_latitude])
    origin_longitude = serializers.DecimalField(max_digits=9, decimal_places=6, validators=[validate_longitude])
    destination_latitude = serializers.DecimalField(max_digits=9, decimal_places=6, validators=[validate_latitude])
    destination_longitude = serializers.DecimalField(max_digits=9, decimal_places=6, validators=[validate_longitude])
    unit = serializers.ChoiceField(choices=['km', 'm'], default='km')
