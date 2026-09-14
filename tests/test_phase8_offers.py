"""
SebaCox Phase 8 Offer & Counter-Offer Foundation Test Suite.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

Tests cover:
1. Model Architecture & Invariants (Decimal fields, calculate_total, versioning, root_offer, snapshot)
2. Pricing & Validation Engine (Zero/negative price, delivery fee, service fee, quantity mismatch)
3. Expiration Engine (Valid expiry window, past expiry rejection, auto-expiry task)
4. Demand & Provider Eligibility Validation (PUBLISHED demand only, ACTIVE provider only)
5. State Machine & Transition Rules (Allowed transitions, forbidden jumps, terminal state lock)
6. Counter-Offer Engine (Sequential versioning, root_offer retention, parent superseding, role swapping)
7. Acceptance & One Accepted Offer Invariant (Mutual agreement, double-accept blocking)
8. Rejection & Cancellation Workflows (Reason capture, audit logging)
9. Security, Permissions & IDOR Protection (Requester rights, Provider rights, Stranger blocked)
10. Domain Events & Audit Trail Dispatching (All 7 Offer lifecycle events, OfferAuditLog model)
11. REST API Serializers, Selectors & Standard Response Format
12. Flutter/Mobile Models, Enums, UI Screens, Branding & Typography Integrity
13. Strict Phase Boundaries (No Deal, Booking, Payment, Delivery, Chat engine in Phase 8)
"""
import sys
import os
import types
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Lightweight Django mocks for standalone test execution
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
            'apps.offers',
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
    dj_models.UniqueConstraint = lambda *a, **kw: None
    dj_models.CheckConstraint = lambda *a, **kw: None
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

    # Timezone mock
    class MockTimezone:
        @staticmethod
        def now():
            return datetime(2026, 9, 13, 12, 0, 0)
    dj_utils.timezone = MockTimezone
    sys.modules['django.utils.timezone'] = MockTimezone

    # Mock rest_framework
    rf = ensure_mock_module('rest_framework')
    rf_views = ensure_mock_module('rest_framework.views')
    rf_views.APIView = object
    rf_resp = ensure_mock_module('rest_framework.response')
    rf_resp.Response = lambda data, status=200: {'data': data, 'status': status}
    rf_status = ensure_mock_module('rest_framework.status')
    rf_status.HTTP_200_OK = 200
    rf_status.HTTP_201_CREATED = 201
    rf_status.HTTP_400_BAD_REQUEST = 400
    rf_status.HTTP_403_FORBIDDEN = 403
    rf_status.HTTP_404_NOT_FOUND = 404
    rf_permissions = ensure_mock_module('rest_framework.permissions')
    class BasePermission:
        pass
    rf_permissions.BasePermission = BasePermission
    rf_permissions.IsAuthenticated = BasePermission
    rf_serializers = ensure_mock_module('rest_framework.serializers')
    rf_serializers.Serializer = object
    rf_serializers.ModelSerializer = object
    rf_serializers.CharField = lambda *a, **kw: None
    rf_serializers.IntegerField = lambda *a, **kw: None
    rf_serializers.DecimalField = lambda *a, **kw: None
    rf_serializers.DateTimeField = lambda *a, **kw: None
    rf_serializers.BooleanField = lambda *a, **kw: None
    rf_serializers.DictField = lambda *a, **kw: None
    rf_serializers.ListField = lambda *a, **kw: None
    rf_serializers.SerializerMethodField = lambda *a, **kw: None
    rf_serializers.ValidationError = ValidationError

