"""
Provider Models for SebaCox.
Architecture Foundation: User ≠ Provider ≠ Service.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .constants import (
    ProviderType,
    ProviderStatus,
    VerificationStatus,
    AvailabilityStatus,
    ContactVisibility,
    PriceType,
    ProviderAuditAction,
    VALID_STATUS_TRANSITIONS,
)
from .validators import validate_slug, validate_status_transition


class Provider(models.Model):
    """
    Service Provider Profile Model.
    Strictly separated from User account.
    A User can exist without being a Provider, or may own a Provider profile.
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='providers',
        db_index=True,
        help_text="প্রোফাইলের মালিক ব্যবহারকারী (User account)"
    )
    provider_type = models.CharField(
        max_length=30,
        choices=ProviderType.choices,
        default=ProviderType.INDIVIDUAL,
        db_index=True,
        help_text="সেবাদাতার ধরন (ব্যক্তিগত, ব্যবসা, প্রতিষ্ঠান)"
    )
    display_name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="প্রদর্শনী নাম বাংলায় (e.g. কক্স ইলেকট্রিক কেয়ার, মো: রফিকুল ইসলাম)"
    )
    display_name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Display name in English"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        validators=[validate_slug],
        help_text="ইউনিক ইউআরএল স্লাগ (e.g. cox-electric-care)"
    )
    short_description_bn = models.TextField(
        blank=True,
        default='',
        help_text="সংক্ষিপ্ত পরিচিতি বাংলায়"
    )
    short_description_en = models.TextField(
        blank=True,
        default='',
        help_text="Short bio in English"
    )
    description_bn = models.TextField(
        blank=True,
        default='',
        help_text="বিস্তারিত বিবরণ বাংলায়"
    )
    description_en = models.TextField(
        blank=True,
        default='',
        help_text="Detailed description in English"
    )
    profile_image = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="প্রোফাইল ছবি বা লোগো পাথ"
    )
    cover_image = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="কভার ব্যানার ছবি পাথ"
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="যোগাযোগের ফোন নম্বর (ফাঁকা থাকলে ইউজারের নম্বর ব্যবহৃত হবে)"
    )
    contact_email = models.EmailField(
        blank=True,
        default='',
        help_text="যোগাযোগের ইমেইল"
    )
    contact_visibility = models.CharField(
        max_length=30,
        choices=ContactVisibility.choices,
        default=ContactVisibility.REGISTERED_ONLY,
        db_index=True,
        help_text="যোগাযোগের গোপনীয়তা নীতি"
    )
    status = models.CharField(
        max_length=30,
        choices=ProviderStatus.choices,
        default=ProviderStatus.DRAFT,
        db_index=True,
        help_text="লাইফসাইকেল স্ট্যাটাস"
    )
    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="যাচাইকৃত কিনা"
    )
    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.UNVERIFIED,
        db_index=True,
        help_text="ভেরিফিকেশন স্ট্যাটাস"
    )
    availability_status = models.CharField(
        max_length=30,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE,
        db_index=True,
        help_text="বর্তমান কর্মক্ষমতা/উপলব্ধতা অবস্থা"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="হাইলাইটেড বা ফিচার্ড সেবাদাতা কিনা"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সিস্টেম এনাবল অবস্থা"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সেবাদাতা (Provider)'
        verbose_name_plural = 'সেবাদাতাগণ (Providers)'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['provider_type', 'status']),
            models.Index(fields=['availability_status', 'status']),
            models.Index(fields=['is_verified', 'status']),
        ]

    def __str__(self):
        return f"{self.display_name_bn} ({self.get_status_display()})"

    def clean(self):
        super().clean()
        if self.slug:
            validate_slug(self.slug)

        # Ensure contact phone defaults to user phone if not explicitly provided
        if not self.contact_phone and hasattr(self, 'user') and self.user:
            self.contact_phone = getattr(self.user, 'mobile_number', '')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.display_name_en or self.display_name_bn or f"provider-{self.user_id}")
            self.slug = base_slug or f"provider-{self.user_id}"
        self.clean()
        super().save(*args, **kwargs)

    def transition_to(self, new_status: str, actor=None, note: str = ''):
        """
        Transitions the provider lifecycle status safely.
        Validates allowed transitions and creates an audit log record.
        """
        old_status = self.status
        if old_status == new_status:
            return self

        validate_status_transition(old_status, new_status)
        self.status = new_status
        self.save(update_fields=['status', 'updated_at'])

        ProviderAuditLog.objects.create(
            provider=self,
            actor=actor,
            action=ProviderAuditAction.STATUS_CHANGED,
            from_state=old_status,
            to_state=new_status,
            note=note
        )
        return self

    def set_availability(self, new_availability: str, actor=None, note: str = ''):
        """
        Updates availability status and logs the event.
        """
        old_availability = self.availability_status
        if old_availability == new_availability:
            return self

        self.availability_status = new_availability
        self.save(update_fields=['availability_status', 'updated_at'])

        ProviderAuditLog.objects.create(
            provider=self,
            actor=actor,
            action=ProviderAuditAction.AVAILABILITY_CHANGED,
            from_state=old_availability,
            to_state=new_availability,
            note=note
        )
        return self


