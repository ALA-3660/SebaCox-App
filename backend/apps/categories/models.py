"""
Category & Service Models for SebaCox.
Universal Service Taxonomy & Capability Engine.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .constants import CategoryKind, ServiceType
from .validators import validate_slug, validate_no_circular_parent


class Category(models.Model):
    """
    Universal hierarchical Category Model.
    Supports arbitrarily deep taxonomy (Parent -> Subcategory -> Sub-subcategory).
    Architecturally separates Public Service Categories from internal System Domains.
    """
    name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="ক্যাটাগরির বাংলা নাম (e.g. স্বাস্থ্য ও চিকিৎসা, ডাক্তার)"
    )
    name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="English Category Name (e.g. Health & Medical, Doctors)"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        validators=[validate_slug],
        help_text="Unique URL-safe identifier (e.g. health-medical, doctors)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Icon identifier (e.g. activity, home, tool)"
    )
    description_bn = models.TextField(
        blank=True,
        default='',
        help_text="ক্যাটাগরির বিস্তারিত বাংলা বিবরণ"
    )
    description_en = models.TextField(
        blank=True,
        default='',
        help_text="Detailed category description in English"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        help_text="প্যারেন্ট ক্যাটাগরি (Parent Category)"
    )
    level = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="হায়ারার্কি স্তর (0 for Root Category, 1 for Subcategory, etc.)"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="প্রদর্শনের ক্রম (Sorting display order)"
    )
    kind = models.CharField(
        max_length=30,
        choices=CategoryKind.choices,
        default=CategoryKind.PUBLIC_SERVICE_CATEGORY,
        db_index=True,
        help_text="ক্যাটাগরি ক্লাসিফিকেশন (Public service category vs Platform system domain)"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা (Active for public directory)"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="হোমস্ক্রিন বা ফিচার্ড তালিকায় প্রদর্শন"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ক্যাটাগরি (Category)'
        verbose_name_plural = 'ক্যাটাগরিসমূহ (Categories)'
        ordering = ['sort_order', 'name_bn']
        indexes = [
            models.Index(fields=['is_active', 'kind', 'parent', 'sort_order']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        prefix = f"L{self.level}: " if self.level > 0 else ""
        return f"{prefix}{self.name_bn} ({self.name_en})"

    def clean(self):
        """Validate integrity and prevent cyclic dependencies."""
        if not self.slug:
            self.slug = slugify(self.name_en)

        if self.parent_id and self.id and self.parent_id == self.id:
            raise ValidationError({'parent': 'একটি ক্যাটাগরি নিজেই নিজের প্যারেন্ট হতে পারে না।'})

        if self.parent_id:
            validate_no_circular_parent(self.id, self.parent_id, Category)
            self.level = self.parent.level + 1
            # Inherit kind from parent if not explicitly changed
            if not self.kind and self.parent.kind:
                self.kind = self.parent.kind
        else:
            self.level = 0

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def has_children(self) -> bool:
        return self.children.filter(is_active=True).exists()

    @property
    def active_children_count(self) -> int:
        return self.children.filter(is_active=True).count()

    @property
    def active_services_count(self) -> int:
        return self.services.filter(is_active=True).count()


class Service(models.Model):
    """
    Universal Service Model.
    Acts as the single source of truth for service taxonomy and capability metadata.
    Enables future specialized modules (Doctor, Hotel, Bus, Mason) to extend cleanly.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='services',
        db_index=True,
        help_text="প্রধান ক্যাটাগরি (Primary Category)"
    )
    secondary_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='cross_services',
        help_text="অতিরিক্ত ক্যাটাগরি (Optional cross-category classification)"
    )
    name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="সেবার বাংলা নাম (e.g. কার্ডিওলজি চিকিৎসা, সিভিল ইঞ্জিনিয়ারিং সেবা)"
    )
    name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Service English Name (e.g. Cardiology Care, Civil Engineering Service)"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        validators=[validate_slug],
        help_text="Unique URL-safe identifier (e.g. cardiology-care, civil-engineering)"
    )
    short_description_bn = models.TextField(
        blank=True,
        default='',
        help_text="সেবার সংক্ষিপ্ত বিবরণ (বাংলা)"
    )
    short_description_en = models.TextField(
        blank=True,
        default='',
        help_text="Short service description (English)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="আইকন বা ইমেজ রেফারেন্স"
    )
    service_type = models.CharField(
        max_length=30,
        choices=ServiceType.choices,
        default=ServiceType.SERVICE,
        db_index=True,
        help_text="সেবার ধরন / স্ট্র্যাটেজি (Service, Product, Rental, Booking, etc.)"
    )

    # -------------------------------------------------------------------------
    # Universal Service Capabilities (Metadata Flags)
    # Single source of truth driving frontend dynamic workflows & future engines
    # -------------------------------------------------------------------------
    requires_booking = models.BooleanField(
        default=False,
        db_index=True,
        help_text="বুকিং ও সময় নির্ধারণ আবশ্যক কিনা (Booking required)"
    )
    supports_demand = models.BooleanField(
        default=False,
        db_index=True,
        help_text="গ্রাহক প্রয়োজন/অনুরোধ পোস্ট করতে পারবে কিনা (Supports demand/request)"
    )
    supports_offer = models.BooleanField(
        default=False,
        db_index=True,
        help_text="সেবাদাতা অফার পাঠাতে পারবে কিনা (Supports provider offer)"
    )
    supports_negotiation = models.BooleanField(
        default=False,
        db_index=True,
        help_text="দর কষাকষি প্রযোজ্য কিনা (Supports price negotiation)"
    )
    supports_delivery = models.BooleanField(
        default=False,
        db_index=True,
        help_text="হোম ডেলিভারি বা কুরিয়ার প্রযোজ্য কিনা (Supports delivery)"
    )
    supports_location = models.BooleanField(
        default=True,
        db_index=True,
        help_text="ভৌগোলিক অবস্থান ভিত্তিক সেবা কিনা (Location-dependent service)"
    )
    supports_online = models.BooleanField(
        default=False,
        db_index=True,
        help_text="অনলাইন বা দূরবর্তী সেবা দেওয়া সম্ভব কিনা (Supports online execution)"
    )
    supports_order = models.BooleanField(
        default=False,
        db_index=True,
        help_text="সরাসরি কার্ট অর্ডার প্রযোজ্য কিনা (Supports direct product ordering)"
    )
    supports_rental = models.BooleanField(
        default=False,
        db_index=True,
        help_text="ভাড়াভিত্তিক সেবা কিনা (Supports rental duration/calendar)"
    )
    supports_payment = models.BooleanField(
        default=False,
        db_index=True,
        help_text="ডিজিটাল পেমেন্ট সাপোর্ট করবে কিনা (Supports digital escrow/payment)"
    )

    # Status & Ordering
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="জনপ্রিয় বা নির্বাচিত সেবা"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="সাজানোর ক্রম"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সেবা (Service)'
        verbose_name_plural = 'সেবাসমূহ (Services)'
        ordering = ['sort_order', 'name_bn']
        indexes = [
            models.Index(fields=['category', 'is_active', 'sort_order']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['service_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name_bn} ({self.name_en}) - {self.get_service_type_display()}"

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name_en)
        if not self.category_id:
            raise ValidationError({'category': 'সেবার জন্য একটি বৈধ ক্যাটাগরি নির্বাচন করা আবশ্যক।'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def capability_matrix(self) -> dict:
        """Returns consolidated dictionary of supported capabilities."""
        return {
            'requires_booking': self.requires_booking,
            'supports_demand': self.supports_demand,
            'supports_offer': self.supports_offer,
            'supports_negotiation': self.supports_negotiation,
            'supports_delivery': self.supports_delivery,
            'supports_location': self.supports_location,
            'supports_online': self.supports_online,
            'supports_order': self.supports_order,
            'supports_rental': self.supports_rental,
            'supports_payment': self.supports_payment,
        }