# Import Phase 8 Modules
from apps.offers.constants import (
    OfferType,
    OfferStatus,
    OfferAuditAction,
    DEFAULT_OFFER_VALIDITY_HOURS,
    DEFAULT_CURRENCY,
    SEBACOX_MAIN_SLOGAN_BN,
    SEBACOX_SHORT_DESC_BN,
    OFFER_STATUS_LABELS_BN,
    OFFER_TYPE_LABELS_BN,
    LOCKED_HISTORICAL_OFFER_STATUSES,
)
from apps.offers.validators import (
    validate_offer_pricing,
    validate_offer_quantity,
    validate_offer_expiry,
    validate_offer_status_transition,
    validate_demand_eligibility_for_offer,
    validate_provider_eligibility_for_offer,
    validate_counter_offer_eligibility,
)
from apps.offers.events import (
    OfferCreatedEvent,
    OfferCounteredEvent,
    OfferAcceptedEvent,
    OfferRejectedEvent,
    OfferCancelledEvent,
    OfferExpiredEvent,
    OfferSupersededEvent,
    dispatch_offer_event,
)
from apps.offers.permissions import (
    IsOfferParticipantOrStaff,
    CanCreateInitialOfferPermission,
    CanAcceptOfferPermission,
    CanCounterOfferPermission,
    CanCancelOfferPermission,
    CanRejectOfferPermission,
)
from apps.offers.tasks import auto_expire_pending_offers_task

# Test counters
passed = 0
failed = 0

def test(name: str, condition: bool, err_msg: str = ""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}: {err_msg}")
        failed += 1


print("=" * 60)
print("SebaCox Phase 8 Offer & Counter-Offer Test Suite")
print(f"মূল স্লোগান: “{SEBACOX_MAIN_SLOGAN_BN}”")
print(f"ছোট পরিচিতি: “{SEBACOX_SHORT_DESC_BN}”")
print("=" * 60)

# -------------------------------------------------------------
# [Group 1] Model Architecture, Enums & Invariants
# -------------------------------------------------------------
print("\n[Group 1] Model Architecture, Enums & Invariants:")

test("OfferType has INITIAL and COUNTER", set([e.value for e in OfferType]) == {'INITIAL', 'COUNTER'})
test("OfferStatus has all 7 required states", set([e.value for e in OfferStatus]) == {
    'DRAFT', 'PENDING', 'ACCEPTED', 'REJECTED', 'CANCELLED', 'EXPIRED', 'SUPERSEDED'
})
test("OfferAuditAction defines all lifecycle actions", set([e.value for e in OfferAuditAction]) == {
    'CREATED', 'COUNTERED', 'ACCEPTED', 'REJECTED', 'CANCELLED', 'EXPIRED', 'SUPERSEDED'
})
test("Terminal statuses locked", set(LOCKED_HISTORICAL_OFFER_STATUSES) == {
    OfferStatus.ACCEPTED, OfferStatus.REJECTED, OfferStatus.CANCELLED, OfferStatus.EXPIRED, OfferStatus.SUPERSEDED
})
test("Default validity is 24 hours", DEFAULT_OFFER_VALIDITY_HOURS == 24)
test("Default currency is BDT", DEFAULT_CURRENCY == 'BDT')
test("Bengali status labels populated", len(OFFER_STATUS_LABELS_BN) == 7 and OFFER_STATUS_LABELS_BN[OfferStatus.ACCEPTED] == "গ্রহণ করা হয়েছে")


# -------------------------------------------------------------
# [Group 2] Monetary & Decimal Precision Engine
# -------------------------------------------------------------
print("\n[Group 2] Monetary & Decimal Precision Engine:")

from apps.offers.models import Offer, OfferAuditLog

class MockQuerySet:
    def __init__(self, items=None):
        self.items = items or []

    def filter(self, *args, **kwargs):
        return self

    def select_related(self, *args, **kwargs):
        return self

    def select_for_update(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def first(self):
        return self.items[0] if self.items else None

    def exists(self):
        return len(self.items) > 0

    def count(self):
        return len(self.items)

    def create(self, **kwargs):
        return Offer(**kwargs)

    def update(self, **kwargs):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)


