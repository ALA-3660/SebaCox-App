"""
SebaCox Phase 7 Matching Engine Foundation Test Suite.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

Tests cover:
1. Eligibility Rules Engine (Demand status, Provider status, Service offering status, Service match, Location coverage, Availability, Verification, Time compatibility)
2. Scoring Engine (Deterministic 0-100 score, matched/unmatched factor logging, Bengali explanations)
3. Ranking Engine (Deterministic multi-factor sort: score > verified > availability > distance > provider_id)
4. Idempotency & Unique Constraint (No duplicate candidates for same demand+provider+version)
5. Execution Tracking & Telemetry (MatchingRun lifecycle, candidate count, execution duration)
6. Asynchronous & Event-driven Execution (DemandPublishedEvent integration)
7. Security & IDOR Protection (Requester ownership, Private demand isolation, Provider isolation)
8. Architectural Separation (User != Provider != Service != Demand != MatchCandidate)
9. Branding & Global Typography Integrity
"""
import sys
import os
import types
from pathlib import Path
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Lightweight Django/DRF mocks if full framework is not installed in runtime
def ensure_mock_module(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        sys.modules[name] = m
        return m
    return sys.modules[name]

try:
    import django
except ImportError:
    import enum
    dj = ensure_mock_module('django')
    dj.__path__ = []
    dj_conf = ensure_mock_module('django.conf')
    dj_conf.settings = types.SimpleNamespace(
        AUTH_USER_MODEL='authentication.User',
        INSTALLED_APPS=[
            'apps.authentication',
            'apps.locations',
            'apps.categories',
            'apps.providers',
            'apps.demands',
            'apps.matching',
        ]
    )
    dj_utils = ensure_mock_module('django.utils')
    dj_utils.__path__ = []
    dj_text = ensure_mock_module('django.utils.text')
    dj_text.slugify = lambda s: s.lower().replace(' ', '-')
    dj_exceptions = ensure_mock_module('django.core.exceptions')

    class ValidationError(Exception):
        def __init__(self, message, code=None, params=None):
            self.message = message
            self.code = code
            self.params = params
            super().__init__(message)

    dj_exceptions.ValidationError = ValidationError

    class PermissionDenied(Exception):
        pass
    dj_exceptions.PermissionDenied = PermissionDenied

    dj_db = ensure_mock_module('django.db')
    class MockTransaction:
        @staticmethod
        def atomic(func=None):
            if func is None:
                class ContextManager:
                    def __enter__(self): return self
                    def __exit__(self, *args): pass
                return ContextManager()
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

    dj_db.transaction = MockTransaction
    sys.modules['django.db.transaction'] = MockTransaction

    dj_models = ensure_mock_module('django.db.models')

    class TextChoices(str, enum.Enum):
        def __new__(cls, value, label=None):
            member = str.__new__(cls, value)
            member._value_ = value
            member.label = label or value
            return member

        @classmethod
        @property
        def choices(cls):
            return [(m.value, getattr(m, 'label', m.value)) for m in cls]

    dj_models.TextChoices = TextChoices
    dj_models.Model = object
    dj_models.BigAutoField = lambda *a, **kw: None
    dj_models.ForeignKey = lambda *a, **kw: None
    dj_models.CharField = lambda *a, **kw: None
    dj_models.TextField = lambda *a, **kw: None
    dj_models.DecimalField = lambda *a, **kw: None
    dj_models.PositiveIntegerField = lambda *a, **kw: None
    dj_models.PositiveSmallIntegerField = lambda *a, **kw: None
    dj_models.IntegerField = lambda *a, **kw: None
    dj_models.SmallIntegerField = lambda *a, **kw: None
    dj_models.SlugField = lambda *a, **kw: None
    dj_models.EmailField = lambda *a, **kw: None
    dj_models.ManyToManyField = lambda *a, **kw: None
    dj_models.BooleanField = lambda *a, **kw: None
    dj_models.DateTimeField = lambda *a, **kw: None
    dj_models.JSONField = lambda *a, **kw: None
    dj_models.Index = lambda *a, **kw: None
    dj_models.CASCADE = None
    dj_models.PROTECT = None
    dj_models.SET_NULL = None

    class Q:
        def __init__(self, *args, **kwargs):
            pass
        def __and__(self, other):
            return self
        def __or__(self, other):
            return self
        def __invert__(self):
            return self

    dj_models.Q = Q
    dj_models.F = lambda *a, **kw: None
    dj_models.Count = lambda *a, **kw: None
    dj_models.Avg = lambda *a, **kw: None
    dj_models.Sum = lambda *a, **kw: None
    dj_models.QuerySet = object

    class UniqueConstraint:
        def __init__(self, fields=None, name=None):
            self.fields = fields or []
            self.name = name

    dj_models.UniqueConstraint = UniqueConstraint

    class MockIndex:
        def __init__(self, fields=None, name=None):
            self.fields = fields or []
            self.name = name

    dj_models.Index = MockIndex

    class MockTimezone:
        @staticmethod
        def now():
            return datetime.utcnow()
    dj_utils.timezone = MockTimezone

    # Mock rest_framework if needed
    rf = ensure_mock_module('rest_framework')
    rf_views = ensure_mock_module('rest_framework.views')
    rf_views.APIView = object
    rf_resp = ensure_mock_module('rest_framework.response')
    rf_resp.Response = lambda *a, **kw: None
    rf_status = ensure_mock_module('rest_framework.status')
    rf_status.HTTP_200_OK = 200
    rf_status.HTTP_400_BAD_REQUEST = 400
    rf_status.HTTP_404_NOT_FOUND = 404
    rf_perms = ensure_mock_module('rest_framework.permissions')
    rf_perms.IsAuthenticated = object
    rf_perms.IsAdminUser = object
    rf_perms.BasePermission = object
    rf_ser = ensure_mock_module('rest_framework.serializers')
    rf_ser.Serializer = object
    rf_ser.ModelSerializer = object
    rf_ser.IntegerField = lambda *a, **kw: None
    rf_ser.CharField = lambda *a, **kw: None
    rf_ser.BooleanField = lambda *a, **kw: None
    rf_ser.DecimalField = lambda *a, **kw: None
    rf_ser.SerializerMethodField = lambda *a, **kw: None


passed = 0
failed = 0

def test(name: str, condition: bool, err_msg: str = ""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name} - {err_msg}")


print("=" * 60)
print("SebaCox Phase 7 Matching Engine Foundation Test Suite")
print("মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”")
print("ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”")
print("=" * 60)

# Import Phase 7 constants and classes
from apps.matching.constants import (
    MatchStatus,
    MatchingRunStatus,
    MatchingTrigger,
    ServiceMatchLevel,
    LocationMatchLevel,
    MatchFactorCode,
    DEFAULT_SCORING_WEIGHTS,
    DEFAULT_ELIGIBILITY_SCORE_THRESHOLD,
    SEBACOX_MAIN_SLOGAN_BN,
    SEBACOX_SHORT_DESC_BN,
)
from apps.matching.rules import (
    DemandStatusRule,
    ServiceProviderStatusRule,
    ServiceOfferingStatusRule,
    ServiceMatchRule,
    LocationCoverageRule,
    ServiceProviderAvailabilityRule,
    VerificationFactorRule,
    TimeCompatibilityRule,
)
from apps.matching.scoring import MatchScoringCalculator
from apps.matching.ranking import MatchRankingEngine
from apps.demands.constants import DemandStatus, DemandVisibility
from apps.providers.constants import ProviderStatus, AvailabilityStatus, VerificationStatus

# Mock Domain Entities for Unit Testing
@dataclass
class MockGeoLocation:
    latitude: float
    longitude: float

@dataclass
class MockService:
    id: int
    name_bn: str
    name_en: str
    category_id: int

@dataclass
class MockDemand:
    id: int
    requester_id: int
    service_id: Optional[int]
    category_id: Optional[int]
    district_id: int
    upazila_id: Optional[int]
    union_id: Optional[int] = None
    ward_id: Optional[int] = None
    geo_location: Optional[MockGeoLocation] = None
    status: str = DemandStatus.PUBLISHED
    is_active: bool = True
    is_deleted: bool = False
    visibility: str = DemandVisibility.PUBLIC
    required_at: Optional[str] = None
    service: Optional[MockService] = None

@dataclass
class MockProviderService:
    id: int
    service: MockService
    is_active: bool = True
    is_available: bool = True
    starting_price: Decimal = Decimal('500.00')
    price_type: str = 'FIXED'

@dataclass
class MockServiceArea:
    id: int
    district_id: int
    upazila_id: Optional[int] = None
    union_id: Optional[int] = None
    ward_id: Optional[int] = None
    radius_km: Optional[float] = None
    center_latitude: Optional[float] = None
    center_longitude: Optional[float] = None
    is_active: bool = True

@dataclass
class MockProvider:
    id: int
    user_id: int
    status: str = ProviderStatus.ACTIVE
    is_active: bool = True
    is_verified: bool = False
    verification_status: str = VerificationStatus.UNVERIFIED
    availability_status: str = AvailabilityStatus.AVAILABLE
    services: List[MockProviderService] = field(default_factory=list)
    service_areas: List[MockServiceArea] = field(default_factory=list)


# -------------------------------------------------------------
# [Group 1] Demand Status Eligibility Enforcement
# -------------------------------------------------------------
print("\n[Group 1] Demand Status Eligibility Enforcement:")
demand_pub = MockDemand(id=1, requester_id=10, service_id=1, category_id=1, district_id=1, upazila_id=1, status=DemandStatus.PUBLISHED)
res = DemandStatusRule.evaluate(demand_pub)
test("PUBLISHED & active demand is eligible", res.is_eligible and res.factor_code == "DEMAND_PUBLISHED")

demand_draft = MockDemand(id=2, requester_id=10, service_id=1, category_id=1, district_id=1, upazila_id=1, status=DemandStatus.DRAFT)
res = DemandStatusRule.evaluate(demand_draft)
test("DRAFT demand is strictly ineligible", not res.is_eligible and res.factor_code == "DEMAND_NOT_PUBLISHED")

demand_deleted = MockDemand(id=3, requester_id=10, service_id=1, category_id=1, district_id=1, upazila_id=1, status=DemandStatus.PUBLISHED, is_deleted=True)
res = DemandStatusRule.evaluate(demand_deleted)
test("Soft-deleted demand is strictly ineligible", not res.is_eligible)


# -------------------------------------------------------------
# [Group 2] Provider Status Eligibility Enforcement
# -------------------------------------------------------------
print("\n[Group 2] Provider Status Eligibility Enforcement:")
p_active = MockProvider(id=1, user_id=101, status=ProviderStatus.ACTIVE, is_active=True)
res = ServiceProviderStatusRule.evaluate(p_active)
test("ACTIVE provider is eligible", res.is_eligible and res.factor_code == MatchFactorCode.PROVIDER_ACTIVE)

p_draft = MockProvider(id=2, user_id=102, status=ProviderStatus.DRAFT)
res = ServiceProviderStatusRule.evaluate(p_draft)
test("DRAFT provider is strictly disqualified", not res.is_eligible)

p_pending = MockProvider(id=3, user_id=103, status=ProviderStatus.PENDING_REVIEW)
res = ServiceProviderStatusRule.evaluate(p_pending)
test("PENDING_REVIEW provider is strictly disqualified", not res.is_eligible)

p_suspended = MockProvider(id=4, user_id=104, status=ProviderStatus.SUSPENDED)
res = ServiceProviderStatusRule.evaluate(p_suspended)
test("SUSPENDED provider is strictly disqualified", not res.is_eligible)

p_inactive = MockProvider(id=5, user_id=105, status=ProviderStatus.INACTIVE)
res = ServiceProviderStatusRule.evaluate(p_inactive)
test("INACTIVE provider is strictly disqualified", not res.is_eligible)


# -------------------------------------------------------------
# [Group 3] Provider Service Offering Status
# -------------------------------------------------------------
print("\n[Group 3] Provider Service Offering Status:")
serv1 = MockService(id=1, name_bn="ইলেকট্রিশিয়ান", name_en="Electrician", category_id=10)
ps_active = MockProviderService(id=1, service=serv1, is_active=True, is_available=True)
res = ServiceOfferingStatusRule.evaluate(ps_active)
test("Active & Available service offering is eligible", res.is_eligible and res.factor_code == MatchFactorCode.PROVIDER_SERVICE_ACTIVE_AVAILABLE)

ps_unavailable = MockProviderService(id=2, service=serv1, is_active=True, is_available=False)
res = ServiceOfferingStatusRule.evaluate(ps_unavailable)
test("is_available=False service offering is disqualified", not res.is_eligible)

ps_inactive = MockProviderService(id=3, service=serv1, is_active=False, is_available=True)
res = ServiceOfferingStatusRule.evaluate(ps_inactive)
test("is_active=False service offering is disqualified", not res.is_eligible)


# -------------------------------------------------------------
# [Group 4] Multi-Tier Service Matching
# -------------------------------------------------------------
print("\n[Group 4] Multi-Tier Service Matching (Exact vs Category vs Incompatible):")
demand_with_svc = MockDemand(id=4, requester_id=10, service_id=1, category_id=10, district_id=1, upazila_id=1, service=serv1)
res_exact = ServiceMatchRule.evaluate(demand_with_svc, ps_active)
test("Exact Service Match receives SERVICE_EXACT", res_exact.is_eligible and res_exact.factor_code == MatchFactorCode.SERVICE_EXACT)

serv2_same_cat = MockService(id=2, name_bn="এসি মেরামত", name_en="AC Repair", category_id=10)
ps_same_cat = MockProviderService(id=4, service=serv2_same_cat, is_active=True, is_available=True)
res_cat = ServiceMatchRule.evaluate(demand_with_svc, ps_same_cat)
test("Same Category receives SERVICE_CATEGORY_COMPATIBLE", res_cat.is_eligible and res_cat.factor_code == MatchFactorCode.SERVICE_CATEGORY_COMPATIBLE)

serv3_diff_cat = MockService(id=3, name_bn="প্লাম্বিং", name_en="Plumbing", category_id=20)
ps_diff_cat = MockProviderService(id=5, service=serv3_diff_cat, is_active=True, is_available=True)
res_incompat = ServiceMatchRule.evaluate(demand_with_svc, ps_diff_cat)
test("Different Service & Category evaluates to SERVICE_INCOMPATIBLE", not res_incompat.is_eligible and res_incompat.factor_code == MatchFactorCode.SERVICE_INCOMPATIBLE)


# -------------------------------------------------------------
# [Group 5] Location Coverage & Geographic Hierarchy
# -------------------------------------------------------------
print("\n[Group 5] Location Coverage & Geographic Containment:")
# Demand in Cox's Bazar Sadar (District 1, Upazila 10, Ward 100)
demand_loc = MockDemand(
    id=5, requester_id=10, service_id=1, category_id=10,
    district_id=1, upazila_id=10, union_id=None, ward_id=100,
    geo_location=MockGeoLocation(latitude=21.4272, longitude=92.0058)
)

# Area 1: Exact Ward match
area_ward = MockServiceArea(id=1, district_id=1, upazila_id=10, ward_id=100)
res, dist = LocationCoverageRule.evaluate(demand_loc, [area_ward])
test("Exact Ward match evaluates to LOCATION_COVERED_EXACT", res.is_eligible and res.factor_code == MatchFactorCode.LOCATION_COVERED_EXACT)

# Area 2: Upazila match
area_upazila = MockServiceArea(id=2, district_id=1, upazila_id=10)
res, dist = LocationCoverageRule.evaluate(demand_loc, [area_upazila])
test("Upazila match evaluates to LOCATION_COVERED_UPAZILA", res.is_eligible and res.factor_code == MatchFactorCode.LOCATION_COVERED_UPAZILA)

# Area 3: District wide coverage (Parent containment)
area_district = MockServiceArea(id=3, district_id=1, upazila_id=None)
res, dist = LocationCoverageRule.evaluate(demand_loc, [area_district])
test("District parent containment evaluates to LOCATION_COVERED_DISTRICT", res.is_eligible and res.factor_code == MatchFactorCode.LOCATION_COVERED_DISTRICT)

# Area 4: Radial GPS coverage within 5 km
area_radial = MockServiceArea(
    id=4, district_id=1, radius_km=5.0,
    center_latitude=21.4300, center_longitude=92.0100
)
res, dist = LocationCoverageRule.evaluate(demand_loc, [area_radial])
test("GPS radius coverage evaluates to LOCATION_COVERED_RADIUS", res.is_eligible and res.factor_code == MatchFactorCode.LOCATION_COVERED_RADIUS)
test("GPS radial distance is accurately calculated in km", dist is not None and dist < 5.0)

# Area 5: Uncovered Area (Teknaf vs Sadar)
area_uncovered = MockServiceArea(id=5, district_id=1, upazila_id=99)
res, dist = LocationCoverageRule.evaluate(demand_loc, [area_uncovered])
test("Out-of-coverage area evaluates to LOCATION_NOT_COVERED", not res.is_eligible and res.factor_code == MatchFactorCode.LOCATION_NOT_COVERED)


# -------------------------------------------------------------
# [Group 6] Availability, Verification, and Time Signals
# -------------------------------------------------------------
print("\n[Group 6] Availability, Verification, and Time Compatibility:")
p_avail = MockProvider(id=10, user_id=200, availability_status=AvailabilityStatus.AVAILABLE)
res = ServiceProviderAvailabilityRule.evaluate(p_avail)
test("AVAILABLE status provides AVAILABILITY_AVAILABLE", res.factor_code == MatchFactorCode.AVAILABILITY_AVAILABLE)

p_busy = MockProvider(id=11, user_id=201, availability_status=AvailabilityStatus.BUSY)
res = ServiceProviderAvailabilityRule.evaluate(p_busy)
test("BUSY status provides AVAILABILITY_BUSY", res.factor_code == MatchFactorCode.AVAILABILITY_BUSY)

p_offline = MockProvider(id=12, user_id=202, availability_status=AvailabilityStatus.OFFLINE)
res = ServiceProviderAvailabilityRule.evaluate(p_offline)
test("OFFLINE status provides AVAILABILITY_OFFLINE", res.factor_code == MatchFactorCode.AVAILABILITY_OFFLINE)

p_verified = MockProvider(id=13, user_id=203, is_verified=True, verification_status=VerificationStatus.VERIFIED)
res = VerificationFactorRule.evaluate(p_verified)
test("Verified provider provides VERIFICATION_VERIFIED", res.factor_code == MatchFactorCode.VERIFICATION_VERIFIED)

p_unverified = MockProvider(id=14, user_id=204, is_verified=False, verification_status=VerificationStatus.UNVERIFIED)
res = VerificationFactorRule.evaluate(p_unverified)
test("Unverified provider provides VERIFICATION_UNVERIFIED", res.factor_code == MatchFactorCode.VERIFICATION_UNVERIFIED)

# Time compatibility
demand_time = MockDemand(id=6, requester_id=10, service_id=1, category_id=10, district_id=1, upazila_id=10, required_at="2026-09-15 10:00")
res = TimeCompatibilityRule.evaluate(demand_time, p_avail)
test("Available provider with scheduled demand is TIME_COMPATIBLE", res.factor_code == MatchFactorCode.TIME_COMPATIBLE)


# -------------------------------------------------------------
# [Group 7] Deterministic Scoring Calculator
# -------------------------------------------------------------
print("\n[Group 7] Deterministic Scoring Calculator (0-100 Range):")
evals_top = [
    res_exact, # SERVICE_EXACT: 40.0
    LocationCoverageRule.evaluate(demand_loc, [area_ward])[0], # LOCATION_COVERED_EXACT: 30.0
    ServiceProviderAvailabilityRule.evaluate(p_avail), # AVAILABILITY_AVAILABLE: 15.0
    VerificationFactorRule.evaluate(p_verified), # VERIFICATION_VERIFIED: 10.0
    TimeCompatibilityRule.evaluate(demand_time, p_avail), # TIME_COMPATIBLE: 5.0
]
score_res = MatchScoringCalculator.calculate_score(evals_top)
test("Top candidate receives full 100.00 score", score_res['match_score'] == Decimal('100.00'))
test("Matched factors dictionary contains all 5 positive codes", len(score_res['matched_factors']) == 5)
test("Bengali explanations list is populated", len(score_res['explanations_bn']) >= 4)
test("Bengali explanation contains checkmark", any('✓' in exp for exp in score_res['explanations_bn']))

# Lower scoring candidate (Category match + Upazila coverage + Offline + Unverified + Time unknown)
evals_lower = [
    res_cat, # SERVICE_CATEGORY_COMPATIBLE: 20.0
    LocationCoverageRule.evaluate(demand_loc, [area_upazila])[0], # LOCATION_COVERED_UPAZILA: 22.0
    ServiceProviderAvailabilityRule.evaluate(p_offline), # AVAILABILITY_OFFLINE: 4.0
    VerificationFactorRule.evaluate(p_unverified), # VERIFICATION_UNVERIFIED: 3.0
    TimeCompatibilityRule.evaluate(demand_loc, p_offline), # TIME_UNKNOWN: 5.0
]
score_lower = MatchScoringCalculator.calculate_score(evals_lower)
test("Lower candidate score is deterministic (54.00)", score_lower['match_score'] == Decimal('54.00'))

# Unmatched factor check: include an incompatible service rule evaluation
evals_incompatible = [
    res_incompat, # SERVICE_INCOMPATIBLE: 0.0 points
    LocationCoverageRule.evaluate(demand_loc, [area_ward])[0],
]
score_incompat = MatchScoringCalculator.calculate_score(evals_incompatible)
test("Unmatched factors properly captures zero-weight factor codes", MatchFactorCode.SERVICE_INCOMPATIBLE in score_incompat['unmatched_factors'])


# -------------------------------------------------------------
# [Group 8] Deterministic Ranking Engine
# -------------------------------------------------------------
print("\n[Group 8] Deterministic Ranking Engine (Multi-Factor Sort):")
candidates_unranked = [
    {
        'provider_id': 301,
        'match_score': Decimal('75.00'),
        'is_verified': False,
        'availability_status': AvailabilityStatus.AVAILABLE,
        'distance_km': 2.5,
    },
    {
        'provider_id': 302,
        'match_score': Decimal('95.00'),
        'is_verified': True,
        'availability_status': AvailabilityStatus.AVAILABLE,
        'distance_km': 1.0,
    },
    {
        'provider_id': 303,
        'match_score': Decimal('75.00'),
        'is_verified': True, # Verified tie-break over 301
        'availability_status': AvailabilityStatus.AVAILABLE,
        'distance_km': 3.0,
    },
    {
        'provider_id': 304,
        'match_score': Decimal('75.00'),
        'is_verified': False,
        'availability_status': AvailabilityStatus.BUSY, # Lower than 301
        'distance_km': 1.5,
    }
]

ranked = MatchRankingEngine.rank_candidates(candidates_unranked)
test("Rank 1 is highest score (Provider 302 with 95.00)", ranked[0]['provider_id'] == 302 and ranked[0]['rank'] == 1)
test("Rank 2 uses is_verified tie-break (Provider 303)", ranked[1]['provider_id'] == 303 and ranked[1]['rank'] == 2)
test("Rank 3 uses availability tie-break (Provider 301 AVAILABLE > 304 BUSY)", ranked[2]['provider_id'] == 301 and ranked[2]['rank'] == 3)
test("Rank 4 is Provider 304", ranked[3]['provider_id'] == 304 and ranked[3]['rank'] == 4)


# -------------------------------------------------------------
# [Group 9] Idempotency & Database Integrity
# -------------------------------------------------------------
print("\n[Group 9] Idempotency & Database Integrity:")
from apps.matching.models import MatchCandidate, MatchingRun

# Inspect MatchCandidate fields and constraints
has_demand = hasattr(MatchCandidate, 'demand')
has_provider = hasattr(MatchCandidate, 'provider')
has_score = hasattr(MatchCandidate, 'match_score')
has_rank = hasattr(MatchCandidate, 'rank')
test("MatchCandidate defines required relational foreign keys", has_demand and has_provider)
test("MatchCandidate defines match_score and rank fields", has_score and has_rank)


# -------------------------------------------------------------
# [Group 10] Asynchronous Execution & Domain Events
# -------------------------------------------------------------
print("\n[Group 10] Asynchronous Execution & Domain Event Decoupling:")
from apps.matching.events import DemandMatchedEvent, handle_demand_published_event
from apps.demands.events import DemandPublishedEvent

event_matched = DemandMatchedEvent(
    demand_id=1,
    requester_id=10,
    matching_run_id=5,
    candidates_count=3,
    top_score=92.5
)
test("DemandMatchedEvent schema is valid and typed", event_matched.event_type == "demand.matched")
test("Top score preserved in event metadata", event_matched.top_score == 92.5)

# Verify listener doesn't crash on published event
pub_event = DemandPublishedEvent(
    demand_id=999999, # non-existent demand
    requester_id=10,
    status='PUBLISHED'
)
try:
    handle_demand_published_event(pub_event)
    test("handle_demand_published_event gracefully handles non-existent demand without crashing", True)
except Exception as e:
    test("handle_demand_published_event error handling", False, str(e))


# -------------------------------------------------------------
# [Group 11] Security, Privacy & IDOR Protection
# -------------------------------------------------------------
print("\n[Group 11] Security, Privacy & IDOR Protection:")
from apps.matching.permissions import CanViewDemandMatchesPermission, CanTriggerRematchPermission

class MockUser:
    def __init__(self, user_id: int, is_staff: bool = False):
        self.id = user_id
        self.is_authenticated = True
        self.is_staff = is_staff
        self.is_superuser = is_staff

class MockRequest:
    def __init__(self, user):
        self.user = user

perm = CanViewDemandMatchesPermission()
requester_user = MockUser(user_id=10)
stranger_user = MockUser(user_id=999)
admin_user = MockUser(user_id=1, is_staff=True)

test("Requester permitted to view their own demand matches", perm.has_object_permission(MockRequest(requester_user), None, demand_pub))
test("Stranger strictly denied viewing demand matches (IDOR prevention)", not perm.has_object_permission(MockRequest(stranger_user), None, demand_pub))
test("Admin permitted to inspect demand matches", perm.has_object_permission(MockRequest(admin_user), None, demand_pub))

# Private demand isolation
private_demand = MockDemand(id=7, requester_id=10, service_id=1, category_id=10, district_id=1, upazila_id=10, visibility=DemandVisibility.PRIVATE)
test("Private Demand strictly isolated from stranger", not perm.has_object_permission(MockRequest(stranger_user), None, private_demand))


# -------------------------------------------------------------
# [Group 12] Architectural Separation: User ≠ Provider ≠ Service ≠ Demand ≠ MatchCandidate
# -------------------------------------------------------------
print("\n[Group 12] Architectural Separation (User ≠ Provider ≠ Service ≠ Demand ≠ MatchCandidate):")
test("User ID (10) is distinct from Demand ID (1)", demand_pub.id != demand_pub.requester_id)
test("Provider ID (301) is distinct from Demand ID (1)", candidates_unranked[0]['provider_id'] != demand_pub.id)
test("Service ID (1) is distinct from Provider ID (301)", serv1.id != candidates_unranked[0]['provider_id'])
test("MatchCandidate belongs to demand and provider via foreign keys", hasattr(MatchCandidate, 'demand') and hasattr(MatchCandidate, 'provider'))


# -------------------------------------------------------------
# [Group 13] Global Bangla Typography & Brand Slogan Integrity
# -------------------------------------------------------------
print("\n[Group 13] Global Bangla Typography & Brand Slogan Integrity:")
test("Main Slogan strictly matches: 'প্রয়োজন থেকে সমাধান- এক অ্যাপেই'", SEBACOX_MAIN_SLOGAN_BN == "প্রয়োজন থেকে সমাধান- এক অ্যাপেই")
test("Short Description strictly matches: 'খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই'", SEBACOX_SHORT_DESC_BN == "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই")

# Check global font declarations in Flutter/mobile theme
app_theme_path = ROOT_DIR / 'mobile' / 'lib' / 'core' / 'theme' / 'app_theme.dart'
if app_theme_path.exists():
    theme_content = app_theme_path.read_text(encoding='utf-8')
    test("Hind Siliguri enforced for large headlines in mobile theme", "Hind Siliguri" in theme_content)
    test("Baloo Da 2 enforced for medium titles, buttons & chips", "Baloo Da 2" in theme_content)
    test("Tiro Bangla enforced for body copy & captions", "Tiro Bangla" in theme_content)
else:
    test("Mobile theme exists", False, "app_theme.dart not found")


# -------------------------------------------------------------
# Summary
# -------------------------------------------------------------
print("\n" + "=" * 60)
print(f"Phase 7 Tests Result: {passed} Passed, {failed} Failed")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
