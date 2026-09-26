"""
Category, SubCategory & Service Models for SebaCox.
Universal Service Taxonomy & Master Data Engine (Master Taxonomy v1.0).
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import unicodedata
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .constants import (
    CategoryKind,
    ServiceType,
    AliasTargetType,
    AliasLanguage,
    AliasType,
    TaxonomyStatus,
    TaxonomyActionType,
)
from .validators import validate_slug, validate_no_circular_parent
import re


def normalize_alias_text(text: str) -> str:
    """
    Normalizes alias query text in Bangla (Unicode NFC) and English (lowercase).
    Strips punctuation, collapses multiple whitespaces, and unifies variations.
    """
    if not text:
        return ''
    # Unicode NFC Normalization
    normalized = unicodedata.normalize('NFC', text.strip())
    # Remove Zero-Width Non-Joiner / Joiner
    normalized = normalized.replace('\u200c', '').replace('\u200d', '')
    # Lowercase English characters
    normalized = normalized.lower()
    # Strip common punctuation: commas, colons, dashes, question marks, bangs, Bangla Dari (।)
    normalized = re.sub(r'[\?!,;:\(\)\[\]\{\}\\\/\-_\."\'“”‘’।]+', ' ', normalized)
    # Collapse multiple whitespaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


class Category(models.Model):
    """
    Universal Master Category Model (31 Master Categories).
    Acts as the top-level architectural grouping.
    Supports hierarchical tree structure and status control.
    """
    name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="ক্যাটাগরির বাংলা নাম (e.g. নির্মাণ ও প্রকৌশল, স্বাস্থ্য ও চিকিৎসা)"
    )
    name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="English Category Name (e.g. Construction & Engineering, Health & Medical)"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        validators=[validate_slug],
        help_text="Unique URL-safe identifier (e.g. construction-engineering, health-medical)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Icon identifier (e.g. hammer, wrench, compass, activity)"
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
        help_text="প্যারেন্ট ক্যাটাগরি (Parent Category for nested taxonomy)"
    )
    level = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="হায়ারার্কি স্তর (0 for Root Category, 1 for Subcategory, etc.)"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="প্রদর্শনের ক্রম (Sorting display order 1-31)"
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
    is_popular = models.BooleanField(
        default=False,
        db_index=True,
        help_text="জনপ্রিয় ক্যাটাগরি হাইলাইট"
    )
    status = models.CharField(
        max_length=20,
        choices=TaxonomyStatus.choices,
        default=TaxonomyStatus.ACTIVE,
        db_index=True,
        help_text="ট্যাক্সোনমি লাইফসাইকেল স্ট্যাটাস (DRAFT, ACTIVE, INACTIVE, DEPRECATED, MERGED)"
    )
    merged_into = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='merged_categories',
        help_text="একীভূতকৃত টার্গেট ক্যাটাগরি (Merged target category)"
    )
    replacement = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_categories',
        help_text="প্রতিস্থাপক ক্যাটাগরি (Replacement category)"
    )
    deprecation_reason = models.TextField(
        blank=True,
        default='',
        help_text="বাতিল বা অপ্রচলনের কারণ (Reason for deprecation/merger)"
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
            models.Index(fields=['is_popular', 'is_active']),
            models.Index(fields=['status', 'is_active']),
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
            if not self.kind and self.parent.kind:
                self.kind = self.parent.kind
        else:
            self.level = 0

        # Synchronize status with is_active
        if self.status == TaxonomyStatus.ACTIVE:
            self.is_active = True
        elif self.status in (TaxonomyStatus.INACTIVE, TaxonomyStatus.DEPRECATED, TaxonomyStatus.MERGED, TaxonomyStatus.DRAFT):
            self.is_active = False

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent hard deletion if related business entities exist
        has_subcategories = self.subcategories.exists()
        has_services = self.services.exists()
        has_demands = getattr(self, 'demands', None) and self.demands.exists()
        has_providers = getattr(self, 'provider_services', None) and self.provider_services.exists()

        if has_subcategories or has_services or has_demands or has_providers:
            raise ValidationError(
                f"ক্যাটাগরি '{self.name_bn}' সরাসরি মুছে ফেলা যাবে না কারণ এর অধীনে সাব-ক্যাটাগরি/সেবা/ডিমান্ড/প্রোভাইডার যুক্ত রয়েছে। অনুগ্রহ করে Deactivate, Deprecate বা Merge অ্যাকশন ব্যবহার করুন।"
            )
        super().delete(*args, **kwargs)

    @property
    def has_children(self) -> bool:
        return self.children.filter(is_active=True).exists()

    @property
    def active_children_count(self) -> int:
        return self.children.filter(is_active=True).count()

    @property
    def active_subcategories_count(self) -> int:
        return self.subcategories.filter(is_active=True).count()

    @property
    def active_services_count(self) -> int:
        return self.services.filter(is_active=True).count()


class SubCategory(models.Model):
    """
    Granular Master SubCategory Model (Master Taxonomy v1.0).
    Every SubCategory strictly belongs to a single Master Category.
    Cascades directly from Category in UI and APIs.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        db_index=True,
        help_text="প্রধান ক্যাটাগরি (Parent Master Category)"
    )
    name_bn = models.CharField(
        max_length=150,
        db_index=True,
        help_text="সাব-ক্যাটাগরির বাংলা নাম (e.g. নির্মাণ শ্রমিক ও মিস্ত্রি, রাজমিস্ত্রি)"
    )
    name_en = models.CharField(
        max_length=150,
        db_index=True,
        help_text="English SubCategory Name (e.g. Masonry & Casting Labour)"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        validators=[validate_slug],
        help_text="Unique URL-safe identifier (e.g. masonry-casting-labour)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Icon identifier (optional)"
    )
    short_description_bn = models.TextField(
        blank=True,
        default='',
        help_text="সাব-ক্যাটাগরির সংক্ষিপ্ত বিবরণ (বাংলা)"
    )
    short_description_en = models.TextField(
        blank=True,
        default='',
        help_text="Short subcategory description (English)"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="ক্যাটাগরির মধ্যে প্রদর্শনের ক্রম"
    )
    is_popular = models.BooleanField(
        default=False,
        db_index=True,
        help_text="জনপ্রিয় সাব-ক্যাটাগরি কিনা"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা"
    )
    status = models.CharField(
        max_length=20,
        choices=TaxonomyStatus.choices,
        default=TaxonomyStatus.ACTIVE,
        db_index=True,
        help_text="ট্যাক্সোনমি লাইফসাইকেল স্ট্যাটাস"
    )
    merged_into = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='merged_subcategories',
        help_text="একীভূতকৃত টার্গেট সাব-ক্যাটাগরি"
    )
    replacement = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_subcategories',
        help_text="প্রতিস্থাপক সাব-ক্যাটাগরি"
    )
    deprecation_reason = models.TextField(
        blank=True,
        default='',
        help_text="বাতিল বা অপ্রচলনের কারণ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'সাব-ক্যাটাগরি (SubCategory)'
        verbose_name_plural = 'সাব-ক্যাটাগরিসমূহ (SubCategories)'
        ordering = ['sort_order', 'name_bn']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name_bn'],
                name='unique_subcategory_per_category_bn'
            ),
        ]
        indexes = [
            models.Index(fields=['category', 'is_active', 'sort_order']),
            models.Index(fields=['is_popular', 'is_active']),
            models.Index(fields=['slug', 'is_active']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"{self.category.name_bn} → {self.name_bn} ({self.name_en})"

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name_en)
        if not self.category_id:
            raise ValidationError({'category': 'সাব-ক্যাটাগরির জন্য একটি প্রধান ক্যাটাগরি আবশ্যক।'})

        # Synchronize status with is_active
        if self.status == TaxonomyStatus.ACTIVE:
            self.is_active = True
        elif self.status in (TaxonomyStatus.INACTIVE, TaxonomyStatus.DEPRECATED, TaxonomyStatus.MERGED, TaxonomyStatus.DRAFT):
            self.is_active = False

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        has_services = self.services.exists()
        has_demands = getattr(self, 'demands', None) and self.demands.exists()
        has_providers = getattr(self, 'provider_services', None) and self.provider_services.exists()

        if has_services or has_demands or has_providers:
            raise ValidationError(
                f"সাব-ক্যাটাগরি '{self.name_bn}' সরাসরি মুছে ফেলা যাবে না কারণ এর সাথে সেবা/ডিমান্ড/প্রোভাইডার যুক্ত রয়েছে। অনুগ্রহ করে Deactivate, Deprecate বা Merge অ্যাকশন ব্যবহার করুন।"
            )
        super().delete(*args, **kwargs)


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
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        db_index=True,
        help_text="সাব-ক্যাটাগরি (SubCategory classification)"
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
            models.Index(fields=['subcategory', 'is_active']),
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


class TaxonomyAlias(models.Model):
    """
    Taxonomy Search & Synonym Alias Model.
    Provides fast, normalized phonetic & vernacular synonym mapping for search indexing.
    Examples:
    - 'রাজমিস্ত্রি' -> SubCategory(102: Masonry & Casting Labour)
    - 'মেস্ত্রি' -> SubCategory(102: Masonry & Casting Labour)
    - 'গাড়ি ভাড়া' -> Category(6: Vehicle Rental & Transport)
    """
    alias_text = models.CharField(
        max_length=150,
        db_index=True,
        help_text="এলিয়াস বা বিকল্প নাম (e.g. রাজমিস্ত্রি, মেস্ত্রি, mason)"
    )
    normalized_text = models.CharField(
        max_length=150,
        db_index=True,
        help_text="স্বাভাবিককৃত সার্চ টেক্সট (Unicode NFC + lowercase)"
    )
    target_type = models.CharField(
        max_length=30,
        choices=AliasTargetType.choices,
        default=AliasTargetType.SUBCATEGORY,
        db_index=True,
        help_text="টার্গেট এনটিটি টাইপ (CATEGORY, SUBCATEGORY, SERVICE, SKILL)"
    )
    target_id = models.PositiveIntegerField(
        db_index=True,
        help_text="টার্গেট অবজেক্টের আইডি"
    )
    language = models.CharField(
        max_length=10,
        choices=AliasLanguage.choices,
        default=AliasLanguage.BN,
        help_text="ভাষা (BN, EN, ALL)"
    )
    alias_type = models.CharField(
        max_length=30,
        choices=AliasType.choices,
        default=AliasType.COMMON,
        db_index=True,
        help_text="এলিয়াসের ধরণ (EXACT, COMMON, COLLOQUIAL, LOCAL_TERM, etc.)"
    )
    priority = models.PositiveIntegerField(
        default=100,
        db_index=True,
        help_text="সার্চ প্রায়োরিটি ওয়েট (উচ্চ মান = উচ্চ স্থান)"
    )
    service_type = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text="নির্দিষ্ট সেবার ধরণ (ঐচ্ছিক)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='aliases',
        help_text="সংশ্লিষ্ট প্রধান ক্যাটাগরি (ঐচ্ছিক)"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='aliases',
        help_text="সংশ্লিষ্ট সাব-ক্যাটাগরি (ঐচ্ছিক)"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় অবস্থা"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ট্যাক্সোনমি এলিয়াস (Taxonomy Alias)'
        verbose_name_plural = 'ট্যাক্সোনমি এলিয়াসসমূহ (Taxonomy Aliases)'
        ordering = ['-priority', 'alias_text']
        indexes = [
            models.Index(fields=['normalized_text', 'is_active']),
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['priority', 'is_active']),
        ]

    def __str__(self):
        return f"{self.alias_text} → {self.target_type}:{self.target_id} ({self.get_language_display()})"

    def clean(self):
        if self.alias_text:
            self.normalized_text = normalize_alias_text(self.alias_text)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class TaxonomyVersion(models.Model):
    """
    SebaCox Master Taxonomy Version & Deployment Registry.
    Tracks official canonical releases (e.g. Version 1.0, Version 1.1) and catalog manifests.
    """
    version_number = models.CharField(
        max_length=20,
        unique=True,
        default='1.0',
        db_index=True,
        help_text="ট্যাক্সোনমি ভার্সন নম্বর (e.g. 1.0, 1.1, 2.0)"
    )
    release_title = models.CharField(
        max_length=150,
        default='SebaCox Master Taxonomy v1.0',
        help_text="রিলিজ টাইটেল"
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text="ভার্সন বিবরণ ও পরিবর্তনের সারসংক্ষেপ"
    )
    changelog = models.JSONField(
        default=list,
        blank=True,
        help_text="কাঠামোগত পরিবর্তন ও রিলিজ নোটের তালিকা"
    )
    is_current = models.BooleanField(
        default=True,
        db_index=True,
        help_text="বর্তমান সক্রিয় ট্যাক্সোনমি ভার্সন কিনা"
    )
    total_categories_count = models.PositiveIntegerField(
        default=0,
        help_text="মোট সক্রিয় ক্যাটাগরি সংখ্যা"
    )
    total_subcategories_count = models.PositiveIntegerField(
        default=0,
        help_text="মোট সক্রিয় সাব-ক্যাটাগরি সংখ্যা"
    )
    total_aliases_count = models.PositiveIntegerField(
        default=0,
        help_text="মোট সক্রিয় এলিয়াস সংখ্যা"
    )
    checksum = models.CharField(
        max_length=64,
        blank=True,
        default='',
        help_text="ট্যাক্সোনমি কন্টেন্ট হ্যাশ / ই-ট্যাগ (for client cache validation)"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ট্যাক্সোনমি ভার্সন (Taxonomy Version)'
        verbose_name_plural = 'ট্যাক্সোনমি ভার্সনসমূহ (Taxonomy Versions)'
        ordering = ['-version_number']

    def __str__(self):
        current_badge = " [Current]" if self.is_current else ""
        return f"{self.release_title} (v{self.version_number}){current_badge}"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Set all other versions to non-current
            TaxonomyVersion.objects.exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)