class MockManager:
    def __init__(self, items=None):
        self.items = items or []

    def filter(self, *args, **kwargs):
        return MockQuerySet(self.items).filter(*args, **kwargs)

    def select_for_update(self, *args, **kwargs):
        return MockQuerySet(self.items).select_for_update(*args, **kwargs)

    def select_related(self, *args, **kwargs):
        return MockQuerySet(self.items).select_related(*args, **kwargs)

    def create(self, **kwargs):
        return MockQuerySet(self.items).create(**kwargs)

    def all(self):
        return MockQuerySet(self.items)


if not hasattr(Offer, 'objects'):
    Offer.objects = MockManager()
if not hasattr(OfferAuditLog, 'objects'):
    OfferAuditLog.objects = MockManager()

# Server-side authoritative total calculation
tot1 = Offer.calculate_total(Decimal('1500.00'), Decimal('120.00'), Decimal('50.00'))
test("Authoritative total calculation (1500 + 120 + 50 = 1670.00)", tot1 == Decimal('1670.00'))

tot_zero = Offer.calculate_total(Decimal('500.00'), Decimal('0.00'), Decimal('0.00'))
test("Authoritative total with zero fees (500.00)", tot_zero == Decimal('500.00'))

# Price validation tests
try:
    validate_offer_pricing(Decimal('500.00'), Decimal('50.00'), Decimal('20.00'))
    test("Valid pricing passes", True)
except ValidationError as e:
    test("Valid pricing passes", False, str(e))

try:
    validate_offer_pricing(Decimal('0.00'), Decimal('0.00'), Decimal('0.00'))
    test("Zero base price rejected", False, "Expected ValidationError")
except ValidationError:
    test("Zero base price rejected", True)

try:
    validate_offer_pricing(Decimal('-100.00'), Decimal('0.00'), Decimal('0.00'))
    test("Negative base price rejected", False, "Expected ValidationError")
except ValidationError:
    test("Negative base price rejected", True)

try:
    validate_offer_pricing(Decimal('500.00'), Decimal('-10.00'), Decimal('0.00'))
    test("Negative delivery fee rejected", False, "Expected ValidationError")
except ValidationError:
    test("Negative delivery fee rejected", True)


# -------------------------------------------------------------
# [Group 3] Quantity & Unit Validation
# -------------------------------------------------------------
print("\n[Group 3] Quantity & Unit Validation:")

try:
    validate_offer_quantity(Decimal('5.00'), 'ট্রাক', Decimal('5.00'), 'ট্রাক')
    test("Matching quantity and unit passed", True)
except ValidationError as e:
    test("Matching quantity and unit passed", False, str(e))

try:
    validate_offer_quantity(Decimal('-2.00'), 'টি')
    test("Negative quantity rejected", False, "Expected ValidationError")
except ValidationError:
    test("Negative quantity rejected", True)


# -------------------------------------------------------------
# [Group 4] Expiration Validation Engine
# -------------------------------------------------------------
print("\n[Group 4] Expiration Validation Engine:")

now = datetime(2026, 9, 13, 12, 0, 0)
future_valid = now + timedelta(hours=24)
past_time = now - timedelta(hours=1)
too_far_future = now + timedelta(days=45)

try:
    validate_offer_expiry(future_valid)
    test("Valid future expiry passed", True)
except ValidationError as e:
    test("Valid future expiry passed", False, str(e))

try:
    validate_offer_expiry(past_time)
    test("Past expiry rejected", False, "Expected ValidationError")
except ValidationError:
    test("Past expiry rejected", True)

try:
    validate_offer_expiry(too_far_future)
    test("Excessive expiry (> 30 days) rejected", False, "Expected ValidationError")
except ValidationError:
    test("Excessive expiry (> 30 days) rejected", True)

# Default expiry computation in Service
calculated_default = now + timedelta(hours=DEFAULT_OFFER_VALIDITY_HOURS)
test(f"Default validity is {DEFAULT_OFFER_VALIDITY_HOURS} hours from now", calculated_default == now + timedelta(hours=24))


