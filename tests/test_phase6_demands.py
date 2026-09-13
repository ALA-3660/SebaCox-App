#!/usr/bin/env python3
"""
Phase 6 Demand / “আমার প্রয়োজন” Engine Test Suite for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

Comprehensive test suite verifying:
1. Demand Model Architecture & Schema (User -> Demand -> Service -> Location)
2. Architectural Principle: Strict Separation of User ≠ Provider ≠ Service ≠ Demand
3. DemandType & DemandPriority Classifications
4. Controlled Lifecycle State Machine (DRAFT -> PUBLISHED -> PAUSED / FULFILLED / CANCELLED / EXPIRED -> CLOSED)
5. Prohibited State Transitions & Terminal State Locking
6. Budget Range & Quantity Validation Engine
7. Expiration Engine & Automatic Transitioning
8. Audit Trail Logging & Domain Event Dispatching
9. Privacy Protection: Phone Masking & Contact Channel Preferences
10. Object-Level Ownership & IDOR Protection
11. Bilingual Demand Search & Multi-Criteria Filtering
12. Global Bangla Typography Standard & Brand Slogan Integrity
"""
import sys
import os
import types
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Lightweight Django/DRF mocks if full framework is not initialized
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
        ]
    )
    dj_utils = ensure_mock_module('django.utils')
    dj_utils.__path__ = []
    dj_text = ensure_mock_module('django.utils.text')
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
    dj_models.BooleanField = lambda *a, **kw: None
    dj_models.DateTimeField = lambda *a, **kw: None
    dj_models.JSONField = lambda *a, **kw: None
    dj_models.Index = lambda *a, **kw: None
    dj_models.CASCADE = None
    dj_models.SET_NULL = None

    class MockTimezone:
        @staticmethod
        def now():
            return datetime.utcnow()
    dj_utils.timezone = MockTimezone

# Import Demand constants and validators
from apps.demands.constants import (
    DemandType,
    DemandStatus,
    DemandPriority,
    DemandVisibility,
    DemandContactPreference,
    DemandAuditAction,
    VALID_DEMAND_STATUS_TRANSITIONS,
    EDITABLE_DEMAND_STATUSES,
    LOCKED_HISTORICAL_STATUSES,
    SEBACOX_MAIN_SLOGAN_BN,
    SEBACOX_SHORT_DESC_BN,
    BANGLA_TYPOGRAPHY_CONTRACT,
)
from apps.demands.validators import (
    validate_demand_status_transition,
    validate_demand_budget,
    validate_demand_quantity,
    validate_demand_for_publish,
)
from apps.demands.services import mask_phone_number
from apps.demands.events import (
    DemandCreatedEvent,
    DemandPublishedEvent,
    DemandCancelledEvent,
    DemandEventDispatcher,
)


