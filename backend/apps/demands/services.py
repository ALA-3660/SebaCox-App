"""
Domain Services for SebaCox Demand Engine.
Encapsulates state machine transitions, audit recording, validation,
and expiration management.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from typing import Optional, Dict, Any
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied

from .models import Demand, DemandAuditLog
from .constants import (
    DemandStatus,
    DemandVisibility,
    DemandContactPreference,
    DemandAuditAction,
    VALID_DEMAND_STATUS_TRANSITIONS,
    EDITABLE_DEMAND_STATUSES,
    LOCKED_HISTORICAL_STATUSES,
)
from .validators import (
    validate_demand_status_transition,
    validate_demand_for_publish,
    validate_demand_budget,
    validate_demand_quantity,
)
from .events import (
    DemandCreatedEvent,
    DemandUpdatedEvent,
    DemandPublishedEvent,
    DemandPausedEvent,
    DemandResumedEvent,
    DemandCancelledEvent,
    DemandFulfilledEvent,
    DemandExpiredEvent,
    DemandClosedEvent,
    DemandEventDispatcher,
)


def mask_phone_number(phone: Optional[str], is_authorized: bool = False) -> str:
    """
    Apply phone masking policy for privacy protection.
    Raw phone numbers are NEVER exposed to unauthenticated or unauthorized users.
    Example: +8801812345678 -> +88018****5678
    """
    if not phone:
        return ""
    if is_authorized:
        return phone

    clean_phone = phone.strip()
    if len(clean_phone) >= 11:
        prefix = clean_phone[:6]
        suffix = clean_phone[-4:]
        return f"{prefix}****{suffix}"
    return "ফোন নম্বর গোপন রাখা হয়েছে"


class DemandService:
    """
    Core Domain Service managing all business rules and operations for Demands.
    """

    @classmethod
    def record_audit(
        cls,
        demand: Demand,
        actor,
        action: str,
        from_status: str = '',
        to_status: str = '',
        message: str = '',
        metadata: Optional[Dict[str, Any]] = None
    ) -> DemandAuditLog:
        """
        Create an append-only audit trail record for this demand operation.
        """
        return DemandAuditLog.objects.create(
            demand=demand,
            actor=actor if actor and getattr(actor, 'is_authenticated', False) else None,
            action=action,
            from_status=from_status,
            to_status=to_status,
            message=message,
            metadata=metadata or {}
        )

    @classmethod
    @transaction.atomic
    def create_demand(cls, requester, data: Dict[str, Any], publish_immediately: bool = False) -> Demand:
        """
        Create a new Demand. By default saves as DRAFT unless publish_immediately is True.
        """
        if not requester or not requester.is_authenticated:
            raise PermissionDenied("প্রয়োজন পোস্ট করার জন্য লগইন আবশ্যক।")

        initial_status = DemandStatus.DRAFT
        demand = Demand(
            requester=requester,
            service_id=data.get('service_id'),
            category_id=data.get('category_id'),
            title_bn=data.get('title_bn', '').strip(),
            title_en=data.get('title_en', '').strip(),
            description_bn=data.get('description_bn', '').strip(),
            description_en=data.get('description_en', '').strip(),
            demand_type=data.get('demand_type', 'SERVICE'),
            status=initial_status,
            priority=data.get('priority', 'NORMAL'),
            quantity=data.get('quantity'),
            unit=data.get('unit', '').strip(),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            currency=data.get('currency', 'BDT'),
            required_at=data.get('required_at'),
            expires_at=data.get('expires_at'),
            district_id=data.get('district_id'),
            upazila_id=data.get('upazila_id'),
            union_id=data.get('union_id'),
            ward_id=data.get('ward_id'),
            geo_location_id=data.get('geo_location_id'),
            location_display_bn=data.get('location_display_bn', '').strip(),
            location_display_en=data.get('location_display_en', '').strip(),
            visibility=data.get('visibility', DemandVisibility.PUBLIC),
            contact_preference=data.get('contact_preference', DemandContactPreference.IN_APP_ONLY),
            is_active=True,
            is_deleted=False,
        )

        demand.clean()
        demand.save()

        # Audit creation
        cls.record_audit(
            demand=demand,
            actor=requester,
            action=DemandAuditAction.CREATED,
            from_status='',
            to_status=initial_status,
            message="নতুন প্রয়োজন খসড়া তৈরি হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandCreatedEvent(
                demand_id=demand.id,
                requester_id=requester.id,
                status=initial_status
            )
        )

        if publish_immediately:
            return cls.publish_demand(demand, requester)

        return demand

    @classmethod
    @transaction.atomic
    def update_demand(cls, demand: Demand, user, data: Dict[str, Any]) -> Demand:
        """
        Update demand fields with state-based permissions and validations.
        """
        if not demand.can_edit_by(user):
            raise PermissionDenied("এই প্রয়োজন পরিবর্তন করার অনুমতি আপনার নেই।")

        if demand.status in LOCKED_HISTORICAL_STATUSES:
            raise ValidationError("সম্পন্ন, বাতিল বা বন্ধ হওয়া প্রয়োজন পরিবর্তন করা সম্ভব নয়।")

        # Allow updating editable fields
        updatable_fields = [
            'service_id', 'category_id', 'title_bn', 'title_en',
            'description_bn', 'description_en', 'demand_type', 'priority',
            'quantity', 'unit', 'budget_min', 'budget_max', 'currency',
            'required_at', 'expires_at', 'district_id', 'upazila_id',
            'union_id', 'ward_id', 'geo_location_id', 'location_display_bn',
            'location_display_en', 'visibility', 'contact_preference',
        ]

        changed_fields = []
        for field in updatable_fields:
            if field in data:
                old_val = getattr(demand, field, None)
                new_val = data[field]
                if old_val != new_val:
                    setattr(demand, field, new_val)
                    changed_fields.append(field)

        demand.clean()

        # If currently published, ensure modifications still satisfy publish criteria
        if demand.status == DemandStatus.PUBLISHED:
            validate_demand_for_publish(
                title_bn=demand.title_bn,
                description_bn=demand.description_bn,
                expires_at=demand.expires_at,
                budget_min=demand.budget_min,
                budget_max=demand.budget_max,
                quantity=demand.quantity,
                unit=demand.unit,
                upazila_id=demand.upazila_id,
                district_id=demand.district_id,
                location_display_bn=demand.location_display_bn,
            )

        demand.save()

        if changed_fields:
            cls.record_audit(
                demand=demand,
                actor=user,
                action=DemandAuditAction.UPDATED,
                from_status=demand.status,
                to_status=demand.status,
                message=f"প্রয়োজনের তথ্য আপডেট করা হয়েছে ({', '.join(changed_fields)})",
                metadata={'changed_fields': changed_fields}
            )

            DemandEventDispatcher.dispatch(
                DemandUpdatedEvent(
                    demand_id=demand.id,
                    requester_id=demand.requester_id,
                    status=demand.status,
                    metadata={'changed_fields': changed_fields}
                )
            )

        return demand

    @classmethod
    @transaction.atomic
    def publish_demand(cls, demand: Demand, user) -> Demand:
        """
        Transition Demand from DRAFT / PAUSED to PUBLISHED.
        Enforces strict server-side validation.
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("প্রয়োজন প্রকাশ করার জন্য লগইন আবশ্যক।")

        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("শুধুমাত্র অনুরোধকারী নিজের প্রয়োজন প্রকাশ করতে পারেন।")

        validate_demand_status_transition(demand.status, DemandStatus.PUBLISHED)

        # Server-side validation for publication
        validate_demand_for_publish(
            title_bn=demand.title_bn,
            description_bn=demand.description_bn,
            expires_at=demand.expires_at,
            budget_min=demand.budget_min,
            budget_max=demand.budget_max,
            quantity=demand.quantity,
            unit=demand.unit,
            upazila_id=demand.upazila_id,
            district_id=demand.district_id,
            location_display_bn=demand.location_display_bn,
        )

        prev_status = demand.status
        demand.status = DemandStatus.PUBLISHED
        demand.published_at = timezone.now()
        demand.is_active = True
        demand.save(update_fields=['status', 'published_at', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.PUBLISHED,
            from_status=prev_status,
            to_status=DemandStatus.PUBLISHED,
            message="প্রয়োজন সফলভাবে প্রকাশ করা হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandPublishedEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.PUBLISHED
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def pause_demand(cls, demand: Demand, user, reason: str = "") -> Demand:
        """
        Temporarily pause a published demand.
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("অনুমতি নেই।")
        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("শুধুমাত্র অনুরোধকারী বা এডমিন এই প্রয়োজন সাময়িক বন্ধ করতে পারেন।")

        validate_demand_status_transition(demand.status, DemandStatus.PAUSED)

        prev_status = demand.status
        demand.status = DemandStatus.PAUSED
        demand.save(update_fields=['status', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.PAUSED,
            from_status=prev_status,
            to_status=DemandStatus.PAUSED,
            message=reason or "প্রয়োজন সাময়িক স্থগিত রাখা হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandPausedEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.PAUSED,
                metadata={'reason': reason}
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def resume_demand(cls, demand: Demand, user) -> Demand:
        """
        Resume a paused demand back to PUBLISHED.
        """
        return cls.publish_demand(demand, user)

    @classmethod
    @transaction.atomic
    def cancel_demand(cls, demand: Demand, user, reason: str = "") -> Demand:
        """
        Cancel a demand (Terminal state).
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("অনুমতি নেই।")
        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("শুধুমাত্র অনুরোধকারী বা এডমিন এই প্রয়োজন বাতিল করতে পারেন।")

        validate_demand_status_transition(demand.status, DemandStatus.CANCELLED)

        prev_status = demand.status
        demand.status = DemandStatus.CANCELLED
        demand.cancelled_at = timezone.now()
        demand.is_active = False
        demand.save(update_fields=['status', 'cancelled_at', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.CANCELLED,
            from_status=prev_status,
            to_status=DemandStatus.CANCELLED,
            message=reason or "প্রয়োজন বাতিল করা হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandCancelledEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.CANCELLED,
                metadata={'reason': reason}
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def fulfill_demand(cls, demand: Demand, user, note: str = "") -> Demand:
        """
        Mark demand as fulfilled (Requirement satisfied).
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("অনুমতি নেই।")
        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("শুধুমাত্র অনুরোধকারী বা এডমিন এই প্রয়োজন পূরণ চিহ্নিত করতে পারেন।")

        validate_demand_status_transition(demand.status, DemandStatus.FULFILLED)

        prev_status = demand.status
        demand.status = DemandStatus.FULFILLED
        demand.fulfilled_at = timezone.now()
        demand.is_active = False
        demand.save(update_fields=['status', 'fulfilled_at', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.FULFILLED,
            from_status=prev_status,
            to_status=DemandStatus.FULFILLED,
            message=note or "প্রয়োজন সফলভাবে সম্পন্ন ও পূরণ হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandFulfilledEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.FULFILLED,
                metadata={'note': note}
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def expire_demand(cls, demand: Demand, system_or_actor=None) -> Demand:
        """
        Transition published/paused demand to EXPIRED.
        """
        validate_demand_status_transition(demand.status, DemandStatus.EXPIRED)

        prev_status = demand.status
        demand.status = DemandStatus.EXPIRED
        demand.is_active = False
        demand.save(update_fields=['status', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=system_or_actor,
            action=DemandAuditAction.EXPIRED,
            from_status=prev_status,
            to_status=DemandStatus.EXPIRED,
            message="প্রয়োজনের মেয়াদ শেষ হয়ে যাওয়ায় স্বয়ংক্রিয়ভাবে স্থগিত হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandExpiredEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.EXPIRED
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def close_demand(cls, demand: Demand, user, reason: str = "") -> Demand:
        """
        Close a fulfilled or expired demand permanently.
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("অনুমতি নেই।")
        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("অনুমতি নেই।")

        validate_demand_status_transition(demand.status, DemandStatus.CLOSED)

        prev_status = demand.status
        demand.status = DemandStatus.CLOSED
        demand.closed_at = timezone.now()
        demand.is_active = False
        demand.save(update_fields=['status', 'closed_at', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.CLOSED,
            from_status=prev_status,
            to_status=DemandStatus.CLOSED,
            message=reason or "প্রয়োজন স্থায়ীভাবে বন্ধ করা হয়েছে।"
        )

        DemandEventDispatcher.dispatch(
            DemandClosedEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                status=DemandStatus.CLOSED
            )
        )

        return demand

    @classmethod
    @transaction.atomic
    def soft_delete_demand(cls, demand: Demand, user) -> Demand:
        """
        Soft-delete a demand. Retains audit and historical records.
        """
        if not user or not user.is_authenticated:
            raise PermissionDenied("অনুমতি নেই।")
        if demand.requester_id != user.id and not (user.is_staff or user.is_superuser):
            raise PermissionDenied("শুধুমাত্র মালিক নিজের প্রয়োজন আর্কাইভ বা মুছে ফেলতে পারেন।")

        demand.is_deleted = True
        demand.is_active = False
        demand.save(update_fields=['is_deleted', 'is_active', 'updated_at'])

        cls.record_audit(
            demand=demand,
            actor=user,
            action=DemandAuditAction.SOFT_DELETED,
            from_status=demand.status,
            to_status=demand.status,
            message="প্রয়োজন আর্কাইভ করা হয়েছে।"
        )

        return demand

    @classmethod
    def check_and_expire_demands(cls, queryset=None, current_time=None) -> int:
        """
        Batch expiration processor: Identifies published demands whose expires_at has passed.
        Marks them as EXPIRED and logs audit records.
        Returns count of expired demands.
        """
        now = current_time or timezone.now()
        target_qs = queryset if queryset is not None else Demand.objects.filter(
            status=DemandStatus.PUBLISHED,
            expires_at__lt=now,
            is_deleted=False
        )

        count = 0
        for d in target_qs:
            try:
                cls.expire_demand(d, system_or_actor=None)
                count += 1
            except Exception:
                pass
        return count