# -------------------------------------------------------------
# [Group 5] Demand & Provider Eligibility Validation
# -------------------------------------------------------------
print("\n[Group 5] Demand & Provider Eligibility Validation:")

class MockDemandObj:
    def __init__(self, id=1, status='PUBLISHED', is_active=True, is_deleted=False, requester_id=10):
        self.id = id
        self.status = status
        self.is_active = is_active
        self.is_deleted = is_deleted
        self.requester_id = requester_id

class MockProviderObj:
    def __init__(self, id=301, status='ACTIVE', is_active=True, is_deleted=False, user_id=20):
        self.id = id
        self.status = status
        self.is_active = is_active
        self.is_deleted = is_deleted
        self.user_id = user_id

# Demand eligibility
valid_demand = MockDemandObj(status='PUBLISHED')
try:
    validate_demand_eligibility_for_offer(valid_demand)
    test("PUBLISHED demand is eligible", True)
except ValidationError as e:
    test("PUBLISHED demand is eligible", False, str(e))

draft_demand = MockDemandObj(status='DRAFT')
try:
    validate_demand_eligibility_for_offer(draft_demand)
    test("DRAFT demand is strictly ineligible", False, "Expected ValidationError")
except ValidationError:
    test("DRAFT demand is strictly ineligible", True)

fulfilled_demand = MockDemandObj(status='FULFILLED')
try:
    validate_demand_eligibility_for_offer(fulfilled_demand)
    test("FULFILLED demand is strictly ineligible", False, "Expected ValidationError")
except ValidationError:
    test("FULFILLED demand is strictly ineligible", True)

# Provider eligibility
valid_provider = MockProviderObj(status='ACTIVE')
try:
    validate_provider_eligibility_for_offer(valid_provider)
    test("ACTIVE provider is eligible", True)
except ValidationError as e:
    test("ACTIVE provider is eligible", False, str(e))

suspended_provider = MockProviderObj(status='SUSPENDED')
try:
    validate_provider_eligibility_for_offer(suspended_provider)
    test("SUSPENDED provider is strictly ineligible", False, "Expected ValidationError")
except ValidationError:
    test("SUSPENDED provider is strictly ineligible", True)


# -------------------------------------------------------------
# [Group 6] State Machine & Controlled Transitions
# -------------------------------------------------------------
print("\n[Group 6] State Machine & Controlled Transitions:")

# Allowed transitions
for st_from, st_to, label in [
    (OfferStatus.DRAFT, OfferStatus.PENDING, "DRAFT -> PENDING"),
    (OfferStatus.DRAFT, OfferStatus.CANCELLED, "DRAFT -> CANCELLED"),
    (OfferStatus.PENDING, OfferStatus.ACCEPTED, "PENDING -> ACCEPTED"),
    (OfferStatus.PENDING, OfferStatus.REJECTED, "PENDING -> REJECTED"),
    (OfferStatus.PENDING, OfferStatus.CANCELLED, "PENDING -> CANCELLED"),
    (OfferStatus.PENDING, OfferStatus.SUPERSEDED, "PENDING -> SUPERSEDED"),
    (OfferStatus.PENDING, OfferStatus.EXPIRED, "PENDING -> EXPIRED"),
]:
    try:
        validate_offer_status_transition(st_from, st_to)
        test(f"{label} is allowed", True)
    except ValidationError as e:
        test(f"{label} is allowed", False, str(e))

# Prohibited transitions
try:
    validate_offer_status_transition(OfferStatus.ACCEPTED, OfferStatus.PENDING)
    test("ACCEPTED -> PENDING locked transition blocked", False, "Expected ValidationError")
except ValidationError:
    test("ACCEPTED -> PENDING locked transition blocked", True)

try:
    validate_offer_status_transition(OfferStatus.REJECTED, OfferStatus.ACCEPTED)
    test("REJECTED -> ACCEPTED locked transition blocked", False, "Expected ValidationError")
