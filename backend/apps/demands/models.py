"""
Demand Models for SebaCox.
Architecture Foundation: User -> Demand -> Service -> Location.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from .constants import (
    DemandType,
    DemandStatus,
    DemandPriority,
    DemandVisibility,
    DemandContactPreference,
    DemandAuditAction,
    VALID_DEMAND_STATUS_TRANSITIONS,
    EDITABLE_DEMAND_STATUSES,
    LOCKED_HISTORICAL_STATUSES,
)
from .validators import (
    validate_demand_status_transition,
    validate_demand_budget,
    validate_demand_quantity,
)


class Demand(models.Model):
    """
    Production-ready Demand Model / “আমার প্রয়োজন”.
    Represents an authenticated user's specific published need for a service,
    product, rental, booking, or general requirement.
    
    Architectural separation:
    - Demand is NOT a Service (it references a Service/Category from Master Taxonomy).
    - Demand is NOT a Provider.
    - Demand is NOT a generic Post (it is a structured need).
    """
    id = models.BigAutoField(primary_key=True)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demands',
        db_index=True,
        help_text="প্রয়োজন পোস্টকারী ব্যবহারকারী (User account)"
    )
    service = models.ForeignKey(
        'categories.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        db_index=True,
        help_text="নির্দিষ্ট সেবা ট্যাক্সোনমি রেফারেন্স (Phase 4 Service)"
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        db_index=True,
        help_text="প্রধান ক্যাটাগরি রেফারেন্স (Phase 4 Category)"
    )
    title_bn = models.CharField(
        max_length=200,
        db_index=True,
        help_text="প্রয়োজনের বাংলা শিরোনাম (e.g. 'কক্সবাজার সদরে ১ ট্রাক ইট প্রয়োজন')"
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        default='',
        db_index=True,
        help_text="Title in English"
    )
    description_bn = models.TextField(
        help_text="প্রয়োজনের বিস্তারিত বিবরণ বাংলায়"
    )
    description_en = models.TextField(
        blank=True,
        default='',
        help_text="Detailed description in English"
    )
    demand_type = models.CharField(
        max_length=30,
        choices=DemandType.choices,
        default=DemandType.SERVICE,
        db_index=True,
        help_text="প্রয়োজনের ধরন (সেবা, পণ্য, ভাড়া, ইত্যাদি)"
    )
    status = models.CharField(
        max_length=30,
        choices=DemandStatus.choices,
        default=DemandStatus.DRAFT,
        db_index=True,
        help_text="জীবনচক্র অবস্থা (DRAFT, PUBLISHED, PAUSED, FULFILLED, CANCELLED, EXPIRED, CLOSED)"
    )
    priority = models.CharField(
        max_length=20,
        choices=DemandPriority.choices,
        default=DemandPriority.NORMAL,
        db_index=True,
        help_text="জরুরিতা মাত্রা (NORMAL, URGENT)"
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="পরিমাণ (ঐচ্ছিক)"
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="পরিমাপের একক (e.g. ট্রাক, জন, ব্যাগ, দিন, টি, শতক)"
    )
    budget_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="সর্বনিম্ন বাজেট (ঐচ্ছিক)"
    )
    budget_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="সর্বোচ্চ বাজেট (ঐচ্ছিক)"
    )
    currency = models.CharField(
        max_length=10,
        default='BDT',
        help_text="মুদ্রা কোড (Default: BDT)"
    )
    required_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="কখন প্রয়োজন (Asia/Dhaka time)"
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="মেয়াদ উত্তীর্ণের সময় (Asia/Dhaka time)"
    )

    # Location Integration (Phase 3 Location Engine)
    # Architectural Rule: CURRENT GPS ≠ SELECTED SERVICE AREA ≠ DEMAND LOCATION
    district = models.ForeignKey(
        'locations.District',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        help_text="প্রয়োজনের জেলা (e.g. কক্সবাজার)"
    )
    upazila = models.ForeignKey(
        'locations.Upazila',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        help_text="প্রয়োজনের উপজেলা (e.g. কক্সবাজার সদর, রামু, টেকনাফ)"
    )
    union = models.ForeignKey(
        'locations.Union',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        help_text="প্রয়োজনের ইউনিয়ন / পৌরসভা ওয়ার্ড"
    )
    ward = models.ForeignKey(
        'locations.Ward',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        help_text="প্রয়োজনের নির্দিষ্ট ওয়ার্ড"
    )
    geo_location = models.ForeignKey(
        'locations.GeoLocation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demands',
        help_text="সুনির্দিষ্ট জিপিএস কোঅর্ডিনেট (SRID 4326)"
    )
    location_display_bn = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="এলাকা বা ঠিকানার বাংলা বিবরণ (e.g. টেকপাড়া, কক্সবাজার সদর)"
    )
    location_display_en = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Location display in English"
    )

    # Privacy and Contact Channels
    visibility = models.CharField(
        max_length=30,
        choices=DemandVisibility.choices,
        default=DemandVisibility.PUBLIC,
        db_index=True,
        help_text="দৃশ্যমানতা পরিধি (PUBLIC, REGISTERED_USERS, PRIVATE)"
    )
    contact_preference = models.CharField(
        max_length=30,
        choices=DemandContactPreference.choices,
        default=DemandContactPreference.IN_APP_ONLY,
        db_index=True,
        help_text="যোগাযোগের মাধ্যম (IN_APP_ONLY, PHONE, BOTH)"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা"
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="সফ্ট ডিলিট / আর্কাইভ ফ্ল্যাগ"
    )

    # Lifecycle transition audit timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'আমার প্রয়োজন (Demand)'
        verbose_name_plural = 'প্রয়োজনসমূহ (Demands)'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active', 'is_deleted', '-created_at']),
            models.Index(fields=['requester', 'status', '-created_at']),
            models.Index(fields=['upazila', 'status', 'is_active']),
            models.Index(fields=['category', 'status', 'is_active']),
            models.Index(fields=['service', 'status', 'is_active']),
            models.Index(fields=['expires_at', 'status']),
        ]

    def __str__(self):
        return f"[{self.status}] {self.title_bn} (User #{self.requester_id})"

    def clean(self):
        super().clean()
        validate_demand_budget(self.budget_min, self.budget_max)
        validate_demand_quantity(self.quantity, self.unit)

        # Ensure category matches service category if both are provided
        if self.service and not self.category:
            self.category = self.service.category
        elif self.service and self.category and self.service.category_id != self.category_id:
            # Reconcile category with service's primary category
            self.category = self.service.category

    def is_expired(self, current_time=None) -> bool:
        """
        Check if demand's expiration time has elapsed.
        """
        if not self.expires_at:
            return False
        now = current_time or timezone.now()
        return self.expires_at < now

    def can_edit_by(self, user) -> bool:
        """
        Permission check: Owner can edit when in editable statuses (DRAFT, PUBLISHED, PAUSED).
        Admin/staff can always moderate.
        """
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        if self.requester_id == user.id:
            return self.status in EDITABLE_DEMAND_STATUSES
        return False

    def can_view_by(self, user) -> bool:
        """
        Visibility evaluation for privacy policy.
        """
        if self.visibility == DemandVisibility.PUBLIC:
            return True
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser or self.requester_id == user.id:
            return True
        if self.visibility == DemandVisibility.REGISTERED_USERS:
            return True
        # PRIVATE is only visible to requester and admin
        return False


class DemandAuditLog(models.Model):
    """
    Append-only audit trail recording every state change and critical modification
    of a Demand. Essential for compliance, fraud prevention, and debugging.
    """
    id = models.BigAutoField(primary_key=True)
    demand = models.ForeignKey(
        Demand,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        db_index=True,
        help_text="সম্পর্কিত প্রয়োজন"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demand_audit_logs',
        help_text="যে ব্যবহারকারী পরিবর্তনটি সম্পাদন করেছেন"
    )
    action = models.CharField(
        max_length=40,
        choices=DemandAuditAction.choices,
        db_index=True,
        help_text="সম্পাদিত কাজের ধরন"
    )
    from_status = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text="পূর্ববর্তী অবস্থা"
    )
    to_status = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text="পরবর্তী অবস্থা"
    )
    message = models.TextField(
        blank=True,
        default='',
        help_text="অডিট বা পরিবর্তনের বিবরণ"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="অতিরিক্ত মেটাডাটা"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="অডিট লগ তৈরির সময়কাল"
    )

    class Meta:
        verbose_name = 'প্রয়োজন অডিট লগ (Demand Audit Log)'
        verbose_name_plural = 'প্রয়োজন অডিট লগসমূহ (Demand Audit Logs)'
        ordering = ['-created_at']

    def __str__(self):
        return f"Demand #{self.demand_id} - {self.action} ({self.created_at})"
