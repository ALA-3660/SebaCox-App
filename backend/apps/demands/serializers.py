"""
Serializers for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework import serializers
from .models import Demand, DemandAuditLog
from .constants import (
    DemandType,
    DemandStatus,
    DemandPriority,
    DemandVisibility,
    DemandContactPreference,
)
from .validators import (
    validate_demand_budget,
    validate_demand_quantity,
)
from .services import mask_phone_number


class DemandAuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = DemandAuditLog
        fields = [
            'id',
            'action',
            'action_display',
            'from_status',
            'to_status',
            'message',
            'actor_name',
            'created_at',
        ]

    def get_actor_name(self, obj):
        if not obj.actor:
            return 'সিস্টেম (System)'
        return getattr(obj.actor, 'full_name', getattr(obj.actor, 'phone', 'ব্যবহারকারী'))


class DemandListSerializer(serializers.ModelSerializer):
    """
    Public and user list serializer for Demands.
    Omits sensitive user details and respects privacy boundaries.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    demand_type_display = serializers.CharField(source='get_demand_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    service_name_bn = serializers.CharField(source='service.name_bn', read_only=True, default='')
    service_name_en = serializers.CharField(source='service.name_en', read_only=True, default='')
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True, default='')
    upazila_name_bn = serializers.CharField(source='upazila.name_bn', read_only=True, default='')
    upazila_name_en = serializers.CharField(source='upazila.name_en', read_only=True, default='')
    district_name_bn = serializers.CharField(source='district.name_bn', read_only=True, default='')
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Demand
        fields = [
            'id',
            'title_bn',
            'title_en',
            'description_bn',
            'demand_type',
            'demand_type_display',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'service_id',
            'service_name_bn',
            'service_name_en',
            'category_id',
            'category_name_bn',
            'quantity',
            'unit',
            'budget_min',
            'budget_max',
            'currency',
            'required_at',
            'expires_at',
            'district_name_bn',
            'upazila_id',
            'upazila_name_bn',
            'upazila_name_en',
            'location_display_bn',
            'visibility',
            'contact_preference',
            'is_owner',
            'published_at',
            'created_at',
        ]

    def get_is_owner(self, obj) -> bool:
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.requester_id == request.user.id


class DemandDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Demand representation.
    Enforces contact privacy: never blindly returns raw phone numbers.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    demand_type_display = serializers.CharField(source='get_demand_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)
    contact_preference_display = serializers.CharField(source='get_contact_preference_display', read_only=True)

    service_name_bn = serializers.CharField(source='service.name_bn', read_only=True, default='')
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True, default='')
    upazila_name_bn = serializers.CharField(source='upazila.name_bn', read_only=True, default='')
    district_name_bn = serializers.CharField(source='district.name_bn', read_only=True, default='')

    requester_name = serializers.SerializerMethodField()
    contact_phone = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    audit_logs = serializers.SerializerMethodField()

    class Meta:
        model = Demand
        fields = [
            'id',
            'requester_id',
            'requester_name',
            'contact_phone',
            'title_bn',
            'title_en',
            'description_bn',
            'description_en',
            'demand_type',
            'demand_type_display',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'service_id',
            'service_name_bn',
            'category_id',
            'category_name_bn',
            'quantity',
            'unit',
            'budget_min',
            'budget_max',
            'currency',
            'required_at',
            'expires_at',
            'district_id',
            'district_name_bn',
            'upazila_id',
            'upazila_name_bn',
            'union_id',
            'ward_id',
            'location_display_bn',
            'location_display_en',
            'visibility',
            'visibility_display',
            'contact_preference',
            'contact_preference_display',
            'is_owner',
            'can_edit',
            'audit_logs',
            'published_at',
            'fulfilled_at',
            'cancelled_at',
            'closed_at',
            'created_at',
            'updated_at',
        ]

    def get_is_owner(self, obj) -> bool:
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.requester_id == request.user.id

    def get_can_edit(self, obj) -> bool:
        request = self.context.get('request')
        if not request or not request.user:
            return False
        return obj.can_edit_by(request.user)

    def get_requester_name(self, obj) -> str:
        requester = obj.requester
        if not requester:
            return "ব্যবহারকারী"
        return getattr(requester, 'full_name', '') or "সেবাকক্স ব্যবহারকারী"

    def get_contact_phone(self, obj) -> str:
        request = self.context.get('request')
        user = request.user if request else None
        is_authorized = False
        if user and user.is_authenticated:
            # Owner or staff always authorized to see unmasked phone
            if obj.requester_id == user.id or user.is_staff or user.is_superuser:
                is_authorized = True
            elif obj.contact_preference in [DemandContactPreference.PHONE, DemandContactPreference.BOTH]:
                # Registered users allowed to see contact when preference allows
                is_authorized = True

        raw_phone = getattr(obj.requester, 'phone', '')
        return mask_phone_number(raw_phone, is_authorized=is_authorized)

    def get_audit_logs(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if not user or not user.is_authenticated:
            return []
        if obj.requester_id == user.id or user.is_staff or user.is_superuser:
            logs = obj.audit_logs.all().select_related('actor')[:10]
            return DemandAuditLogSerializer(logs, many=True).data
        return []


class DemandCreateSerializer(serializers.ModelSerializer):
    """
    Input serializer for creating a new Demand.
    Can optionally trigger immediate publish via publish_now boolean.
    """
    publish_now = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Demand
        fields = [
            'service',
            'category',
            'title_bn',
            'title_en',
            'description_bn',
            'description_en',
            'demand_type',
            'priority',
            'quantity',
            'unit',
            'budget_min',
            'budget_max',
            'currency',
            'required_at',
            'expires_at',
            'district',
            'upazila',
            'union',
            'ward',
            'geo_location',
            'location_display_bn',
            'location_display_en',
            'visibility',
            'contact_preference',
            'publish_now',
        ]

    def validate(self, attrs):
        validate_demand_budget(attrs.get('budget_min'), attrs.get('budget_max'))
        validate_demand_quantity(attrs.get('quantity'), attrs.get('unit'))
        return attrs


class DemandUpdateSerializer(serializers.ModelSerializer):
    """
    Input serializer for modifying an existing Demand.
    """
    class Meta:
        model = Demand
        fields = [
            'service',
            'category',
            'title_bn',
            'title_en',
            'description_bn',
            'description_en',
            'demand_type',
            'priority',
            'quantity',
            'unit',
            'budget_min',
            'budget_max',
            'currency',
            'required_at',
            'expires_at',
            'district',
            'upazila',
            'union',
            'ward',
            'geo_location',
            'location_display_bn',
            'location_display_en',
            'visibility',
            'contact_preference',
        ]

    def validate(self, attrs):
        validate_demand_budget(attrs.get('budget_min'), attrs.get('budget_max'))
        validate_demand_quantity(attrs.get('quantity'), attrs.get('unit'))
        return attrs