class ProviderService(models.Model):
    """
    Mapping between Provider and Platform Service.
    Rule: ProviderService does NOT override platform Service capabilities.
    The Service model remains the platform's Single Source of Truth.
    """
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='services',
        db_index=True,
        help_text="যে সেবাদাতার সেবা"
    )
    service = models.ForeignKey(
        'categories.Service',
        on_delete=models.PROTECT,
        related_name='provider_offerings',
        db_index=True,
        help_text="প্ল্যাটফর্ম নির্ধারিত সেবা"
    )
    title_bn = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="সেবাদাতার নিজস্ব শিরোনাম (ঐচ্ছিক)"
    )
    title_en = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Provider's custom service title in English (optional)"
    )
    description_bn = models.TextField(
        blank=True,
        default='',
        help_text="সেবাদাতার নির্দিষ্ট বিবরণ"
    )
    description_en = models.TextField(
        blank=True,
        default='',
        help_text="Provider's specific description in English"
    )
    starting_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="প্রাথমিক মূল্য বা রেট (ঐচ্ছিক)"
    )
    price_type = models.CharField(
        max_length=30,
        choices=PriceType.choices,
        default=PriceType.STARTING_FROM,
        blank=True,
        help_text="মূল্যের ধরন"
    )
    is_available = models.BooleanField(
        default=True,
        db_index=True,
        help_text="বর্তমানে এই সেবাটি প্রদান করা হচ্ছে কিনা"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সেবাদাতার সেবা (Provider Service)'
        verbose_name_plural = 'সেবাদাতার সেবাসমূহ (Provider Services)'
        constraints = [
            models.UniqueConstraint(
                fields=['provider', 'service'],
                name='unique_provider_service_mapping'
            )
        ]
        ordering = ['-is_available', '-created_at']

    def __str__(self):
        name = self.title_bn or (self.service.name_bn if hasattr(self, 'service') else 'Service')
        return f"{self.provider.display_name_bn} - {name}"

    @property
    def effective_capabilities(self):
        """
        Guarantees Service capability preservation:
        Returns capabilities directly from platform Service entity.
        """
        if not self.service:
            return {}
        return {
            'requires_booking': self.service.requires_booking,
            'supports_demand': self.service.supports_demand,
            'supports_offer': self.service.supports_offer,
            'supports_negotiation': self.service.supports_negotiation,
            'supports_delivery': self.service.supports_delivery,
            'supports_location': self.service.supports_location,
            'supports_online': self.service.supports_online,
            'supports_order': self.service.supports_order,
            'supports_rental': self.service.supports_rental,
            'supports_payment': self.service.supports_payment,
        }


class ProviderServiceArea(models.Model):
    """
    Provider Service Area Coverage.
    Integrates directly with Phase 3 Location Engine.
    Allows administrative boundary coverage (District, Upazila, Municipality, Union, Ward, Locality)
    and future GPS radial coverage.
    """
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='service_areas',
        db_index=True
    )
    area_type = models.CharField(
        max_length=30,
        default='ADMINISTRATIVE',
        help_text="এলাকার ধরন (ADMINISTRATIVE / RADIUS)"
    )
    district = models.ForeignKey(
        'locations.District',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    upazila = models.ForeignKey(
        'locations.Upazila',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    municipality = models.ForeignKey(
        'locations.Municipality',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    union = models.ForeignKey(
        'locations.Union',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    ward = models.ForeignKey(
        'locations.Ward',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    locality = models.ForeignKey(
        'locations.Locality',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    service_area = models.ForeignKey(
        'locations.ServiceArea',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='provider_service_areas'
    )
    radius_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GPS কেন্দ্র থেকে কভারেজ ব্যাসার্ধ (কিমি)"
    )
    center_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    center_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সেবাদাতার এলাকা (Provider Service Area)'
        verbose_name_plural = 'সেবাদাতার এলাকাসমূহ (Provider Service Areas)'
        ordering = ['-is_active', '-created_at']

    def __str__(self):
        target = self.upazila or self.municipality or self.district or self.union or 'All'
        return f"{self.provider.display_name_bn} - {target}"

    def clean(self):
        super().clean()
        if not any([self.district, self.upazila, self.municipality, self.union, self.ward, self.locality, self.service_area, self.radius_km]):
            raise ValidationError("অন্তত একটি প্রশাসনিক এলাকা বা ব্যাসার্ধ নির্ধারণ করা আবশ্যক।")


class ProviderAuditLog(models.Model):
    """
    Audit Trail for Provider Lifecycle & Configuration Changes.
    Enforces accountability and state tracking.
    """
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        db_index=True
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='provider_audit_events'
    )
    action = models.CharField(
        max_length=50,
        choices=ProviderAuditAction.choices,
        db_index=True
    )
    from_state = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    to_state = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    note = models.TextField(
        blank=True,
        default=''
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'সেবাদাতা অডিট লগ (Provider Audit Log)'
        verbose_name_plural = 'সেবাদাতা অডিট লগসমূহ (Provider Audit Logs)'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.action}] Provider #{self.provider_id} by Actor #{self.actor_id or 'System'}"
