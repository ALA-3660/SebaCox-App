"""
Eligibility Rules Engine for SebaCox Matching.
Phase 7: Explainable Multi-Dimensional Evaluation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple
from decimal import Decimal

from apps.demands.constants import DemandStatus
from apps.providers.constants import ProviderStatus, AvailabilityStatus, VerificationStatus
from apps.locations.services import calculate_haversine_distance
from .constants import (
    MatchFactorCode,
    ServiceMatchLevel,
    LocationMatchLevel,
    TimeCompatibilityLevel,
)


@dataclass
class RuleEvaluationResult:
    """
    Result of evaluating a specific eligibility rule.
    """
    rule_name: str
    is_eligible: bool
    factor_code: str
    score_weight_key: str
    details: Dict[str, Any]
    explanation_bn: str


class DemandStatusRule:
    """
    Rule 1: Demand Status Enforcement.
    Only PUBLISHED, active, and non-deleted Demands can be matched.
    """
    @staticmethod
    def evaluate(demand) -> RuleEvaluationResult:
        status = getattr(demand, 'status', None)
        is_active = getattr(demand, 'is_active', False)
        is_deleted = getattr(demand, 'is_deleted', False)

        if status == DemandStatus.PUBLISHED and is_active and not is_deleted:
            return RuleEvaluationResult(
                rule_name="DemandStatus",
                is_eligible=True,
                factor_code="DEMAND_PUBLISHED",
                score_weight_key="DEMAND_PUBLISHED",
                details={'status': status},
                explanation_bn="প্রয়োজনটি সক্রিয় ও প্রকাশিত"
            )

        return RuleEvaluationResult(
            rule_name="DemandStatus",
            is_eligible=False,
            factor_code="DEMAND_NOT_PUBLISHED",
            score_weight_key="DEMAND_NOT_PUBLISHED",
            details={'status': status, 'is_active': is_active, 'is_deleted': is_deleted},
            explanation_bn=f"প্রয়োজনটি প্রকাশিত অবস্থায় নেই ({status})"
        )


class ServiceProviderStatusRule:
    """
    Rule 2: Provider Status Enforcement.
    ONLY providers with status=ACTIVE can be candidate matches.
    Excludes DRAFT, PENDING_REVIEW, SUSPENDED, INACTIVE, REJECTED.
    """
    @staticmethod
    def evaluate(provider) -> RuleEvaluationResult:
        status = getattr(provider, 'status', None)
        is_active = getattr(provider, 'is_active', True)

        if status == ProviderStatus.ACTIVE and is_active:
            return RuleEvaluationResult(
                rule_name="ProviderStatus",
                is_eligible=True,
                factor_code=MatchFactorCode.PROVIDER_ACTIVE,
                score_weight_key="PROVIDER_ACTIVE",
                details={'status': status},
                explanation_bn="সেবাদাতা সক্রিয় অবস্থায় আছেন"
            )

        return RuleEvaluationResult(
            rule_name="ProviderStatus",
            is_eligible=False,
            factor_code=MatchFactorCode.PROVIDER_NOT_ACTIVE,
            score_weight_key="PROVIDER_NOT_ACTIVE",
            details={'status': status, 'is_active': is_active},
            explanation_bn=f"সেবাদাতা সক্রিয় নন (বর্তমান অবস্থা: {status})"
        )

# Alias for backward compatibility
ProviderStatusRule = ServiceProviderStatusRule


class ServiceOfferingStatusRule:
    """
    Rule 3: ProviderService Status Enforcement.
    Provider's specific service offering must have is_active=True and is_available=True.
    """
    @staticmethod
    def evaluate(provider_service) -> RuleEvaluationResult:
        if not provider_service:
            # If no specific ProviderService is passed, cannot verify service offering status
            return RuleEvaluationResult(
                rule_name="ProviderServiceStatus",
                is_eligible=False,
                factor_code=MatchFactorCode.PROVIDER_SERVICE_UNAVAILABLE,
                score_weight_key="PROVIDER_SERVICE_UNAVAILABLE",
                details={'reason': 'No provider_service specified'},
                explanation_bn="সেবাদাতার নির্দিষ্ট সেবা ম্যাপিং পাওয়া যায়নি"
            )

        is_active = getattr(provider_service, 'is_active', False)
        is_available = getattr(provider_service, 'is_available', False)

        if is_active and is_available:
            return RuleEvaluationResult(
                rule_name="ProviderServiceStatus",
                is_eligible=True,
                factor_code=MatchFactorCode.PROVIDER_SERVICE_ACTIVE_AVAILABLE,
                score_weight_key="PROVIDER_SERVICE_ACTIVE_AVAILABLE",
                details={'is_active': is_active, 'is_available': is_available},
                explanation_bn="সেবাটি সক্রিয় এবং বর্তমানে প্রদানযোগ্য"
            )

        return RuleEvaluationResult(
            rule_name="ProviderServiceStatus",
            is_eligible=False,
            factor_code=MatchFactorCode.PROVIDER_SERVICE_UNAVAILABLE,
            score_weight_key="PROVIDER_SERVICE_UNAVAILABLE",
            details={'is_active': is_active, 'is_available': is_available},
            explanation_bn="সেবাদাতার এই সেবাটি বর্তমানে সাময়িকভাবে বন্ধ"
        )

# Alias for backward compatibility
ProviderServiceStatusRule = ServiceOfferingStatusRule


class ServiceMatchRule:
    """
    Rule 4: Service & Taxonomy Compatibility.
    - Exact Service Match: strongest signal (Demand.service == ProviderService.service)
    - Category Compatibility: same category fallback (Demand.category == ProviderService.service.category)
    - Incompatible: different service/category
    """
    @staticmethod
    def evaluate(demand, provider_service) -> RuleEvaluationResult:
        demand_service_id = getattr(demand, 'service_id', None)
        demand_category_id = getattr(demand, 'category_id', None)

        if not provider_service or not getattr(provider_service, 'service', None):
            return RuleEvaluationResult(
                rule_name="ServiceMatch",
                is_eligible=False,
                factor_code=MatchFactorCode.SERVICE_INCOMPATIBLE,
                score_weight_key="SERVICE_INCOMPATIBLE",
                details={'reason': 'Missing provider service'},
                explanation_bn="সেবা সনাক্ত করা সম্ভব হয়নি"
            )

        p_service = provider_service.service
        p_service_id = p_service.id
        p_category_id = getattr(p_service, 'category_id', None)

        # 1. Exact Service Match
        if demand_service_id and demand_service_id == p_service_id:
            service_name = getattr(p_service, 'name_bn', '')
            return RuleEvaluationResult(
                rule_name="ServiceMatch",
                is_eligible=True,
                factor_code=MatchFactorCode.SERVICE_EXACT,
                score_weight_key="SERVICE_EXACT",
                details={'service_id': p_service_id, 'match_level': ServiceMatchLevel.EXACT},
                explanation_bn=f"✓ হুবহু একই সেবা ({service_name or 'নির্দিষ্ট সেবা'})"
            )

        # 2. Category Match
        # If demand has no specific service, or services differ but categories match
        eff_demand_cat = demand_category_id
        if not eff_demand_cat and getattr(demand, 'service', None):
            eff_demand_cat = getattr(demand.service, 'category_id', None)

        if eff_demand_cat and p_category_id and eff_demand_cat == p_category_id:
            return RuleEvaluationResult(
                rule_name="ServiceMatch",
                is_eligible=True,
                factor_code=MatchFactorCode.SERVICE_CATEGORY_COMPATIBLE,
                score_weight_key="SERVICE_CATEGORY_COMPATIBLE",
                details={'category_id': p_category_id, 'match_level': ServiceMatchLevel.CATEGORY},
                explanation_bn="✓ সম্পর্কিত ক্যাটাগরির সেবা প্রদান করেন"
            )

        return RuleEvaluationResult(
            rule_name="ServiceMatch",
            is_eligible=False,
            factor_code=MatchFactorCode.SERVICE_INCOMPATIBLE,
            score_weight_key="SERVICE_INCOMPATIBLE",
            details={'demand_service': demand_service_id, 'provider_service': p_service_id},
            explanation_bn="সেবার ধরন মিল নেই"
        )


class LocationCoverageRule:
    """
    Rule 5: Location Coverage & Geographic Containment.
    Evaluates administrative hierarchy and GPS radius:
    - Exact Ward/Union Match (highest precision)
    - Upazila Match (direct coverage)
    - District Match (parent containment - district covers child upazilas)
    - GPS Radius Match (calculated distance <= radius_km)
    """
    @staticmethod
    def evaluate(demand, service_areas) -> Tuple[RuleEvaluationResult, Optional[float]]:
        """
        Returns (RuleEvaluationResult, calculated_distance_km)
        """
        demand_district_id = getattr(demand, 'district_id', None)
        demand_upazila_id = getattr(demand, 'upazila_id', None)
        demand_union_id = getattr(demand, 'union_id', None)
        demand_ward_id = getattr(demand, 'ward_id', None)

        # Extract demand coordinates if present
        demand_lat = None
        demand_lon = None
        if hasattr(demand, 'geo_location') and demand.geo_location:
            demand_lat = getattr(demand.geo_location, 'latitude', None)
            demand_lon = getattr(demand.geo_location, 'longitude', None)

        best_match = None
        best_level_priority = -1
        computed_distance_km = None

        if not service_areas:
            return RuleEvaluationResult(
                rule_name="LocationCoverage",
                is_eligible=False,
                factor_code=MatchFactorCode.LOCATION_NOT_COVERED,
                score_weight_key="LOCATION_NOT_COVERED",
                details={'reason': 'Provider has no service areas defined'},
                explanation_bn="সেবাদাতার কোনো নির্ধারিত সেবা এলাকা নেই"
            ), None

        for area in service_areas:
            if not getattr(area, 'is_active', True):
                continue

            # 1. Exact Ward match (Priority 5)
            if demand_ward_id and getattr(area, 'ward_id', None) == demand_ward_id:
                if best_level_priority < 5:
                    best_level_priority = 5
                    best_match = (MatchFactorCode.LOCATION_COVERED_EXACT, "LOCATION_COVERED_EXACT", "✓ আপনার নির্দিষ্ট ওয়ার্ডের সেবাদাতা")

            # 2. Exact Union match (Priority 4)
            elif demand_union_id and getattr(area, 'union_id', None) == demand_union_id:
                if best_level_priority < 4:
                    best_level_priority = 4
                    best_match = (MatchFactorCode.LOCATION_COVERED_EXACT, "LOCATION_COVERED_EXACT", "✓ আপনার নির্দিষ্ট ইউনিয়নের সেবাদাতা")

            # 3. GPS Radial Coverage (Priority 3.5)
            elif (getattr(area, 'radius_km', None) and getattr(area, 'center_latitude', None) is not None
                  and getattr(area, 'center_longitude', None) is not None and demand_lat is not None and demand_lon is not None):
                try:
                    dist = calculate_haversine_distance(
                        float(demand_lat), float(demand_lon),
                        float(area.center_latitude), float(area.center_longitude)
                    )
                    radius = float(area.radius_km)
                    if dist <= radius:
                        computed_distance_km = dist
                        if best_level_priority < 3.5:
                            best_level_priority = 3.5
                            best_match = (
                                MatchFactorCode.LOCATION_COVERED_RADIUS,
                                "LOCATION_COVERED_RADIUS",
                                f"✓ আপনার অবস্থানের নিকটবর্তী ({dist:.1f} কিমি কভারেজ)"
                            )
                except Exception:
                    pass

            # 4. Upazila match (Priority 3)
            elif demand_upazila_id and getattr(area, 'upazila_id', None) == demand_upazila_id:
                upazila_name = getattr(area.upazila, 'name_bn', '') if hasattr(area, 'upazila') and area.upazila else ''
                if best_level_priority < 3:
                    best_level_priority = 3
                    best_match = (
                        MatchFactorCode.LOCATION_COVERED_UPAZILA,
                        "LOCATION_COVERED_UPAZILA",
                        f"✓ আপনার উপজেলায় সেবা দেন ({upazila_name or 'উপজেলা কভারেজ'})"
                    )

            # 5. District-wide coverage (Parent containment) (Priority 2)
            elif (getattr(area, 'district_id', None) and demand_district_id and
                  getattr(area, 'district_id', None) == demand_district_id and
                  not getattr(area, 'upazila_id', None)): # District level without restricting upazila
                if best_level_priority < 2:
                    best_level_priority = 2
                    best_match = (
                        MatchFactorCode.LOCATION_COVERED_DISTRICT,
                        "LOCATION_COVERED_DISTRICT",
                        "✓ জেলাব্যাপী সেবাদানকারী প্রতিষ্ঠান"
                    )

        if best_match:
            factor_code, weight_key, exp_bn = best_match
            return RuleEvaluationResult(
                rule_name="LocationCoverage",
                is_eligible=True,
                factor_code=factor_code,
                score_weight_key=weight_key,
                details={'priority': best_level_priority, 'distance_km': computed_distance_km},
                explanation_bn=exp_bn
            ), computed_distance_km

        return RuleEvaluationResult(
            rule_name="LocationCoverage",
            is_eligible=False,
            factor_code=MatchFactorCode.LOCATION_NOT_COVERED,
            score_weight_key="LOCATION_NOT_COVERED",
            details={'demand_upazila': demand_upazila_id, 'demand_district': demand_district_id},
            explanation_bn="প্রয়োজনের এলাকায় এই সেবাদাতার কভারেজ নেই"
        ), None


class ServiceProviderAvailabilityRule:
    """
    Rule 6: Availability Signal Evaluation.
    Evaluates provider's live availability status (AVAILABLE, BUSY, OFFLINE).
    """
    @staticmethod
    def evaluate(provider) -> RuleEvaluationResult:
        avail = getattr(provider, 'availability_status', AvailabilityStatus.AVAILABLE)

        if avail == AvailabilityStatus.AVAILABLE:
            return RuleEvaluationResult(
                rule_name="ProviderAvailability",
                is_eligible=True,
                factor_code=MatchFactorCode.AVAILABILITY_AVAILABLE,
                score_weight_key="AVAILABILITY_AVAILABLE",
                details={'status': avail},
                explanation_bn="✓ বর্তমানে সেবায় প্রস্তুত ও সক্রিয়"
            )
        elif avail == AvailabilityStatus.BUSY:
            return RuleEvaluationResult(
                rule_name="ProviderAvailability",
                is_eligible=True, # Eligible, but with busy note
                factor_code=MatchFactorCode.AVAILABILITY_BUSY,
                score_weight_key="AVAILABILITY_BUSY",
                details={'status': avail},
                explanation_bn="⚠ সেবাদাতা বর্তমানে ব্যস্ত, তবে সেবা দিতে পারেন"
            )
        else: # OFFLINE
            return RuleEvaluationResult(
                rule_name="ProviderAvailability",
                is_eligible=True, # Offline providers remain candidates, but ranked lower
                factor_code=MatchFactorCode.AVAILABILITY_OFFLINE,
                score_weight_key="AVAILABILITY_OFFLINE",
                details={'status': avail},
                explanation_bn="⚠ সেবাদাতা বর্তমানে অফলাইনে আছেন"
            )

# Alias for backward compatibility
ProviderAvailabilityRule = ServiceProviderAvailabilityRule


class VerificationFactorRule:
    """
    Rule 7: Verification Status Evaluation.
    Non-blocking factor that enriches scoring and trustworthiness.
    """
    @staticmethod
    def evaluate(provider) -> RuleEvaluationResult:
        is_verified = getattr(provider, 'is_verified', False)
        ver_status = getattr(provider, 'verification_status', VerificationStatus.UNVERIFIED)

        if is_verified or ver_status == VerificationStatus.VERIFIED:
            return RuleEvaluationResult(
                rule_name="VerificationFactor",
                is_eligible=True,
                factor_code=MatchFactorCode.VERIFICATION_VERIFIED,
                score_weight_key="VERIFICATION_VERIFIED",
                details={'verification_status': ver_status},
                explanation_bn="✓ প্ল্যাটফর্ম কর্তৃক যাচাইকৃত সেবাদাতা"
            )
        elif ver_status == VerificationStatus.PENDING:
            return RuleEvaluationResult(
                rule_name="VerificationFactor",
                is_eligible=True,
                factor_code=MatchFactorCode.VERIFICATION_PENDING,
                score_weight_key="VERIFICATION_PENDING",
                details={'verification_status': ver_status},
                explanation_bn="— যাচাইকরণ প্রক্রিয়াধীন"
            )
        else:
            return RuleEvaluationResult(
                rule_name="VerificationFactor",
                is_eligible=True,
                factor_code=MatchFactorCode.VERIFICATION_UNVERIFIED,
                score_weight_key="VERIFICATION_UNVERIFIED",
                details={'verification_status': ver_status},
                explanation_bn="— সাধারণ সেবাদাতা প্রোফাইল"
            )


class TimeCompatibilityRule:
    """
    Rule 8: Required Time Compatibility.
    Evaluates demand required_at against provider availability signal.
    """
    @staticmethod
    def evaluate(demand, provider) -> RuleEvaluationResult:
        required_at = getattr(demand, 'required_at', None)
        avail = getattr(provider, 'availability_status', AvailabilityStatus.AVAILABLE)

        if not required_at:
            return RuleEvaluationResult(
                rule_name="TimeCompatibility",
                is_eligible=True,
                factor_code=MatchFactorCode.TIME_UNKNOWN,
                score_weight_key="TIME_UNKNOWN",
                details={'required_at': None},
                explanation_bn="— নির্দিষ্ট সময়সূচি এখনো নির্ধারিত নয়"
            )

        # If required_at is set, check provider availability signal
        if avail == AvailabilityStatus.AVAILABLE:
            return RuleEvaluationResult(
                rule_name="TimeCompatibility",
                is_eligible=True,
                factor_code=MatchFactorCode.TIME_COMPATIBLE,
                score_weight_key="TIME_COMPATIBLE",
                details={'required_at': str(required_at), 'availability': avail},
                explanation_bn="✓ প্রয়োজনের সময়ে সেবা প্রদানে প্রস্তুত"
            )
        elif avail == AvailabilityStatus.BUSY:
            return RuleEvaluationResult(
                rule_name="TimeCompatibility",
                is_eligible=True,
                factor_code=MatchFactorCode.TIME_UNKNOWN,
                score_weight_key="TIME_UNKNOWN",
                details={'required_at': str(required_at), 'availability': avail},
                explanation_bn="— সেবাদাতা ব্যস্ত থাকায় সময়সূচি সমন্বয় প্রয়োজন"
            )
        else:
            return RuleEvaluationResult(
                rule_name="TimeCompatibility",
                is_eligible=True,
                factor_code=MatchFactorCode.TIME_UNKNOWN,
                score_weight_key="TIME_UNKNOWN",
                details={'required_at': str(required_at), 'availability': avail},
                explanation_bn="— অফলাইনে থাকায় সময়সূচি নিশ্চিত নয়"
            )