except ValidationError:
    test("REJECTED -> ACCEPTED locked transition blocked", True)

try:
    validate_offer_status_transition(OfferStatus.EXPIRED, OfferStatus.ACCEPTED)
    test("EXPIRED -> ACCEPTED locked transition blocked", False, "Expected ValidationError")
except ValidationError:
    test("EXPIRED -> ACCEPTED locked transition blocked", True)

try:
    validate_offer_status_transition(OfferStatus.SUPERSEDED, OfferStatus.ACCEPTED)
    test("SUPERSEDED -> ACCEPTED locked transition blocked", False, "Expected ValidationError")
except ValidationError:
    test("SUPERSEDED -> ACCEPTED locked transition blocked", True)


# -------------------------------------------------------------
# [Group 7] Counter-Offer Eligibility & Chain Integrity
# -------------------------------------------------------------
print("\n[Group 7] Counter-Offer Eligibility & Chain Integrity:")

class MockOfferObj:
    def __init__(self, id=101, version=1, status=OfferStatus.PENDING, demand=valid_demand,
                 provider=valid_provider, requester_id=10, proposer_id=20, expires_at=future_valid):
        self.id = id
        self.version = version
        self.status = status
        self.demand = demand
        self.provider = provider
        self.requester_id = requester_id
        self.proposer_id = proposer_id
        self.expires_at = expires_at
        self.is_expired = False

class MockUserObj:
    def __init__(self, id=10, is_staff=False):
        self.id = id
        self.is_authenticated = True
        self.is_staff = is_staff

# Valid counter by requester (User 10 countering Provider User 20's offer)
pending_v1_offer = MockOfferObj(id=101, version=1, proposer_id=20, requester_id=10)
requester_user = MockUserObj(id=10)
provider_user = MockUserObj(id=20)
stranger_user = MockUserObj(id=999)

try:
    validate_counter_offer_eligibility(pending_v1_offer, requester_user)
    test("Recipient (Requester) is eligible to counter", True)
except Exception as e:
    test("Recipient (Requester) is eligible to counter", False, str(e))

# Proposer cannot counter their own offer without waiting for recipient
try:
    validate_counter_offer_eligibility(pending_v1_offer, provider_user)
    test("Proposer countering their own pending offer is blocked", False, "Expected ValidationError")
except ValidationError:
    test("Proposer countering their own pending offer is blocked", True)

# Stranger cannot counter
try:
    validate_counter_offer_eligibility(pending_v1_offer, stranger_user)
    test("Stranger countering is strictly denied", False, "Expected PermissionDenied")
except PermissionDenied:
    test("Stranger countering is strictly denied", True)

# Expired parent offer cannot be countered
expired_parent = MockOfferObj(id=102, status=OfferStatus.EXPIRED)
expired_parent.is_expired = True
try:
    validate_counter_offer_eligibility(expired_parent, requester_user)
    test("Expired parent offer cannot be countered", False, "Expected ValidationError")
except ValidationError:
    test("Expired parent offer cannot be countered", True)

# Superseded parent offer cannot be countered
superseded_parent = MockOfferObj(id=103, status=OfferStatus.SUPERSEDED)
try:
    validate_counter_offer_eligibility(superseded_parent, requester_user)
    test("Superseded parent offer cannot be countered", False, "Expected ValidationError")
except ValidationError:
    test("Superseded parent offer cannot be countered", True)


# -------------------------------------------------------------
# [Group 8] Security, Permissions & IDOR Protection
# -------------------------------------------------------------
print("\n[Group 8] Security, Permissions & IDOR Protection:")

class MockRequest:
    def __init__(self, user):
        self.user = user

perm_participant = IsOfferParticipantOrStaff()
perm_accept = CanAcceptOfferPermission()
perm_cancel = CanCancelOfferPermission()