class TaxonomyChangeLog(models.Model):
    """
    Audit Trail and Change History for Master Taxonomy Governance.
    Logs every Rename, Deactivate, Deprecate, Merge, Move, Replace & Alias operation.
    """
    target_type = models.CharField(
        max_length=30,
        choices=AliasTargetType.choices,
        db_index=True,
        help_text="এনটিটি টাইপ (CATEGORY, SUBCATEGORY, SERVICE, ALIAS, VERSION)"
    )
    target_id = models.PositiveIntegerField(
        db_index=True,
        help_text="টার্গেট অবজেক্টের আইডি"
    )
    target_name = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="অবজেক্টের নাম বা শিরোনাম"
    )
    action = models.CharField(
        max_length=30,
        choices=TaxonomyActionType.choices,
        db_index=True,
        help_text="অ্যাকশন টাইপ (CREATE, RENAME, DEACTIVATE, MERGE, MOVE, etc.)"
    )
    old_values = models.JSONField(
        default=dict,
        blank=True,
        help_text="পূর্বের মান"
    )
    new_values = models.JSONField(
        default=dict,
        blank=True,
        help_text="নতুন মান"
    )
    reason = models.TextField(
        blank=True,
        default='',
        help_text="পরিবর্তনের কারণ বা এডমিন নোট"
    )
    impact_summary = models.JSONField(
        default=dict,
        blank=True,
        help_text="প্রভাব বিশ্লেষণ সারসংক্ষেপ (Affected providers, demands, services)"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taxonomy_changes',
        help_text="পরিবর্তনকারী এডমিন ব্যবহারকারী"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'ট্যাক্সোনমি চেঞ্জ লগ (Taxonomy Change Log)'
        verbose_name_plural = 'ট্যাক্সোনমি চেঞ্জ লগসমূহ (Taxonomy Change Logs)'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['action', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.get_action_display()}] {self.target_type}:{self.target_id} ({self.target_name}) at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
