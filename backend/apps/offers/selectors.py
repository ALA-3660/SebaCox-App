"""
Offer Selectors and Query Logic for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from typing import Optional
from django.db.models import QuerySet, Q
from django.core.exceptions import PermissionDenied, ValidationError
from .models import Offer, OfferAuditLog
from apps.demands.models import Demand
from apps.providers.models import Provider


def get_user_offers(user, status: Optional[str] = None, demand_id: Optional[int] = None, role: Optional[str] = None) -> QuerySet:
    """
    Returns list of offers visible to the authenticated user.
    - Requester: offers received for their demands
    - Provider: offers submitted by their provider profile
    - Proposer: offers proposed by this user directly
    """
    if not user or not user.is_authenticated:
        return Offer.objects.none()

    if user.is_staff:
        qs = Offer.objects.all()
    else:
        # Find user's provider profile if any
        user_provider = Provider.objects.filter(user=user).first()
        condition = Q(requester=user) | Q(proposer=user)
        if user_provider:
            condition |= Q(provider=user_provider)
        qs = Offer.objects.filter(condition)

    if status:
        qs = qs.filter(status=status)

    if demand_id:
        qs = qs.filter(demand_id=demand_id)

    if role == 'requester':
        qs = qs.filter(requester=user)
    elif role == 'provider' and not user.is_staff:
        user_provider = Provider.objects.filter(user=user).first()
        if user_provider:
            qs = qs.filter(provider=user_provider)
        else:
            return Offer.objects.none()

    return qs.select_related('demand', 'provider', 'requester', 'proposer').order_by('-created_at')


def get_demand_offers(demand_id: int, user) -> QuerySet:
    """
    Returns all offers for a specific demand, enforcing competitor isolation:
    - Requester sees all offers for their demand
    - Provider sees ONLY their own offers for this demand (anti-poaching / confidentiality)
    - Staff sees all
    """
    demand = Demand.objects.filter(id=demand_id).first()
    if not demand:
        raise ValidationError(f"প্রয়োজন (Demand #{demand_id}) পাওয়া যায়নি।")

    if user.is_staff or demand.requester_id == user.id:
        # Full visibility for demand owner and staff
        return Offer.objects.filter(demand_id=demand_id).select_related(
            'provider', 'proposer', 'parent_offer'
        ).order_by('-created_at')

    # For provider: show only their offers
    user_provider = Provider.objects.filter(user=user).first()
    if user_provider:
        return Offer.objects.filter(
            demand_id=demand_id,
            provider=user_provider
        ).select_related('provider', 'proposer', 'parent_offer').order_by('-created_at')

    # Unauthorized user
    raise PermissionDenied("এই প্রয়োজনের প্রস্তাবসমূহ দেখার অনুমতি আপনার নেই।")


def get_offer_by_id(offer_id: int, user) -> Offer:
    """
    Retrieves a single offer ensuring caller is requester, provider, or staff.
    """
    offer = Offer.objects.select_related(
        'demand', 'provider', 'requester', 'proposer', 'parent_offer', 'root_offer'
    ).filter(id=offer_id).first()

    if not offer:
        raise ValidationError(f"প্রস্তাব (Offer #{offer_id}) পাওয়া যায়নি।")

    if user.is_staff:
        return offer

    is_requester = (offer.requester_id == user.id)
    is_proposer = (offer.proposer_id == user.id)
    is_provider = False
    if hasattr(offer.provider, 'user_id') and offer.provider.user_id == user.id:
        is_provider = True

    if not (is_requester or is_proposer or is_provider):
        raise PermissionDenied("এই প্রস্তাবটি দেখার অনুমতি আপনার নেই।")

    return offer


def get_offer_chain_history(offer_id: int, user) -> QuerySet:
    """
    Retrieves the complete negotiation history chain for an offer:
    from root initial offer down to the latest counter-offer.
    """
    offer = get_offer_by_id(offer_id, user)
    root = offer.root_offer or offer

    # Fetch all offers that share this root_offer or are this root_offer
    chain = Offer.objects.filter(
        Q(id=root.id) | Q(root_offer=root)
    ).select_related('proposer', 'provider', 'requester').order_by('version', 'created_at')

    return chain


def get_offer_audit_logs(offer_id: int, user) -> QuerySet:
    """
    Retrieves audit logs for an offer.
    """
    # Verify permission first
    get_offer_by_id(offer_id, user)
    return OfferAuditLog.objects.filter(offer_id=offer_id).select_related('actor').order_by('created_at')
