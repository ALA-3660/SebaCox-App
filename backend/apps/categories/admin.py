"""
Django Admin interface for Categories, SubCategories, Services, Taxonomy Aliases,
Taxonomy Releases (Versions) and Governance Audit Trail.
Master Taxonomy v1.0
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, SubCategory, Service, TaxonomyAlias, TaxonomyVersion, TaxonomyChangeLog
from .constants import CategoryKind, ServiceType, TaxonomyStatus, TaxonomyActionType
from .governance import TaxonomyGovernanceService


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ['name_bn', 'name_en', 'slug', 'sort_order', 'status', 'is_popular', 'is_active']
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'sort_order',
        'name_bn',
        'name_en',
        'slug',
        'subcategories_count',
        'kind',
        'status_badge',
        'is_active',
        'is_popular',
        'is_featured',
    ]
    list_filter = ['status', 'is_active', 'is_popular', 'is_featured', 'kind', 'level']
    search_fields = ['name_bn', 'name_en', 'slug', 'description_bn', 'description_en', 'deprecation_reason']
    ordering = ['sort_order', 'name_bn']
    readonly_fields = ['level', 'created_at', 'updated_at']
    raw_id_fields = ['parent', 'merged_into', 'replacement']
    inlines = [SubCategoryInline]
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured', 'check_integrity']

    def subcategories_count(self, obj):
        return obj.subcategories.count()
    subcategories_count.short_description = 'সাব-ক্যাটাগরি সংখ্যা'

    def status_badge(self, obj):
        color_map = {
            TaxonomyStatus.ACTIVE: '#16a34a',
            TaxonomyStatus.INACTIVE: '#64748b',
            TaxonomyStatus.DEPRECATED: '#e11d48',
            TaxonomyStatus.MERGED: '#7c3aed',
            TaxonomyStatus.DRAFT: '#ca8a04',
        }
        color = color_map.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'স্ট্যাটাস'

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        for cat in queryset:
            TaxonomyGovernanceService.reactivate_category(cat.id, reason="Admin batch activation", user=request.user)

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ নিষ্ক্রিয় করুন (Deactivate safely)')
    def make_inactive(self, request, queryset):
        for cat in queryset:
            TaxonomyGovernanceService.deactivate_category(cat.id, reason="Admin batch deactivation", user=request.user)

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ ফিচার্ড করুন (Mark as Featured)')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ ফিচার্ড থেকে বাদ দিন (Unmark Featured)')
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'category',
        'sort_order',
        'name_bn',
        'name_en',
        'slug',
        'status_badge',
        'is_popular',
        'is_active',
    ]
    list_filter = ['status', 'category', 'is_popular', 'is_active']
    search_fields = ['name_bn', 'name_en', 'slug', 'category__name_bn', 'category__name_en', 'deprecation_reason']
    ordering = ['category__sort_order', 'sort_order', 'name_bn']
    raw_id_fields = ['category', 'merged_into', 'replacement']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['make_active', 'make_inactive']

    def status_badge(self, obj):
        color_map = {
            TaxonomyStatus.ACTIVE: '#16a34a',
            TaxonomyStatus.INACTIVE: '#64748b',
            TaxonomyStatus.DEPRECATED: '#e11d48',
            TaxonomyStatus.MERGED: '#7c3aed',
            TaxonomyStatus.DRAFT: '#ca8a04',
        }
        color = color_map.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'স্ট্যাটাস'

    @admin.action(description='নির্বাচিত সাব-ক্যাটাগরিসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        for sub in queryset:
            TaxonomyGovernanceService.reactivate_subcategory(sub.id, reason="Admin batch activation", user=request.user)

    @admin.action(description='নির্বাচিত সাব-ক্যাটাগরিসমূহ নিষ্ক্রিয় করুন (Deactivate safely)')
    def make_inactive(self, request, queryset):
        for sub in queryset:
            TaxonomyGovernanceService.deactivate_subcategory(sub.id, reason="Admin batch deactivation", user=request.user)


@admin.register(TaxonomyAlias)
class TaxonomyAliasAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'alias_text',
        'normalized_text',
        'target_type',
        'target_id',
        'alias_type',
        'priority',
        'category',
        'subcategory',
        'language',
        'is_active',
    ]
    list_filter = ['target_type', 'alias_type', 'language', 'is_active', 'category']
    search_fields = ['alias_text', 'normalized_text']
    raw_id_fields = ['category', 'subcategory']
    ordering = ['-priority', 'alias_text']
    actions = ['make_active', 'make_inactive']

    @admin.action(description='নির্বাচিত এলিয়াসসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='নির্বাচিত এলিয়াসসমূহ নিষ্ক্রিয় করুন (Deactivate)')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(TaxonomyVersion)
class TaxonomyVersionAdmin(admin.ModelAdmin):
    list_display = [
        'version_number',
        'release_title',
        'is_current_badge',
        'total_categories_count',
        'total_subcategories_count',
        'total_aliases_count',
        'checksum',
        'applied_at',
    ]
    list_filter = ['is_current']
    search_fields = ['version_number', 'release_title', 'description', 'checksum']
    ordering = ['-applied_at']
    readonly_fields = ['checksum', 'applied_at', 'created_at', 'updated_at']

    def is_current_badge(self, obj):
        if obj.is_current:
            return format_html('<span style="background-color: #16a34a; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 600;">ACTIVE CANONICAL</span>')
        return format_html('<span style="color: #64748b;">Previous</span>')
    is_current_badge.short_description = 'বর্তমান ভার্সন'


@admin.register(TaxonomyChangeLog)
class TaxonomyChangeLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'action_badge',
        'target_type',
        'target_id',
        'target_name',
        'reason',
        'changed_by',
        'created_at',
    ]
    list_filter = ['action', 'target_type', 'created_at']
    search_fields = ['target_name', 'reason']
    ordering = ['-created_at']
    readonly_fields = [
        'target_type',
        'target_id',
        'target_name',
        'action',
        'old_values',
        'new_values',
        'reason',
        'impact_summary',
        'changed_by',
        'created_at',
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def action_badge(self, obj):
        color_map = {
            TaxonomyActionType.CREATE: '#16a34a',
            TaxonomyActionType.RENAME: '#0284c7',
            TaxonomyActionType.MOVE: '#d97706',
            TaxonomyActionType.MERGE: '#7c3aed',
            TaxonomyActionType.DEPRECATE: '#e11d48',
            TaxonomyActionType.DEACTIVATE: '#64748b',
            TaxonomyActionType.REACTIVATE: '#059669',
            TaxonomyActionType.VERSION_BUMP: '#4338ca',
        }
        color = color_map.get(obj.action, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_badge.short_description = 'অ্যাকশন'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name_bn',
        'name_en',
        'category',
        'subcategory',
        'service_type',
        'requires_booking',
        'supports_demand',
        'supports_location',
        'is_active',
        'is_featured',
        'sort_order',
    ]
    list_filter = [
        'category',
        'service_type',
        'is_active',
        'is_featured',
        'requires_booking',
        'supports_demand',
        'supports_delivery',
        'supports_location',
        'supports_online',
    ]
    search_fields = [
        'name_bn',
        'name_en',
        'slug',
        'short_description_bn',
        'short_description_en',
        'category__name_bn',
        'category__name_en'
    ]
    ordering = ['sort_order', 'name_bn']
    raw_id_fields = ['category', 'subcategory']
    filter_horizontal = ['secondary_categories']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured']

    @admin.action(description='নির্বাচিত সেবাসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='নির্বাচিত সেবাসমূহ নিষ্ক্রিয় করুন (Deactivate)')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='নির্বাচিত সেবাসমূহ ফিচার্ড করুন (Mark as Featured)')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='নির্বাচিত সেবাসমূহ ফিচার্ড থেকে বাদ দিন (Unmark Featured)')
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)