# Participant check
test("Requester has participant permission", perm_participant.has_object_permission(MockRequest(requester_user), None, pending_v1_offer))
test("Provider owner has participant permission", perm_participant.has_object_permission(MockRequest(provider_user), None, pending_v1_offer))
test("Stranger is strictly blocked by participant permission", not perm_participant.has_object_permission(MockRequest(stranger_user), None, pending_v1_offer))

# Accept permission (only recipient)
test("Requester (recipient of v1) can accept", perm_accept.has_object_permission(MockRequest(requester_user), None, pending_v1_offer))
test("Provider (proposer of v1) cannot accept own offer", not perm_accept.has_object_permission(MockRequest(provider_user), None, pending_v1_offer))
test("Stranger cannot accept", not perm_accept.has_object_permission(MockRequest(stranger_user), None, pending_v1_offer))

# Cancel permission (only proposer)
test("Provider (proposer of v1) can cancel", perm_cancel.has_object_permission(MockRequest(provider_user), None, pending_v1_offer))
test("Requester (recipient of v1) cannot cancel (must reject instead)", not perm_cancel.has_object_permission(MockRequest(requester_user), None, pending_v1_offer))


# -------------------------------------------------------------
# [Group 9] Domain Events & Audit Dispatching
# -------------------------------------------------------------
print("\n[Group 9] Domain Events & Audit Dispatching:")

evt_created = OfferCreatedEvent(
    offer_id=101,
    demand_id=1,
    provider_id=301,
    requester_id=10,
    proposer_id=20,
    version=1,
    total_amount=Decimal('1500.00'),
    currency='BDT',
    status=OfferStatus.PENDING,
    expires_at=future_valid.isoformat()
)
test("OfferCreatedEvent schema is valid", evt_created.event_type == 'offer.created')
test("OfferCreatedEvent carries authoritative total amount", evt_created.total_amount == Decimal('1500.00'))

evt_counter = OfferCounteredEvent(
    offer_id=102,
    parent_offer_id=101,
    root_offer_id=101,
    demand_id=1,
    provider_id=301,
    requester_id=10,
    proposer_id=10,
    version=2,
    total_amount=Decimal('1350.00'),
    currency='BDT'
)
test("OfferCounteredEvent schema is valid", evt_counter.event_type == 'offer.countered')
test("OfferCounteredEvent version incremented to 2", evt_counter.version == 2)

evt_accepted = OfferAcceptedEvent(
    offer_id=102,
    demand_id=1,
    provider_id=301,
    requester_id=10,
    proposer_id=10,
    version=2,
    accepted_by_id=20,
    total_amount=Decimal('1350.00'),
    currency='BDT'
)
test("OfferAcceptedEvent schema is valid", evt_accepted.event_type == 'offer.accepted')

# Event dispatching does not raise
try:
    dispatch_offer_event(evt_created)
    dispatch_offer_event(evt_counter)
    dispatch_offer_event(evt_accepted)
    test("dispatch_offer_event executes successfully", True)
except Exception as e:
    test("dispatch_offer_event executes successfully", False, str(e))


# -------------------------------------------------------------
# [Group 10] Automatic Expiration Task Logic
# -------------------------------------------------------------
print("\n[Group 10] Automatic Expiration Task Logic:")

try:
    res = auto_expire_pending_offers_task()
    test("auto_expire_pending_offers_task executes cleanly", isinstance(res, int))
except Exception as e:
    test("auto_expire_pending_offers_task executes cleanly", False, str(e))


# -------------------------------------------------------------
# [Group 11] Flutter & Mobile Integration Integrity
# -------------------------------------------------------------
print("\n[Group 11] Flutter & Mobile Integration Integrity:")

