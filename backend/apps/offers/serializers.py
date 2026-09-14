"""
Offer Serializers for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from decimal import Decimal
from rest_framework import serializers
from .models import Offer, OfferAuditLog
from .constants import (
    OfferStatus,
    OfferType,
    OFFER_STATUS_LABELS_BN,
    OFFER_TYPE_LABELS_BN,
    DEFAULT_CURRENCY,
)
from apps.demands.models import Demand
from apps.providers.models import Provider


class OfferAuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    action_label = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = OfferAuditLog
        fields = [
            'id',
            'offer',
            'actor',
            'actor_name',
            'action',
            'action_label',
            'previous_status',
            'new_status',
            'metadata',
            'created_at',
        ]

    def get_actor_name(self, obj):
        if not obj.actor:
            return "সিস্টেম (System)"
        return getattr(obj.actor, 'get_full_name', lambda: '')() or getattr(obj.actor, 'phone_number', str(obj.actor))


class OfferSerializer(serializers.ModelSerializer):
    status_label_bn = serializers.SerializerMethodField()
    offer_type_label_bn = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    is_terminal = serializers.BooleanField(read_only=True)
    provider_summary = serializers.SerializerMethodField()
    proposer_summary = serializers.SerializerMethodField()
    demand_summary = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'demand',
            'match_candidate',
            'provider',
            'requester',
            'proposer',
            'parent_offer',
            'root_offer',
            'version',
            'offer_type',
            'offer_type_label_bn',
            'status',
            'status_label_bn',
            'is_expired',
            'is_terminal',
            'title_bn',
            'description_bn',
            'quantity',
            'unit',
            'price',
            'currency',
            'delivery_fee',
            'service_fee',
            'total_amount',
            'terms_bn',
            'estimated_delivery_duration',
            'proposed_at',
            'expires_at',
            'accepted_at',
            'rejected_at',
            'cancelled_at',
            'rejection_reason_bn',
            'cancellation_reason_bn',
            'provider_summary',
            'proposer_summary',
            'demand_summary',
            'snapshot',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'demand',
            'match_candidate',
            'provider',
            'requester',
            'proposer',
            'parent_offer',
            'root_offer',
            'version',
            'offer_type',
            'status',
            'total_amount',
            'proposed_at',
            'accepted_at',
            'rejected_at',
            'cancelled_at',
            'created_at',
            'updated_at',
        ]

    def get_status_label_bn(self, obj):
        return OFFER_STATUS_LABELS_BN.get(obj.status, obj.status)

    def get_offer_type_label_bn(self, obj):
        return OFFER_TYPE_LABELS_BN.get(obj.offer_type, obj.offer_type)

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_provider_summary(self, obj):
        if not obj.provider:
            return None
        return {
            'id': obj.provider.id,
            'business_name_bn': getattr(obj.provider, 'business_name_bn', ''),
            'is_verified': getattr(obj.provider, 'is_verified', False),
            'rating_average': getattr(obj.provider, 'rating_average', '0.00'),
        }

    def get_proposer_summary(self, obj):
        if not obj.proposer:
            return None
        return {
            'id': obj.proposer.id,
            'name': getattr(obj.proposer, 'get_full_name', lambda: '')() or getattr(obj.proposer, 'phone_number', 'ব্যবহারকারী'),
        }

    def get_demand_summary(self, obj):
        if not obj.demand:
            return None
        return {
            'id': obj.demand.id,
            'title_bn': getattr(obj.demand, 'title_bn', ''),
            'demand_type': getattr(obj.demand, 'demand_type', ''),
            'status': getattr(obj.demand, 'status', ''),
        }


class CreateInitialOfferSerializer(serializers.Serializer):
    demand_id = serializers.IntegerField(required=True)
    provider_id = serializers.IntegerField(required=True)
    title_bn = serializers.CharField(max_length=255, required=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    delivery_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), required=False)
    service_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), required=False)
    description_bn = serializers.CharField(required=False, allow_blank=True, default='')
    quantity = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    unit = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')
    terms_bn = serializers.CharField(required=False, allow_blank=True, default='')
    estimated_delivery_duration = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    match_candidate_id = serializers.IntegerField(required=False, allow_null=True)
    currency = serializers.CharField(max_length=10, default=DEFAULT_CURRENCY, required=False)


class CreateCounterOfferSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    title_bn = serializers.CharField(max_length=255, required=False, allow_blank=True)
    delivery_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), required=False)
    service_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), required=False)
    description_bn = serializers.CharField(required=False, allow_blank=True)
    quantity = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    unit = serializers.CharField(max_length=50, required=False, allow_blank=True)
    terms_bn = serializers.CharField(required=False, allow_blank=True)
    estimated_delivery_duration = serializers.CharField(max_length=100, required=False, allow_blank=True)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)


class RejectOfferSerializer(serializers.Serializer):
    rejection_reason_bn = serializers.CharField(required=False, allow_blank=True, default='')


class CancelOfferSerializer(serializers.Serializer):
    cancellation_reason_bn = serializers.CharField(required=False, allow_blank=True, default='')
