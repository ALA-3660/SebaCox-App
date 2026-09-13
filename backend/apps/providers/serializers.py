"""
Serializers for Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from rest_framework import serializers
from django.utils.text import slugify

from .models import Provider, ProviderService, ProviderServiceArea, ProviderAuditLog
from .constants import (
    ProviderType,
    ProviderStatus,
    VerificationStatus,
    AvailabilityStatus,
    ContactVisibility,
    PriceType,
)
from .validators import validate_slug


class ProviderServiceAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for service area mappings with human-readable location labels.
    """
    district_name_bn = serializers.ReadOnlyField(source='district.name_bn', default=None)
    district_name_en = serializers.ReadOnlyField(source='district.name_en', default=None)
    upazila_name_bn = serializers.ReadOnlyField(source='upazila.name_bn', default=None)
    upazila_name_en = serializers.ReadOnlyField(source='upazila.name_en', default=None)
    union_name_bn = serializers.ReadOnlyField(source='union.name_bn', default=None)

    class Meta:
        model = ProviderServiceArea
        fields = [
            'id',
            'provider_id',
            'area_type',
            'district',
            'district_name_bn',
            'district_name_en',
            'upazila',
            'upazila_name_bn',
            'upazila_name_en',
            'municipality',
            'union',
            'union_name_bn',
            'ward',
            'locality',
            'service_area',
            'radius_km',
            'center_latitude',
            'center_longitude',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'provider_id', 'created_at']


class ProviderServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for mapped service offerings.
    Preserves platform service capabilities as Single Source of Truth.
    """
    service_name_bn = serializers.ReadOnlyField(source='service.name_bn')
    service_name_en = serializers.ReadOnlyField(source='service.name_en')
    service_slug = serializers.ReadOnlyField(source='service.slug')
    category_id = serializers.ReadOnlyField(source='service.category_id')
    category_name_bn = serializers.ReadOnlyField(source='service.category.name_bn')
    capabilities = serializers.ReadOnlyField(source='effective_capabilities')

    class Meta:
        model = ProviderService
        fields = [
            'id',
            'provider_id',
            'service',
            'service_name_bn',
            'service_name_en',
            'service_slug',
            'category_id',
            'category_name_bn',
            'title_bn',
            'title_en',
            'description_bn',
            'description_en',
            'starting_price',
            'price_type',
            'is_available',
            'is_active',
            'capabilities',
            'created_at',
        ]
        read_only_fields = ['id', 'provider_id', 'created_at', 'capabilities']


class ProviderListSerializer(serializers.ModelSerializer):
    """
    Public listing serializer for discovering providers.
    Masks or hides contact information based on privacy policy.
    """
    services_count = serializers.SerializerMethodField()
    primary_services = serializers.SerializerMethodField()
    primary_areas = serializers.SerializerMethodField()
    safe_contact_phone = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = [
            'id',
            'user_id',
            'provider_type',
            'display_name_bn',
            'display_name_en',
            'slug',
            'short_description_bn',
            'short_description_en',
            'profile_image',
            'cover_image',
            'safe_contact_phone',
            'contact_visibility',
            'status',
            'is_verified',
            'verification_status',
            'availability_status',
            'is_featured',
            'services_count',
            'primary_services',
            'primary_areas',
            'created_at',
        ]

    def get_services_count(self, obj):
        if hasattr(obj, 'services'):
            return obj.services.filter(is_active=True).count()
        return 0

    def get_primary_services(self, obj):
        if hasattr(obj, 'services'):
            return [
                {
                    'id': ps.id,
                    'service_id': ps.service_id,
                    'name_bn': ps.title_bn or ps.service.name_bn,
                    'name_en': ps.title_en or ps.service.name_en,
                }
                for ps in obj.services.filter(is_active=True)[:3]
            ]
        return []

    def get_primary_areas(self, obj):
        if hasattr(obj, 'service_areas'):
            return [
                {
                    'id': sa.id,
                    'upazila_bn': sa.upazila.name_bn if sa.upazila else None,
                    'district_bn': sa.district.name_bn if sa.district else None,
                }
                for sa in obj.service_areas.filter(is_active=True)[:3]
            ]
        return []

    def get_safe_contact_phone(self, obj):
        request = self.context.get('request')
        is_owner = request and request.user.is_authenticated and (request.user.id == obj.user_id or request.user.is_staff)
        if is_owner:
            return obj.contact_phone

        if obj.contact_visibility == ContactVisibility.PUBLIC:
            return obj.contact_phone
        elif obj.contact_visibility == ContactVisibility.REGISTERED_ONLY:
            if request and request.user.is_authenticated:
                return obj.contact_phone
            # Mask for unregistered
            if obj.contact_phone and len(obj.contact_phone) >= 7:
                return f"{obj.contact_phone[:4]}*****{obj.contact_phone[-2:]}"
            return "লগইন করে দেখুন"
        elif obj.contact_visibility == ContactVisibility.ON_REQUEST:
            return "অনুরোধ সাপেক্ষে"
        else:
            return "গোপন রাখা হয়েছে"


class ProviderDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive Provider detail serializer.
    Includes full service catalog and coverage areas.
    """
    services = ProviderServiceSerializer(many=True, read_only=True)
    service_areas = ProviderServiceAreaSerializer(many=True, read_only=True)
    safe_contact_phone = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = [
            'id',
            'user_id',
            'provider_type',
            'display_name_bn',
            'display_name_en',
            'slug',
            'short_description_bn',
            'short_description_en',
            'description_bn',
            'description_en',
            'profile_image',
            'cover_image',
            'contact_phone',
            'safe_contact_phone',
            'contact_email',
            'contact_visibility',
            'status',
            'is_verified',
            'verification_status',
            'availability_status',
            'is_featured',
            'is_active',
            'services',
            'service_areas',
            'created_at',
            'updated_at',
        ]

    def get_safe_contact_phone(self, obj):
        request = self.context.get('request')
        is_owner = request and request.user.is_authenticated and (request.user.id == obj.user_id or request.user.is_staff)
        if is_owner:
            return obj.contact_phone

        if obj.contact_visibility == ContactVisibility.PUBLIC:
            return obj.contact_phone
        elif obj.contact_visibility == ContactVisibility.REGISTERED_ONLY:
            if request and request.user.is_authenticated:
                return obj.contact_phone
            if obj.contact_phone and len(obj.contact_phone) >= 7:
                return f"{obj.contact_phone[:4]}*****{obj.contact_phone[-2:]}"
            return "লগইন করে দেখুন"
        elif obj.contact_visibility == ContactVisibility.ON_REQUEST:
            return "অনুরোধ সাপেক্ষে"
        else:
            return "গোপন রাখা হয়েছে"


class ProviderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for initiating and registering a new provider profile.
    Initial status starts at DRAFT or PENDING_REVIEW.
    """
    class Meta:
        model = Provider
        fields = [
            'id',
            'provider_type',
            'display_name_bn',
            'display_name_en',
            'slug',
            'short_description_bn',
            'short_description_en',
            'description_bn',
            'description_en',
            'profile_image',
            'cover_image',
            'contact_phone',
            'contact_email',
            'contact_visibility',
            'status',
        ]
        read_only_fields = ['id', 'status']

    def validate_slug(self, value):
        validate_slug(value)
        if Provider.objects.filter(slug=value).exists():
            raise serializers.ValidationError("এই স্লাগটি ইতিমধ্যে ব্যবহৃত হয়েছে। অন্য একটি নির্বাচন করুন।")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        # Generate slug if omitted
        if 'slug' not in validated_data or not validated_data['slug']:
            base = slugify(validated_data.get('display_name_en') or f"provider-{user.id}")
            validated_data['slug'] = base or f"provider-{user.id}"

        # Default contact phone to user's phone if blank
        if not validated_data.get('contact_phone') and hasattr(user, 'mobile_number'):
            validated_data['contact_phone'] = user.mobile_number

        validated_data['user'] = user
        validated_data['status'] = ProviderStatus.DRAFT
        validated_data['verification_status'] = VerificationStatus.UNVERIFIED
        provider = super().create(validated_data)

        # Audit log creation
        ProviderAuditLog.objects.create(
            provider=provider,
            actor=user,
            action='CREATED',
            from_state='',
            to_state=ProviderStatus.DRAFT,
            note='নতুন সেবাদাতা প্রোফাইল তৈরি হয়েছে'
        )
        return provider


class ProviderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing provider profile.
    Does NOT permit bypass of status or verification flags without workflow.
    """
    class Meta:
        model = Provider
        fields = [
            'provider_type',
            'display_name_bn',
            'display_name_en',
            'short_description_bn',
            'short_description_en',
            'description_bn',
            'description_en',
            'profile_image',
            'cover_image',
            'contact_phone',
            'contact_email',
            'contact_visibility',
        ]


class ProviderAvailabilitySerializer(serializers.Serializer):
    """
    Dedicated serializer for updating availability status.
    """
    availability_status = serializers.ChoiceField(choices=AvailabilityStatus.choices)
    note = serializers.CharField(required=False, allow_blank=True, default='')