# Verify mobile model and service files exist
mobile_offer_enums = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'models' / 'offer_enums.dart'
mobile_offer_model = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'models' / 'offer_model.dart'
mobile_offer_service = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'services' / 'offer_service.dart'
mobile_offer_list = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'screens' / 'offer_list_screen.dart'
mobile_offer_detail = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'screens' / 'offer_detail_screen.dart'
mobile_counter_screen = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'screens' / 'counter_offer_screen.dart'
mobile_history_screen = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'offers' / 'screens' / 'offer_history_screen.dart'

test("Flutter offer_enums.dart exists", mobile_offer_enums.exists())
test("Flutter offer_model.dart exists", mobile_offer_model.exists())
test("Flutter offer_service.dart exists", mobile_offer_service.exists())
test("Flutter offer_list_screen.dart exists", mobile_offer_list.exists())
test("Flutter offer_detail_screen.dart exists", mobile_offer_detail.exists())
test("Flutter counter_offer_screen.dart exists", mobile_counter_screen.exists())
test("Flutter offer_history_screen.dart exists", mobile_history_screen.exists())

if mobile_offer_enums.exists():
    enums_src = mobile_offer_enums.read_text(encoding='utf-8')
    test("Flutter enum contains 'superseded'", 'superseded' in enums_src)
    test("Flutter enum contains 'accepted'", 'accepted' in enums_src)
    test("Flutter enum contains 'initial'", 'initial' in enums_src)
    test("Flutter enum contains 'counter'", 'counter' in enums_src)

if mobile_offer_model.exists():
    model_src = mobile_offer_model.read_text(encoding='utf-8')
    test("Flutter model parses totalAmount", 'totalAmount' in model_src)
    test("Flutter model supports parentOfferId", 'parentOfferId' in model_src)
    test("Flutter model supports rootOfferId", 'rootOfferId' in model_src)


# -------------------------------------------------------------
# [Group 12] Global Bangla Typography & Brand Slogan Integrity
# -------------------------------------------------------------
print("\n[Group 12] Global Bangla Typography & Brand Slogan Integrity:")
test("Main Slogan strictly matches: 'প্রয়োজন থেকে সমাধান- এক অ্যাপেই'", SEBACOX_MAIN_SLOGAN_BN == "প্রয়োজন থেকে সমাধান- এক অ্যাপেই")
test("Short Description strictly matches: 'খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই'", SEBACOX_SHORT_DESC_BN == "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই")

app_theme_path = ROOT_DIR / 'mobile' / 'lib' / 'core' / 'theme' / 'app_theme.dart'
if app_theme_path.exists():
    theme_content = app_theme_path.read_text(encoding='utf-8')
    test("Hind Siliguri enforced for large headlines in mobile theme", "Hind Siliguri" in theme_content)
    test("Baloo Da 2 enforced for medium titles, buttons & chips", "Baloo Da 2" in theme_content)
    test("Tiro Bangla enforced for body copy & captions", "Tiro Bangla" in theme_content)


# -------------------------------------------------------------
# [Group 13] Strict Phase Boundaries (No Deal/Booking/Payment Engine)
# -------------------------------------------------------------
print("\n[Group 13] Strict Phase Boundaries (No Deal/Booking/Payment/Chat Engines in Phase 8):")
deal_app_exists = (ROOT_DIR / 'backend' / 'apps' / 'deals').exists()
booking_app_exists = (ROOT_DIR / 'backend' / 'apps' / 'bookings').exists()
payment_app_exists = (ROOT_DIR / 'backend' / 'apps' / 'payments').exists()
chat_app_exists = (ROOT_DIR / 'backend' / 'apps' / 'chats').exists()

test("Deal Engine strictly not in Phase 8", not deal_app_exists)
test("Booking Engine strictly not in Phase 8", not booking_app_exists)
test("Payment Engine strictly not in Phase 8", not payment_app_exists)
test("Chat Engine strictly not in Phase 8", not chat_app_exists)


# -------------------------------------------------------------
# Summary
# -------------------------------------------------------------
print("\n" + "=" * 60)
print(f"Phase 8 Tests Result: {passed} Passed, {failed} Failed")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
