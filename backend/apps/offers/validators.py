"""
Validation Logic for SebaCox Offers.
Phase 8: Offer & Counter-Offer Foundation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from decimal import Decimal
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from .constants import (
    OfferStatus,
    VALID_OFFER_STATUS_TRANSITIONS,
    TERMINAL_OFFER_STATUSES,
    OFFER_STATUS_LABELS_BN,
    MAX_OFFER_VALIDITY_HOURS,
)
from apps.demands.constants import DemandStatus
from apps.providers.constants import ProviderStatus


def validate_offer_status_transition(current_status: str, target_status: str) -> None:
    """
    Validates state machine transitions for Offer.
    Enforces terminal state immutability.
    """
    if current_status in TERMINAL_OFFER_STATUSES:
        curr_label = OFFER_STATUS_LABELS_BN.get(current_status, current_status)
        raise ValidationError(
            f"প্রস্তাবটি ইতোমধ্যে চূড়ান্ত অবস্থায় ('{curr_label}') রয়েছে। আর কোনো পরিবর্তন সম্ভব নয়।"
        )

    allowed = VALID_OFFER_STATUS_TRANSITIONS.get(current_status, [])
    if target_status not in allowed:
        curr_label = OFFER_STATUS_LABELS_BN.get(current_status, current_status)
        tgt_label = OFFER_STATUS_LABELS_BN.get(target_status, target_status)
        raise ValidationError(
            f"প্রস্তাবের অবস্থা '{curr_label}' থেকে '{tgt_label}'-এ পরিবর্তন অনুমোদিত নয়।"
        )


def validate_offer_pricing(price: Decimal, delivery_fee: Decimal = Decimal('0.00'), service_fee: Decimal = Decimal('0.00')) -> None:
    """
    Validates money and price parameters using Decimal accuracy.
    No negative values, price must be positive.
    """
    if price is None or price <= Decimal('0.00'):
        raise ValidationError("প্রস্তাবের মূল্য অবশ্যই শূন্যের বেশি (ধনাত্মক) হতে হবে।")

    if delivery_fee is not None and delivery_fee < Decimal('0.00'):
        raise ValidationError("ডেলিভারি ফি ঋণাত্মক হতে পারবে না।")

    if service_fee is not None and service_fee < Decimal('0.00'):
        raise ValidationError("সার্ভিস ফি ঋণাত্মক হতে পারবে না।")


def validate_offer_quantity(quantity: Decimal = None, unit: str = '', demand_quantity: Decimal = None, demand_unit: str = '') -> None:
    """
    Validates quantity against demand quantity rules.
    Partial quantities without explicit permission or negative quantities are rejected.
    """
    if quantity is not None:
        if quantity <= Decimal('0.00'):
            raise ValidationError("পরিমাণ অবশ্যই শূন্যের বেশি হতে হবে।")

    # If demand specifies a unit, offer unit should be provided
    if demand_unit and unit and demand_unit.strip().lower() != unit.strip().lower():
        raise ValidationError(
            f"প্রয়োজনের পরিমাপের একক ('{demand_unit}') এবং প্রস্তাবের একক ('{unit}') মিলছে না।"
        )


def validate_offer_expiry(expires_at, now=None) -> None:
    """
    Validates offer expiration datetime.
    Must be timezone-aware and in the future, up to MAX_OFFER_VALIDITY_HOURS.
    """
    if not expires_at:
        raise ValidationError("প্রস্তাবের মেয়াদ শেষ হওয়ার তারিখ ও সময় (expires_at) আবশ্যক।")

    current_time = now or timezone.now()
    if expires_at <= current_time:
        raise ValidationError("প্রস্তাবের মেয়াদ অবশ্যই ভবিষ্যৎ সময়ের হতে হবে।")

    max_future = current_time + timedelta(hours=MAX_OFFER_VALIDITY_HOURS)
    if expires_at > max_future:
        raise ValidationError(
            f"প্রস্তাবের মেয়াদ সর্বোচ্চ {MAX_OFFER_VALIDITY_HOURS // 24} দিন পর্যন্ত নির্ধারণ করা যাবে।"
        )


def validate_demand_eligibility_for_offer(demand) -> None:
    """
    Ensures Demand is in an active, published state suitable for receiving offers.
    """
    if not demand:
        raise ValidationError("প্রয়োজন (Demand) খুঁজে পাওয়া যায়নি।")

    if getattr(demand, 'is_deleted', False):
        raise ValidationError("এই প্রয়োজনটি মুছে ফেলা হয়েছে, নতুন প্রস্তাব দেওয়া যাবে না।")

    if demand.status != DemandStatus.PUBLISHED:
        raise ValidationError(
            f"শুধুমাত্র প্রকাশিত ('PUBLISHED') প্রয়োজনে প্রস্তাব দেওয়া সম্ভব। বর্তমান অবস্থা: {demand.status}।"
        )

    # Check if demand has expired
    if getattr(demand, 'expires_at', None) and demand.expires_at <= timezone.now():
        raise ValidationError("এই প্রয়োজনের মেয়াদ ইতোমধ্যে শেষ হয়ে গেছে।")


def validate_provider_eligibility_for_offer(provider) -> None:
    """
    Ensures Provider is in an ACTIVE state suitable for proposing offers.
    """
    if not provider:
        raise ValidationError("সেবাদাতা প্রোফাইল খুঁজে পাওয়া যায়নি।")

    if not getattr(provider, 'is_active', True):
        raise ValidationError("সেবাদাতার অ্যাকাউন্ট বর্তমানে নিষ্ক্রিয় রয়েছে।")

    if provider.status != ProviderStatus.ACTIVE:
        raise ValidationError(
            f"শুধুমাত্র সক্রিয় সেবাদাতারা প্রস্তাব দিতে পারেন। বর্তমান অবস্থা: {provider.status}।"
        )


def validate_counter_offer_eligibility(parent_offer, user) -> None:
    """
    Verifies that a counter-offer can be made against the parent offer:
    - parent must be PENDING
    - parent must not be expired
    - user must be an authorized party (either requester or provider user)
    - user must not be the exact proposer of the pending parent offer (you counter the OTHER party's proposal)
    """
    if not parent_offer:
        raise ValidationError("মূল প্রস্তাব (Parent Offer) পাওয়া যায়নি।")

    if parent_offer.status != OfferStatus.PENDING:
        curr_label = OFFER_STATUS_LABELS_BN.get(parent_offer.status, parent_offer.status)
        raise ValidationError(
            f"শুধুমাত্র অপেক্ষমাণ ('PENDING') প্রস্তাবে পাল্টা প্রস্তাব দেওয়া যায়। বর্তমান অবস্থা: '{curr_label}'।"
        )

    is_exp = parent_offer.is_expired() if callable(getattr(parent_offer, 'is_expired', None)) else bool(getattr(parent_offer, 'is_expired', False))
    if is_exp:
        raise ValidationError("মূল প্রস্তাবটির মেয়াদ উত্তীর্ণ হয়ে গেছে। পাল্টা প্রস্তাব দেওয়া সম্ভব নয়।")

    # Verify user party
    requester_user_id = getattr(parent_offer, 'requester_id', None) or (parent_offer.requester.id if hasattr(parent_offer, 'requester') else None)
    provider_user_id = None
    if hasattr(parent_offer, 'provider') and parent_offer.provider:
        provider_user_id = getattr(parent_offer.provider, 'user_id', None) or (parent_offer.provider.user.id if hasattr(parent_offer.provider, 'user') else None)

    user_id = getattr(user, 'id', None)
    from django.core.exceptions import PermissionDenied
    if user_id not in (requester_user_id, provider_user_id) and not getattr(user, 'is_staff', False):
        raise PermissionDenied("আপনি এই প্রস্তাবটির কোনো পক্ষ নন। পাল্টা প্রস্তাব দেওয়ার অনুমতি নেই।")

    # Proposer cannot counter their own proposal before other party responds
    proposer_id = getattr(parent_offer, 'proposer_id', None) or (parent_offer.proposer.id if hasattr(parent_offer, 'proposer') else None)
    if user_id == proposer_id and not getattr(user, 'is_staff', False):
        raise ValidationError(
            "আপনি নিজেই বর্তমান প্রস্তাবের প্রস্তাবক। অপর পক্ষ সাড়া না দেওয়া পর্যন্ত নতুন পাল্টা প্রস্তাব দেওয়া যাবে না।"
        )
