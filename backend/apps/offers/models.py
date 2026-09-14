"""
Offer Models for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from .constants import (
    OfferType,
    OfferStatus,
    OfferAuditAction,
    DEFAULT_CURRENCY,
    OFFER_STATUS_LABELS_BN,
    OFFER_TYPE_LABELS_BN,
)
from .validators import (
    validate_offer_status_transition,
    validate_offer_pricing,
    validate_offer_quantity,
    validate_offer_expiry,
    validate_demand_eligibility_for_offer,
    validate_provider_eligibility_for_offer,
)


class Offer(models.Model):
    """
    Production-ready Offer Model for SebaCox.
    Represents a structured proposal from a Provider to a Demand Requester,
    or a Counter-Offer between either party.

    Architectural Invariants:
    1. Demand -> Requester -> MatchCandidate -> Provider context verified server-side.
    2. Versioned & Immutable: Older offers in a chain are never overwritten; each counter is a new record.
    3. Superseding: An active counter-offer marks its parent PENDING offer as SUPERSEDED.
    4. One Accepted Offer Rule: Only one offer can be ACCEPTED for a Demand at a time.
    5. Accepted Offer != Deal: Accepted Offer is solely the verified precursor to future Deal Engine.
    6. Decimal Precision: All money fields strictly utilize Decimal values.
    """
    id = models.BigAutoField(primary_key=True)
    demand = models.ForeignKey(
        'demands.Demand',
        on_delete=models.CASCADE,
        related_name='offers',
        db_index=True,
        help_text="সংশ্লিষ্ট প্রয়োজন (Demand)"
    )
    match_candidate = models.ForeignKey(
        'matching.MatchCandidate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offers',
        db_index=True,
        help_text="উৎস ম্যাচিং ক্যান্ডিডেট রেফারেন্স (যদি ম্যাচিং ইঞ্জিন হতে উদ্ভূত হয়)"
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.PROTECT,
        related_name='offers',
        db_index=True,
        help_text="প্রস্তাবদাতা বা সংশ্লিষ্ট সেবাদাতা (Provider)"
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_offers',
        db_index=True,
        help_text="প্রয়োজন পোস্টকারী ব্যবহারকারী (Requester User)"
    )
    proposer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proposed_offers',
        db_index=True,
        help_text="এই নির্দিষ্ট প্রস্তাব/পাল্টা-প্রস্তাব জমাদানকারী ব্যবহারকারী"
    )
    parent_offer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='counter_offers',
        db_index=True,
        help_text="পূর্ববর্তী প্রস্তাব (Counter Offer চেইনের পূর্ববর্তী লিংক)"
    )
    root_offer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chain_offers',
        db_index=True,
        help_text="চেইনের আদি প্রস্তাব (Root Initial Offer)"
    )
    version = models.PositiveIntegerField(
        default=1,
        db_index=True,
        help_text="চেইনে প্রস্তাবের সংস্করণ নম্বর (১, ২, ৩...)"
    )
    offer_type = models.CharField(
        max_length=20,
        choices=OfferType.choices,
        default=OfferType.INITIAL,
        db_index=True,
        help_text="প্রস্তাবের ধরন (INITIAL = প্রাথমিক, COUNTER = পাল্টা প্রস্তাব)"
    )
    status = models.CharField(
        max_length=20,
        choices=OfferStatus.choices,
        default=OfferStatus.PENDING,
        db_index=True,
        help_text="অবস্থা (DRAFT, PENDING, ACCEPTED, REJECTED, CANCELLED, EXPIRED, SUPERSEDED)"
    )

    # Offer Content Details
    title_bn = models.CharField(
        max_length=255,
        help_text="প্রস্তাবের শিরোনাম বাংলায়"
    )
    description_bn = models.TextField(
        blank=True,
        default='',
        help_text="প্রস্তাবের বিস্তারিত বিবরণ বাংলায়"
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="কাজের বা সেবার পরিমাণ"
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="পরিমাপের একক (যেমন: ট্রাক, জন, দিন, স্কয়ার ফুট)"
    )

    # Monetary Architecture (Decimal Precision Only)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="মূল কাজের মূল্য (BDT)"
    )
    currency = models.CharField(
        max_length=10,
        default=DEFAULT_CURRENCY,
        help_text="মুদ্রা কোড (Default: BDT)"
    )
    delivery_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="পরিবহন বা ডেলিভারি ফি (যদি থাকে)"
    )
    service_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="সার্ভিস বা অতিরিক্ত চার্জ (যদি থাকে)"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="সর্বমোট মূল্য (সার্ভার-সাইড নির্ধারিত)"
    )

    # Terms & Timing
    terms_bn = models.TextField(
        blank=True,
        default='',
        help_text="প্রস্তাবের শর্তাবলী বাংলায়"
    )
    estimated_delivery_duration = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="আনুমানিক সময়কাল (যেমন: ২ দিনের মধ্যে, ২৪ ঘণ্টা)"
    )
    proposed_at = models.DateTimeField(
        default=timezone.now,
        help_text="প্রস্তাব প্রেরণের সময়"
    )
    expires_at = models.DateTimeField(
        db_index=True,
        help_text="প্রস্তাবের মেয়াদ শেষ হওয়ার সময়"
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="প্রস্তাব গ্রহণের সময়কাল"
    )
    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="প্রস্তাব প্রত্যাখ্যানের সময়কাল"
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="প্রস্তাব বাতিলের সময়কাল"
    )
    rejection_reason_bn = models.TextField(
        blank=True,
        default='',
        help_text="প্রত্যাখ্যানের কারণ বাংলায়"
    )
    cancellation_reason_bn = models.TextField(
        blank=True,
        default='',
        help_text="বাতিলের কারণ বাংলায়"
    )

    # Snapshot to protect historical audit integrity against future master-data changes
    snapshot = models.JSONField(
        default=dict,
        blank=True,
        help_text="প্রস্তাব তৈরির সময়কার ডিমান্ড ও প্রোভাইডার মেটাডাটার স্ন্যাপশট"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'প্রস্তাব (Offer)'
        verbose_name_plural = 'প্রস্তাবসমূহ (Offers)'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['demand', 'status']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['requester', 'status']),
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['root_offer', 'version']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['demand', 'provider', 'version'],
                name='unique_demand_provider_version_offer'
            )
        ]

    def __str__(self):
        type_lbl = OFFER_TYPE_LABELS_BN.get(self.offer_type, self.offer_type)
        status_lbl = OFFER_STATUS_LABELS_BN.get(self.status, self.status)
        return f"Offer #{self.id} (v{self.version}) - {type_lbl} [{status_lbl}]: ৳{self.total_amount}"

    @property
    def is_terminal(self) -> bool:
        return self.status in [
            OfferStatus.ACCEPTED,
            OfferStatus.REJECTED,
            OfferStatus.CANCELLED,
            OfferStatus.EXPIRED,
            OfferStatus.SUPERSEDED,
        ]

    def is_expired(self, now=None) -> bool:
        """
        Checks if offer has passed its expires_at timestamp.
        """
        current_time = now or timezone.now()
        return current_time >= self.expires_at

    @staticmethod
    def calculate_total(price: Decimal, delivery_fee: Decimal = Decimal('0.00'), service_fee: Decimal = Decimal('0.00')) -> Decimal:
        """
        Authoritative server-side total amount calculation using Decimal precision.
        """
        p = Decimal(str(price or '0.00'))
        d = Decimal(str(delivery_fee or '0.00'))
        s = Decimal(str(service_fee or '0.00'))
        return (p + d + s).quantize(Decimal('0.01'))

    def clean(self):
        """
        Django model validation.
        """
        validate_offer_pricing(self.price, self.delivery_fee, self.service_fee)
        if not self.total_amount:
            self.total_amount = self.calculate_total(self.price, self.delivery_fee, self.service_fee)

        if self.expires_at:
            validate_offer_expiry(self.expires_at)

        if hasattr(self, 'demand') and self.demand:
            validate_demand_eligibility_for_offer(self.demand)
            validate_offer_quantity(
                self.quantity,
                self.unit,
                getattr(self.demand, 'quantity', None),
                getattr(self.demand, 'unit', '')
            )

        if hasattr(self, 'provider') and self.provider:
            validate_provider_eligibility_for_offer(self.provider)

    def save(self, *args, **kwargs):
        # Always enforce server-side calculated total_amount
        self.total_amount = self.calculate_total(self.price, self.delivery_fee, self.service_fee)
        super().save(*args, **kwargs)


class OfferAuditLog(models.Model):
    """
    Append-only audit trail logging state transitions and lifecycle actions for an Offer.
    """
    id = models.BigAutoField(primary_key=True)
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        db_index=True
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer_audit_logs',
        help_text="যে ব্যবহারকারী পরিবর্তনটি ঘটিয়েছেন"
    )
    action = models.CharField(
        max_length=30,
        choices=OfferAuditAction.choices,
        db_index=True,
        help_text="অডিট অ্যাকশন (CREATED, COUNTERED, ACCEPTED, REJECTED, CANCELLED, EXPIRED, SUPERSEDED)"
    )
    previous_status = models.CharField(
        max_length=30,
        blank=True,
        default=''
    )
    new_status = models.CharField(
        max_length=30,
        blank=True,
        default=''
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="অতিরিক্ত অডিট তথ্য"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'অফার অডিট রেকর্ড (Offer Audit Log)'
        verbose_name_plural = 'অফার অডিট রেকর্ডসমূহ (Offer Audit Logs)'
        ordering = ['-created_at']

    def __str__(self):
        return f"Offer #{self.offer_id} Audit: {self.get_action_display()} at {self.created_at}"
