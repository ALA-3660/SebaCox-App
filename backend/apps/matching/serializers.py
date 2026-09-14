"""
Serializers for SebaCox Matching Engine.
Phase 7: Privacy-Preserving, Zero-Fake Data Serialization.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from rest_framework import serializers
from .models import MatchCandidate, MatchingRun
from apps.demands.services import mask_phone_number


class MatchedProviderBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    display_name_bn = serializers.CharField(read_only=True)
    display_name_en = serializers.CharField(read_only=True)
    provider_type = serializers.CharField(read_only=True)
    provider_type_display = serializers.CharField(source='get_provider_type_display', read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    verification_status = serializers.CharField(read_only=True)
    availability_status = serializers.CharField(read_only=True)
    availability_status_display = serializers.CharField(source='get_availability_status_display', read_only=True)
    profile_image = serializers.CharField(read_only=True)
    contact_phone = serializers.SerializerMethodField()

    def get_contact_phone(self, obj):
        # Enforce phone privacy masking
        request = self.context.get('request')
        phone = getattr(obj, 'contact_phone', '')
        if not phone and hasattr(obj, 'user') and obj.user:
            phone = getattr(obj.user, 'mobile_number', '')
        if not phone:
            return ''
        # If user is staff or demand requester, phone can be visible, else masked
        if request and request.user and request.user.is_authenticated:
            return phone
        return mask_phone_number(phone)


class MatchedOfferingBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    service_id = serializers.IntegerField(source='service.id', read_only=True)
    service_name_bn = serializers.CharField(source='service.name_bn', read_only=True)
    service_name_en = serializers.CharField(source='service.name_en', read_only=True)
    title_bn = serializers.CharField(read_only=True)
    starting_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    price_type = serializers.CharField(read_only=True)


class MatchCandidateSerializer(serializers.ModelSerializer):
    provider = MatchedProviderBriefSerializer(read_only=True)
    provider_service = MatchedOfferingBriefSerializer(read_only=True)
    match_status_display = serializers.CharField(source='get_match_status_display', read_only=True)

    class Meta:
        model = MatchCandidate
        fields = [
            'id',
            'demand_id',
            'provider',
            'provider_service',
            'matching_version',
            'match_status',
            'match_status_display',
            'match_score',
            'rank',
            'distance_km',
            'matched_factors',
            'unmatched_factors',
            'explanations_bn',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class MatchingRunSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    trigger_display = serializers.CharField(source='get_trigger_display', read_only=True)

    class Meta:
        model = MatchingRun
        fields = [
            'id',
            'demand_id',
            'version',
            'trigger',
            'trigger_display',
            'status',
            'status_display',
            'candidate_count',
            'started_at',
            'completed_at',
            'execution_duration_ms',
            'error',
            'metadata',
            'created_at',
        ]
        read_only_fields = fields