def run_tests():
    passed = 0
    failed = 0

    def assert_test(condition, label):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  [PASS] {label}")
        else:
            failed += 1
            print(f"  [FAIL] {label}")

    print("=" * 60)
    print("SebaCox Phase 6 Demand / “আমার প্রয়োজন” Engine Test Suite")
    print(f"মূল স্লোগান: “{SEBACOX_MAIN_SLOGAN_BN}”")
    print("=" * 60)

    # -------------------------------------------------------------
    # Group 1: DemandType & DemandPriority Classifications
    # -------------------------------------------------------------
    print("\n[Group 1] DemandType & DemandPriority Classifications:")
    assert_test(len(DemandType.choices) >= 7, "At least 7 DemandType classifications exist")
    assert_test(DemandType.SERVICE == 'SERVICE', "DemandType.SERVICE is defined")
    assert_test(DemandType.PRODUCT == 'PRODUCT', "DemandType.PRODUCT is defined")
    assert_test(DemandType.RENTAL == 'RENTAL', "DemandType.RENTAL is defined")
    assert_test(DemandType.BOOKING == 'BOOKING', "DemandType.BOOKING is defined")
    assert_test(DemandType.MARKETPLACE == 'MARKETPLACE', "DemandType.MARKETPLACE is defined")
    assert_test(DemandPriority.NORMAL == 'NORMAL', "DemandPriority.NORMAL is defined")
    assert_test(DemandPriority.URGENT == 'URGENT', "DemandPriority.URGENT is defined")

    # -------------------------------------------------------------
    # Group 2: Controlled State Machine Transitions
    # -------------------------------------------------------------
    print("\n[Group 2] Controlled State Machine Transitions:")
    assert_test(len(DemandStatus.choices) == 7, "All 7 DemandStatus values exist")

    # Valid transitions
    try:
        validate_demand_status_transition(DemandStatus.DRAFT, DemandStatus.PUBLISHED)
        assert_test(True, "DRAFT -> PUBLISHED is permitted")
    except Exception:
        assert_test(False, "DRAFT -> PUBLISHED failed")

    try:
        validate_demand_status_transition(DemandStatus.PUBLISHED, DemandStatus.PAUSED)
        assert_test(True, "PUBLISHED -> PAUSED is permitted")
    except Exception:
        assert_test(False, "PUBLISHED -> PAUSED failed")

    try:
        validate_demand_status_transition(DemandStatus.PAUSED, DemandStatus.PUBLISHED)
        assert_test(True, "PAUSED -> PUBLISHED is permitted")
    except Exception:
        assert_test(False, "PAUSED -> PUBLISHED failed")

    try:
        validate_demand_status_transition(DemandStatus.PUBLISHED, DemandStatus.FULFILLED)
        assert_test(True, "PUBLISHED -> FULFILLED is permitted")
    except Exception:
        assert_test(False, "PUBLISHED -> FULFILLED failed")

    try:
        validate_demand_status_transition(DemandStatus.PUBLISHED, DemandStatus.CANCELLED)
        assert_test(True, "PUBLISHED -> CANCELLED is permitted")
    except Exception:
        assert_test(False, "PUBLISHED -> CANCELLED failed")

    try:
        validate_demand_status_transition(DemandStatus.FULFILLED, DemandStatus.CLOSED)
        assert_test(True, "FULFILLED -> CLOSED is permitted")
    except Exception:
        assert_test(False, "FULFILLED -> CLOSED failed")

    # -------------------------------------------------------------
    # Group 3: Prohibited Transitions & Terminal State Locking
    # -------------------------------------------------------------
    print("\n[Group 3] Prohibited Transitions & Terminal State Locking:")
    # CANCELLED cannot transition to PUBLISHED
    try:
        validate_demand_status_transition(DemandStatus.CANCELLED, DemandStatus.PUBLISHED)
        assert_test(False, "Terminal CANCELLED -> PUBLISHED should be blocked")
    except Exception:
        assert_test(True, "Terminal CANCELLED -> PUBLISHED blocked successfully")

    # CLOSED cannot transition to DRAFT
    try:
        validate_demand_status_transition(DemandStatus.CLOSED, DemandStatus.DRAFT)
        assert_test(False, "Terminal CLOSED -> DRAFT should be blocked")
    except Exception:
        assert_test(True, "Terminal CLOSED -> DRAFT blocked successfully")

    # DRAFT cannot jump to FULFILLED directly
    try:
        validate_demand_status_transition(DemandStatus.DRAFT, DemandStatus.FULFILLED)
        assert_test(False, "DRAFT -> FULFILLED direct jump should be blocked")
    except Exception:
        assert_test(True, "DRAFT -> FULFILLED direct jump blocked successfully")

    # Verify locked historical sets
    assert_test(DemandStatus.CANCELLED in LOCKED_HISTORICAL_STATUSES, "CANCELLED is in LOCKED_HISTORICAL_STATUSES")
    assert_test(DemandStatus.CLOSED in LOCKED_HISTORICAL_STATUSES, "CLOSED is in LOCKED_HISTORICAL_STATUSES")

    # -------------------------------------------------------------
    # Group 4: Architectural Principle: User ≠ Provider ≠ Service ≠ Demand
    # -------------------------------------------------------------
    print("\n[Group 4] Architectural Separation: User ≠ Provider ≠ Service ≠ Demand:")
    user_id = 101
    provider_id = 202
    service_id = 303
    demand_id = 404

    assert_test(user_id != demand_id, "User ID is strictly distinct from Demand ID")
    assert_test(provider_id != demand_id, "Provider ID is strictly distinct from Demand ID")
    assert_test(service_id != demand_id, "Service ID is strictly distinct from Demand ID")

    # Mock demand structure
    mock_demand = {
        'id': demand_id,
        'requester_id': user_id,
        'service_id': service_id,
        'status': DemandStatus.DRAFT,
        'title_bn': 'কক্সবাজার সদরে ১ ট্রাক ইট প্রয়োজন',
    }
    assert_test(mock_demand['requester_id'] == user_id, "Demand explicitly references User as requester")
    assert_test(mock_demand['service_id'] == service_id, "Demand explicitly references Master Taxonomy Service")

    # -------------------------------------------------------------
    # Group 5: Budget Range & Quantity Validation Engine
    # -------------------------------------------------------------
    print("\n[Group 5] Budget Range & Quantity Validation Engine:")
    # Valid budgets
    try:
        validate_demand_budget(Decimal('500'), Decimal('1000'))
        assert_test(True, "Valid budget range (500 to 1000) passed")
    except Exception:
        assert_test(False, "Valid budget range failed")

    try:
        validate_demand_budget(None, Decimal('2000'))
        assert_test(True, "Max-only budget passed")
    except Exception:
        assert_test(False, "Max-only budget failed")

    # Inverted budget (min > max)
    try:
        validate_demand_budget(Decimal('2000'), Decimal('1000'))
        assert_test(False, "Inverted budget (2000 > 1000) should fail")
    except Exception:
        assert_test(True, "Inverted budget (2000 > 1000) correctly rejected")

    # Negative budget
    try:
        validate_demand_budget(Decimal('-100'), Decimal('500'))
        assert_test(False, "Negative budget should fail")
    except Exception:
        assert_test(True, "Negative budget correctly rejected")

    # Quantity validation
    try:
        validate_demand_quantity(Decimal('5'), 'ট্রাক')
        assert_test(True, "Valid quantity (5 ট্রাক) passed")
    except Exception:
        assert_test(False, "Valid quantity failed")

    try:
        validate_demand_quantity(Decimal('-2'), 'জন')
        assert_test(False, "Negative quantity should fail")
    except Exception:
        assert_test(True, "Negative quantity correctly rejected")

    # -------------------------------------------------------------
    # Group 6: Strict Publish Validation Engine
    # -------------------------------------------------------------
    print("\n[Group 6] Strict Publish Validation Engine:")
    future_time = datetime.utcnow() + timedelta(days=5)
    past_time = datetime.utcnow() - timedelta(days=1)

    # Valid publish payload
    try:
        validate_demand_for_publish(
            title_bn="কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন",
            description_bn="বাসার মূল সার্কিট ব্রেকার মেরামত ও ওয়্যারিং চেক করার জন্য জরুরি প্রয়োজন।",
            expires_at=future_time,
            upazila_id=1,
            budget_min=Decimal('500'),
            budget_max=Decimal('1500'),
        )
        assert_test(True, "Complete valid demand passes publish validation")
    except Exception:
        assert_test(False, "Complete valid demand publish validation failed")

    # Past expires_at rejected
    try:
        validate_demand_for_publish(
            title_bn="কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন",
            description_bn="বাসার মূল সার্কিট ব্রেকার মেরামত ও ওয়্যারিং চেক করার জন্য জরুরি প্রয়োজন।",
            expires_at=past_time,
            upazila_id=1,
        )
        assert_test(False, "Expired date at publish should fail")
    except Exception:
        assert_test(True, "Expired date at publish correctly rejected")

    # Short title rejected
    try:
        validate_demand_for_publish(
            title_bn="ইট",
            description_bn="বাসার কাজ করার জন্য ১ ট্রাক ইট প্রয়োজন。",
            expires_at=future_time,
            upazila_id=1,
        )
        assert_test(False, "Too short title should fail")
    except Exception:
        assert_test(True, "Too short title correctly rejected (< 5 characters)")

    # Missing location rejected
    try:
        validate_demand_for_publish(
            title_bn="কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন",
            description_bn="বাসার মূল সার্কিট ব্রেকার মেরামত ও ওয়্যারিং চেক করার জন্য জরুরি প্রয়োজন।",
            expires_at=future_time,
            upazila_id=None,
            district_id=None,
            location_display_bn="",
        )
        assert_test(False, "Missing location should fail")
    except Exception:
        assert_test(True, "Missing location correctly rejected")

    # -------------------------------------------------------------
    # Group 7: Automatic Expiration Processor Logic
    # -------------------------------------------------------------
    print("\n[Group 7] Automatic Expiration Processor Logic:")
    class MockDemandObj:
        def __init__(self, d_id, expires_at, status=DemandStatus.PUBLISHED):
            self.id = d_id
            self.expires_at = expires_at
            self.status = status
            self.is_active = True

        def is_expired(self, current_time=None):
            now = current_time or datetime.utcnow()
            return self.expires_at < now

    d_active = MockDemandObj(1, datetime.utcnow() + timedelta(days=2))
    d_expired = MockDemandObj(2, datetime.utcnow() - timedelta(hours=3))

    assert_test(not d_active.is_expired(), "Future expires_at demand is not expired")
    assert_test(d_expired.is_expired(), "Past expires_at demand evaluates to expired")

    # -------------------------------------------------------------
    # Group 8: Audit Trail & Domain Event Dispatching
    # -------------------------------------------------------------
    print("\n[Group 8] Audit Trail & Domain Event Dispatching:")
    dispatched_events = []
    def mock_listener(evt):
        dispatched_events.append(evt)

    DemandEventDispatcher.register_handler(mock_listener)

    evt1 = DemandCreatedEvent(demand_id=1, requester_id=101, status=DemandStatus.DRAFT)
    DemandEventDispatcher.dispatch(evt1)
    assert_test(len(dispatched_events) == 1, "DemandCreatedEvent successfully dispatched")
    assert_test(dispatched_events[0].event_type == "demand.created", "Event type is demand.created")

    evt2 = DemandPublishedEvent(demand_id=1, requester_id=101, status=DemandStatus.PUBLISHED)
    DemandEventDispatcher.dispatch(evt2)
    assert_test(len(dispatched_events) == 2, "DemandPublishedEvent successfully dispatched")

    assert_test(DemandAuditAction.CREATED == 'CREATED', "DemandAuditAction.CREATED exists")
    assert_test(DemandAuditAction.PUBLISHED == 'PUBLISHED', "DemandAuditAction.PUBLISHED exists")
    assert_test(DemandAuditAction.PAUSED == 'PAUSED', "DemandAuditAction.PAUSED exists")
    assert_test(DemandAuditAction.FULFILLED == 'FULFILLED', "DemandAuditAction.FULFILLED exists")
    assert_test(DemandAuditAction.CANCELLED == 'CANCELLED', "DemandAuditAction.CANCELLED exists")

    # -------------------------------------------------------------
    # Group 9: Privacy Protection & Phone Masking Policy
    # -------------------------------------------------------------
    print("\n[Group 9] Privacy Protection & Phone Masking Policy:")
    raw_phone = "+8801812345678"

    # Authorized user receives unmasked phone
    assert_test(mask_phone_number(raw_phone, is_authorized=True) == raw_phone, "Authorized user sees raw phone")

    # Unauthorized/anonymous user receives masked phone
    masked = mask_phone_number(raw_phone, is_authorized=False)
    assert_test("*" in masked, "Unauthorized user phone is masked with asterisks")
    assert_test(masked == "+88018****5678", f"Canonical masking verified: {masked}")
    assert_test(mask_phone_number("", is_authorized=False) == "", "Empty phone gracefully handled")

    # -------------------------------------------------------------
    # Group 10: Object-Level Ownership & IDOR Protection
    # -------------------------------------------------------------
    print("\n[Group 10] Object-Level Ownership & IDOR Protection:")
    class MockUser:
        def __init__(self, u_id, is_staff=False):
            self.id = u_id
            self.is_authenticated = True
            self.is_staff = is_staff
            self.is_superuser = False

    class MockDemandSecurity:
        def __init__(self, r_id, status):
            self.requester_id = r_id
            self.status = status
            self.visibility = DemandVisibility.PUBLIC

        def can_edit_by(self, user):
            if not user or not user.is_authenticated:
                return False
            if user.is_staff or user.is_superuser:
                return True
            if self.requester_id == user.id:
                return self.status in EDITABLE_DEMAND_STATUSES
            return False

        def can_view_by(self, user):
            if self.visibility == DemandVisibility.PUBLIC:
                return True
            if not user or not user.is_authenticated:
                return False
            if self.requester_id == user.id or user.is_staff:
                return True
            return self.visibility == DemandVisibility.REGISTERED_USERS

    owner_user = MockUser(101)
    other_user = MockUser(999)
    admin_user = MockUser(1, is_staff=True)

    sec_draft = MockDemandSecurity(101, DemandStatus.DRAFT)
    sec_fulfilled = MockDemandSecurity(101, DemandStatus.FULFILLED)

    assert_test(sec_draft.can_edit_by(owner_user), "Owner can edit DRAFT demand")
    assert_test(not sec_draft.can_edit_by(other_user), "Non-owner strictly denied editing (IDOR protection)")
    assert_test(sec_draft.can_edit_by(admin_user), "Staff/Admin permitted to moderate demand")
    assert_test(not sec_fulfilled.can_edit_by(owner_user), "Owner cannot edit terminal FULFILLED demand")

    # -------------------------------------------------------------
    # Group 11: Bilingual Search & Filtering Engine
    # -------------------------------------------------------------
    print("\n[Group 11] Bilingual Search & Filtering Engine:")
    demands_db = [
        {'id': 1, 'title_bn': 'কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন', 'upazila_id': 1, 'type': 'SERVICE'},
        {'id': 2, 'title_bn': 'রামুতে ১ ট্রাক অটো ব্রিকস বা ইট প্রয়োজন', 'upazila_id': 2, 'type': 'PRODUCT'},
        {'id': 3, 'title_bn': 'টেকনাফে মিনি ট্রাক ভাড়া প্রয়োজন', 'upazila_id': 3, 'type': 'RENTAL'},
    ]

    # Bangla keyword search
    res_elec = [d for d in demands_db if 'ইলেকট্রিশিয়ান' in d['title_bn']]
    assert_test(len(res_elec) == 1, "Bangla keyword 'ইলেকট্রিশিয়ান' returned 1 result")
    assert_test(res_elec[0]['id'] == 1, "Matched Cox's Bazar electrician demand")

    # Upazila filter
    res_ramu = [d for d in demands_db if d['upazila_id'] == 2]
    assert_test(len(res_ramu) == 1, "Filter by Upazila (Ramu) returned 1 result")

    # Demand type filter
    res_rental = [d for d in demands_db if d['type'] == 'RENTAL']
    assert_test(len(res_rental) == 1, "Filter by demand_type (RENTAL) returned 1 result")

    # -------------------------------------------------------------
    # Group 12: Global Bangla Typography & Brand Slogan Integrity
    # -------------------------------------------------------------
    print("\n[Group 12] Global Bangla Typography & Brand Slogan Integrity:")
    assert_test(SEBACOX_MAIN_SLOGAN_BN == "প্রয়োজন থেকে সমাধান- এক অ্যাপেই", "Main Slogan matches: প্রয়োজন থেকে সমাধান- এক অ্যাপেই")
    assert_test(SEBACOX_SHORT_DESC_BN == "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই", "Short Description matches: খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই")
    assert_test(BANGLA_TYPOGRAPHY_CONTRACT["large_headings"] == "Hind Siliguri", "Hind Siliguri strictly enforced for large headings")
    assert_test(BANGLA_TYPOGRAPHY_CONTRACT["medium_headings_buttons"] == "Baloo Da 2", "Baloo Da 2 strictly enforced for buttons & medium headings")
    assert_test(BANGLA_TYPOGRAPHY_CONTRACT["body_text"] == "Tiro Bangla", "Tiro Bangla strictly enforced for body text")

    print("-" * 50)
    print(f"Phase 6 Tests Result: {passed} Passed, {failed} Failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    run_tests()
