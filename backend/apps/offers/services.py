"""
Offer Engine Services for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import logging
from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone

from .constants import (
    OfferType,
    OfferStatus,
    OfferAuditAction,
    DEFAULT_OFFER_VALIDITY_HOURS,
    DEFAULT_CURRENCY,
    OFFER_STATUS_LABELS_BN,
)
from .models import Offer, OfferAuditLog
from .validators import (
    validate_offer_status_transition,
    validate_offer_pricing,
    validate_offer_quantity,
    validate_offer_expiry,
    validate_demand_eligibility_for_offer,
    validate_provider_eligibility_for_offer,
    validate_counter_offer_eligibility,
)
from .events import (
    OfferCreatedEvent,
    OfferCounteredEvent,
    OfferAcceptedEvent,
    OfferRejectedEvent,
    OfferCancelledEvent,
    OfferExpiredEvent,
    OfferSupersededEvent,
    dispatch_offer_event,
)
from apps.demands.models import Demand
from apps.providers.models import Provider
from apps.matching.models import MatchCandidate

logger = logging.getLogger(__name__)


class OfferService:
    """
    Authoritative Orchestrator for Offer Lifecycle, Counter-Offers, and Expiration.
    """

    @classmethod
    @transaction.atomic
    def create_initial_offer(
        cls,
        demand_id: int,
        provider_id: int,
        proposer_user,
        price: Decimal,
        title_bn: str,
        delivery_fee: Decimal = Decimal('0.00'),
        service_fee: Decimal = Decimal('0.00'),
        description_bn: str = '',
        quantity: Decimal = None,
        unit: str = '',
        terms_bn: str = '',
        estimated_delivery_duration: str = '',
        expires_at = None,
        match_candidate_id: int = None,
        currency: str = DEFAULT_CURRENCY,
    ) -> Offer:
        """
        Creates an INITIAL Offer from an Eligible Provider to a Demand Requester.
        """
        # 1. Resolve & validate Demand
        demand = Demand.objects.filter(id=demand_id).select_related('requester', 'service', 'category').first()
        if not demand:
            raise ValidationError(f"প্রয়োজন (Demand #{demand_id}) খুঁজে পাওয়া যায়নি।")

        validate_demand_eligibility_for_offer(demand)

        # 2. Resolve & validate Provider
        provider = Provider.objects.filter(id=provider_id).select_related('user').first()
        if not provider:
            raise ValidationError(f"সেবাদাতা (Provider #{provider_id}) খুঁজে পাওয়া যায়নি।")

        validate_provider_eligibility_for_offer(provider)

        # Ensure proposer owns or represents the provider
        if provider.user_id != proposer_user.id and not getattr(proposer_user, 'is_staff', False):
            raise PermissionDenied("আপনি এই সেবাদাতা অ্যাকাউন্টের পক্ষ থেকে প্রস্তাব পাঠানোর অধিকারী নন।")

        # Demand requester cannot propose an initial offer to their own demand
        if demand.requester_id == proposer_user.id:
            raise ValidationError("আপনি নিজের প্রয়োজনের বিপরীতে সেবাদাতা হিসেবে প্রাথমিক প্রস্তাব দিতে পারেন না।")

        # 3. Match candidate context (Optional but verified if provided)
        match_candidate = None
        if match_candidate_id:
            match_candidate = MatchCandidate.objects.filter(
                id=match_candidate_id,
                demand_id=demand_id,
                provider_id=provider_id
            ).first()
            if not match_candidate:
                raise ValidationError("প্রদত্ত ম্যাচিং ক্যান্ডিডেট রেফারেন্সটি সঠিক নয়।")

        # 4. Quantity and Unit validations
        validate_offer_quantity(
            quantity=quantity,
            unit=unit,
            demand_quantity=getattr(demand, 'quantity', None),
            demand_unit=getattr(demand, 'unit', '')
        )

        # 5. Price & fees validations
        validate_offer_pricing(price, delivery_fee, service_fee)
        total_amount = Offer.calculate_total(price, delivery_fee, service_fee)

        # 6. Expiry setup
        if not expires_at:
            expires_at = timezone.now() + timedelta(hours=DEFAULT_OFFER_VALIDITY_HOURS)
        validate_offer_expiry(expires_at)

        # 7. Snapshot generation
        snapshot = {
            'demand': {
                'id': demand.id,
                'title_bn': demand.title_bn,
                'demand_type': demand.demand_type,
                'service_id': demand.service_id,
                'service_name_bn': demand.service.name_bn if demand.service else None,
                'quantity': str(demand.quantity) if demand.quantity else None,
                'unit': demand.unit,
            },
            'provider': {
                'id': provider.id,
                'business_name_bn': provider.business_name_bn,
                'is_verified': provider.is_verified,
            }
        }

        # 8. Persistence
        offer = Offer.objects.create(
            demand=demand,
            match_candidate=match_candidate,
            provider=provider,
            requester=demand.requester,
            proposer=proposer_user,
            parent_offer=None,
            root_offer=None, # Will set to self immediately
            version=1,
            offer_type=OfferType.INITIAL,
            status=OfferStatus.PENDING,
            title_bn=title_bn,
            description_bn=description_bn,
            quantity=quantity,
            unit=unit,
            price=price,
            currency=currency,
            delivery_fee=delivery_fee,
            service_fee=service_fee,
            total_amount=total_amount,
            terms_bn=terms_bn,
            estimated_delivery_duration=estimated_delivery_duration,
            proposed_at=timezone.now(),
            expires_at=expires_at,
            snapshot=snapshot,
        )
        # Link root_offer to self
        offer.root_offer = offer
        offer.save(update_fields=['root_offer'])

        # 9. Audit Log
        OfferAuditLog.objects.create(
            offer=offer,
            actor=proposer_user,
            action=OfferAuditAction.CREATED,
            previous_status='',
            new_status=OfferStatus.PENDING,
            metadata={
                'version': 1,
                'total_amount': str(total_amount),
                'currency': currency,
            }
        )

        # 10. Dispatch Domain Event
        event = OfferCreatedEvent(
            offer_id=offer.id,
            demand_id=demand.id,
            provider_id=provider.id,
            requester_id=demand.requester_id,
            proposer_id=proposer_user.id,
            version=1,
            total_amount=str(total_amount),
            currency=currency,
            timestamp=timezone.now().isoformat(),
        )
        dispatch_offer_event(event)

        logger.info(f"Initial Offer #{offer.id} created for Demand #{demand.id} by Provider #{provider.id}")
        return offer

    @classmethod
    @transaction.atomic
    def create_counter_offer(
        cls,
        parent_offer_id: int,
        user,
        price: Decimal,
        title_bn: str = None,
        delivery_fee: Decimal = Decimal('0.00'),
        service_fee: Decimal = Decimal('0.00'),
        description_bn: str = None,
        quantity: Decimal = None,
        unit: str = None,
        terms_bn: str = None,
        estimated_delivery_duration: str = None,
        expires_at = None,
    ) -> Offer:
        """
        Creates a COUNTER-OFFER against a PENDING parent offer.
        Uses database row-locking (select_for_update) to prevent concurrency races.
        Marks parent offer as SUPERSEDED.
        """
        # 1. Lock parent offer
        parent_offer = Offer.objects.select_for_update().select_related(
            'demand', 'provider', 'requester', 'proposer', 'root_offer'
        ).filter(id=parent_offer_id).first()

        if not parent_offer:
            raise ValidationError(f"মূল প্রস্তাব (Offer #{parent_offer_id}) পাওয়া যায়নি।")

        # 2. Check Expiry
        if parent_offer.is_expired():
            # Auto-expire parent offer if expired
            parent_offer.status = OfferStatus.EXPIRED
            parent_offer.save(update_fields=['status'])
            OfferAuditLog.objects.create(
                offer=parent_offer,
                actor=None,
                action=OfferAuditAction.EXPIRED,
                previous_status=OfferStatus.PENDING,
                new_status=OfferStatus.EXPIRED,
                metadata={'reason': 'Counter attempted on expired offer'}
            )
            raise ValidationError("মূল প্রস্তাবটির মেয়াদ উত্তীর্ণ হয়ে গেছে। পাল্টা প্রস্তাব দেওয়া সম্ভব নয়।")

        # 3. Validate counter eligibility
        validate_counter_offer_eligibility(parent_offer, user)
        validate_demand_eligibility_for_offer(parent_offer.demand)
        validate_provider_eligibility_for_offer(parent_offer.provider)

        # 4. Values inheritance & fallback
        t_bn = title_bn or f"পাল্টা প্রস্তাব: {parent_offer.title_bn}"
        desc_bn = description_bn if description_bn is not None else parent_offer.description_bn
        q = quantity if quantity is not None else parent_offer.quantity
        u = unit if unit is not None else parent_offer.unit
        t_terms = terms_bn if terms_bn is not None else parent_offer.terms_bn
        est_duration = estimated_delivery_duration if estimated_delivery_duration is not None else parent_offer.estimated_delivery_duration

        # 5. Price & fee validations
        validate_offer_pricing(price, delivery_fee, service_fee)
        total_amount = Offer.calculate_total(price, delivery_fee, service_fee)

        # 6. Expiry for counter offer
        if not expires_at:
            expires_at = timezone.now() + timedelta(hours=DEFAULT_OFFER_VALIDITY_HOURS)
        validate_offer_expiry(expires_at)

        # 7. Next version calculation & Root reference
        root_offer = parent_offer.root_offer or parent_offer
        next_version = parent_offer.version + 1

        # 8. Mark parent offer as SUPERSEDED
        prev_parent_status = parent_offer.status
        parent_offer.status = OfferStatus.SUPERSEDED
        parent_offer.save(update_fields=['status', 'updated_at'])

        OfferAuditLog.objects.create(
            offer=parent_offer,
            actor=user,
            action=OfferAuditAction.SUPERSEDED,
            previous_status=prev_parent_status,
            new_status=OfferStatus.SUPERSEDED,
            metadata={
                'superseded_by_version': next_version,
                'actor_id': user.id,
            }
        )

        dispatch_offer_event(OfferSupersededEvent(
            offer_id=parent_offer.id,
            demand_id=parent_offer.demand_id,
            provider_id=parent_offer.provider_id,
            requester_id=parent_offer.requester_id,
            proposer_id=parent_offer.proposer_id,
            version=parent_offer.version,
            total_amount=str(parent_offer.total_amount),
            currency=parent_offer.currency,
            timestamp=timezone.now().isoformat(),
            superseded_by_offer_id=0, # updated after create
        ))

        # 9. Create Counter Offer
        counter_offer = Offer.objects.create(
            demand=parent_offer.demand,
            match_candidate=parent_offer.match_candidate,
            provider=parent_offer.provider,
            requester=parent_offer.requester,
            proposer=user,
            parent_offer=parent_offer,
            root_offer=root_offer,
            version=next_version,
            offer_type=OfferType.COUNTER,
            status=OfferStatus.PENDING,
            title_bn=t_bn,
            description_bn=desc_bn,
            quantity=q,
            unit=u,
            price=price,
            currency=parent_offer.currency,
            delivery_fee=delivery_fee,
            service_fee=service_fee,
            total_amount=total_amount,
            terms_bn=t_terms,
            estimated_delivery_duration=est_duration,
            proposed_at=timezone.now(),
            expires_at=expires_at,
            snapshot=parent_offer.snapshot,
        )

        # 10. Audit log for counter offer
        OfferAuditLog.objects.create(
            offer=counter_offer,
            actor=user,
            action=OfferAuditAction.COUNTERED,
            previous_status='',
            new_status=OfferStatus.PENDING,
            metadata={
                'parent_offer_id': parent_offer.id,
                'version': next_version,
                'total_amount': str(total_amount),
            }
        )

        # 11. Dispatch Domain Event
        dispatch_offer_event(OfferCounteredEvent(
            offer_id=counter_offer.id,
            demand_id=counter_offer.demand_id,
            provider_id=counter_offer.provider_id,
            requester_id=counter_offer.requester_id,
            proposer_id=user.id,
            version=next_version,
            total_amount=str(total_amount),
            currency=counter_offer.currency,
            timestamp=timezone.now().isoformat(),
            parent_offer_id=parent_offer.id,
        ))

        logger.info(f"Counter Offer #{counter_offer.id} (v{next_version}) created for Demand #{counter_offer.demand_id} by User #{user.id}")
        return counter_offer

    @classmethod
    @transaction.atomic
    def accept_offer(cls, offer_id: int, user) -> Offer:
        """
        Accepts a PENDING Offer.
        Enforces:
        - Row-level lock on the Offer and Demand
        - Non-proposer (recipient) authorization
        - One Accepted Offer Rule: No concurrent/multiple accepted offers for same Demand
        - Non-expired status
        - Accepted Offer != Deal (Domain event published for future phase)
        """
        offer = Offer.objects.select_for_update().select_related(
            'demand', 'provider', 'requester', 'proposer'
        ).filter(id=offer_id).first()

        if not offer:
            raise ValidationError(f"প্রস্তাব (Offer #{offer_id}) খুঁজে পাওয়া যায়নি।")

        # Check terminal state
        if offer.status == OfferStatus.ACCEPTED:
            return offer # Idempotent acceptance return

        validate_offer_status_transition(offer.status, OfferStatus.ACCEPTED)

        # Expiry check
        if offer.is_expired():
            offer.status = OfferStatus.EXPIRED
            offer.save(update_fields=['status'])
            OfferAuditLog.objects.create(
                offer=offer,
                actor=user,
                action=OfferAuditAction.EXPIRED,
                previous_status=OfferStatus.PENDING,
                new_status=OfferStatus.EXPIRED,
                metadata={'reason': 'Acceptance attempted on expired offer'}
            )
            raise ValidationError("প্রস্তাবটির মেয়াদ উত্তীর্ণ হয়ে গেছে। এটি গ্রহণ করা যাবে না।")

        # Authorization: Only the receiving party can accept, NOT the proposer
        requester_user_id = offer.requester_id
        provider_user_id = offer.provider.user_id if hasattr(offer.provider, 'user') else None

        if user.id not in (requester_user_id, provider_user_id) and not getattr(user, 'is_staff', False):
            raise PermissionDenied("আপনি এই প্রস্তাবটি গ্রহণ করার অধিকারী নন।")

        if user.id == offer.proposer_id and not getattr(user, 'is_staff', False):
            raise ValidationError("আপনি নিজের দেওয়া প্রস্তাব নিজে গ্রহণ করতে পারবেন না। অপর পক্ষের সম্মতি প্রয়োজন।")

        # ONE ACCEPTED OFFER RULE:
        # Lock Demand row to serialize concurrent accept attempts across competing providers
        Demand.objects.select_for_update().filter(id=offer.demand_id).exists()

        existing_accepted = Offer.objects.filter(
            demand_id=offer.demand_id,
            status=OfferStatus.ACCEPTED
        ).exclude(id=offer.id).first()

        if existing_accepted:
            raise ValidationError(
                f"এই প্রয়োজনের জন্য ইতোমধ্যে অন্য একটি প্রস্তাব (Offer #{existing_accepted.id}) গ্রহণ করা হয়েছে।"
            )

        # Transition to ACCEPTED
        prev_status = offer.status
        offer.status = OfferStatus.ACCEPTED
        offer.accepted_at = timezone.now()
        offer.save(update_fields=['status', 'accepted_at', 'updated_at'])

        # Audit Log
        OfferAuditLog.objects.create(
            offer=offer,
            actor=user,
            action=OfferAuditAction.ACCEPTED,
            previous_status=prev_status,
            new_status=OfferStatus.ACCEPTED,
            metadata={'accepted_by_user_id': user.id}
        )

        # Dispatch Domain Event (input for future Deal Engine)
        dispatch_offer_event(OfferAcceptedEvent(
            offer_id=offer.id,
            demand_id=offer.demand_id,
            provider_id=offer.provider_id,
            requester_id=offer.requester_id,
            proposer_id=offer.proposer_id,
            version=offer.version,
            total_amount=str(offer.total_amount),
            currency=offer.currency,
            timestamp=timezone.now().isoformat(),
        ))

        logger.info(f"Offer #{offer.id} ACCEPTED by User #{user.id} for Demand #{offer.demand_id}")
        return offer

    @classmethod
    @transaction.atomic
    def reject_offer(cls, offer_id: int, user, rejection_reason_bn: str = '') -> Offer:
        """
        Rejects a PENDING Offer.
        Only the receiving party (or staff) can reject.
        """
        offer = Offer.objects.select_for_update().select_related(
            'demand', 'provider', 'requester', 'proposer'
        ).filter(id=offer_id).first()

        if not offer:
            raise ValidationError(f"প্রস্তাব (Offer #{offer_id}) খুঁজে পাওয়া যায়নি।")

        if offer.status == OfferStatus.REJECTED:
            return offer # Idempotent

        validate_offer_status_transition(offer.status, OfferStatus.REJECTED)

        # Authorization: Recipient or staff
        requester_user_id = offer.requester_id
        provider_user_id = offer.provider.user_id if hasattr(offer.provider, 'user') else None

        if user.id not in (requester_user_id, provider_user_id) and not getattr(user, 'is_staff', False):
            raise PermissionDenied("আপনি এই প্রস্তাবটি প্রত্যাখ্যান করার অধিকারী নন।")

        if user.id == offer.proposer_id and not getattr(user, 'is_staff', False):
            raise ValidationError("নিজের দেওয়া প্রস্তাব প্রত্যাখ্যান নয়, 'বাতিল' (Cancel) করতে পারেন।")

        prev_status = offer.status
        offer.status = OfferStatus.REJECTED
        offer.rejected_at = timezone.now()
        offer.rejection_reason_bn = rejection_reason_bn
        offer.save(update_fields=['status', 'rejected_at', 'rejection_reason_bn', 'updated_at'])

        OfferAuditLog.objects.create(
            offer=offer,
            actor=user,
            action=OfferAuditAction.REJECTED,
            previous_status=prev_status,
            new_status=OfferStatus.REJECTED,
            metadata={
                'rejected_by_user_id': user.id,
                'reason': rejection_reason_bn,
            }
        )

        dispatch_offer_event(OfferRejectedEvent(
            offer_id=offer.id,
            demand_id=offer.demand_id,
            provider_id=offer.provider_id,
            requester_id=offer.requester_id,
            proposer_id=offer.proposer_id,
            version=offer.version,
            total_amount=str(offer.total_amount),
            currency=offer.currency,
            timestamp=timezone.now().isoformat(),
            rejection_reason_bn=rejection_reason_bn,
        ))

        logger.info(f"Offer #{offer.id} REJECTED by User #{user.id}")
        return offer

    @classmethod
    @transaction.atomic
    def cancel_offer(cls, offer_id: int, user, cancellation_reason_bn: str = '') -> Offer:
        """
        Cancels a PENDING (or DRAFT) Offer by the proposer.
        """
        offer = Offer.objects.select_for_update().select_related(
            'demand', 'provider', 'requester', 'proposer'
        ).filter(id=offer_id).first()

        if not offer:
            raise ValidationError(f"প্রস্তাব (Offer #{offer_id}) খুঁজে পাওয়া যায়নি।")

        if offer.status == OfferStatus.CANCELLED:
            return offer # Idempotent

        validate_offer_status_transition(offer.status, OfferStatus.CANCELLED)

        # Authorization: Only proposer or staff
        if user.id != offer.proposer_id and not getattr(user, 'is_staff', False):
            raise PermissionDenied("শুধুমাত্র প্রস্তাব প্রদানকারী নিজের প্রস্তাব বাতিল করতে পারেন।")

        prev_status = offer.status
        offer.status = OfferStatus.CANCELLED
        offer.cancelled_at = timezone.now()
        offer.cancellation_reason_bn = cancellation_reason_bn
        offer.save(update_fields=['status', 'cancelled_at', 'cancellation_reason_bn', 'updated_at'])

        OfferAuditLog.objects.create(
            offer=offer,
            actor=user,
            action=OfferAuditAction.CANCELLED,
            previous_status=prev_status,
            new_status=OfferStatus.CANCELLED,
            metadata={
                'cancelled_by_user_id': user.id,
                'reason': cancellation_reason_bn,
            }
        )

        dispatch_offer_event(OfferCancelledEvent(
            offer_id=offer.id,
            demand_id=offer.demand_id,
            provider_id=offer.provider_id,
            requester_id=offer.requester_id,
            proposer_id=offer.proposer_id,
            version=offer.version,
            total_amount=str(offer.total_amount),
            currency=offer.currency,
            timestamp=timezone.now().isoformat(),
            cancellation_reason_bn=cancellation_reason_bn,
        ))

        logger.info(f"Offer #{offer.id} CANCELLED by User #{user.id}")
        return offer

    @classmethod
    @transaction.atomic
    def expire_pending_offers(cls) -> int:
        """
        Scans for PENDING offers past their expires_at and transitions them to EXPIRED.
        Idempotent periodic processor. Returns count of expired offers.
        """
        now = timezone.now()
        expired_qs = Offer.objects.select_for_update().filter(
            status=OfferStatus.PENDING,
            expires_at__lte=now
        )

        count = 0
        for offer in expired_qs:
            prev_status = offer.status
            offer.status = OfferStatus.EXPIRED
            offer.save(update_fields=['status', 'updated_at'])

            OfferAuditLog.objects.create(
                offer=offer,
                actor=None,
                action=OfferAuditAction.EXPIRED,
                previous_status=prev_status,
                new_status=OfferStatus.EXPIRED,
                metadata={'expired_at': now.isoformat()}
            )

            dispatch_offer_event(OfferExpiredEvent(
                offer_id=offer.id,
                demand_id=offer.demand_id,
                provider_id=offer.provider_id,
                requester_id=offer.requester_id,
                proposer_id=offer.proposer_id,
                version=offer.version,
                total_amount=str(offer.total_amount),
                currency=offer.currency,
                timestamp=now.isoformat(),
            ))
            count += 1

        if count > 0:
            logger.info(f"Offer expiration task: marked {count} offers as EXPIRED.")
        return count
