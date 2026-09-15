"""
Django Admin interface for Categories, SubCategories, Services & Taxonomy Aliases.
Master Taxonomy v1.0
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.contrib import admin
from .models import Category, SubCategory, Service, TaxonomyAlias
from .constants import CategoryKind, ServiceType


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ['name_bn', 'name_en', 'slug', 'sort_order', 'is_popular', 'is_active']
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
        'is_active',
        'is_popular',
        'is_featured',
    ]
    list_filter = ['is_active', 'is_popular', 'is_featured', 'kind', 'level']
    search_fields = ['name_bn', 'name_en', 'slug', 'description_bn', 'description_en']
    ordering = ['sort_order', 'name_bn']
    readonly_fields = ['level', 'created_at', 'updated_at']
    inlines = [SubCategoryInline]
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured']

    def subcategories_count(self, obj):
        return obj.subcategories.count()
    subcategories_count.short_description = 'সাব-ক্যাটাগরি সংখ্যা'

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='নির্বাচিত ক্যাটাগরিসমূহ নিষ্ক্রিয় করুন (Deactivate)')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

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
        'is_popular',
        'is_active',
    ]
    list_filter = ['category', 'is_popular', 'is_active']
    search_fields = ['name_bn', 'name_en', 'slug', 'category__name_bn', 'category__name_en']
    ordering = ['category__sort_order', 'sort_order', 'name_bn']
    raw_id_fields = ['category']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['make_active', 'make_inactive']

    @admin.action(description='নির্বাচিত সাব-ক্যাটাগরিসমূহ সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='নির্বাচিত সাব-ক্যাটাগরিসমূহ নিষ্ক্রিয় করুন (Deactivate)')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(TaxonomyAlias)
class TaxonomyAliasAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'alias_text',
        'normalized_text',
        'target_type',
        'target_id',
        'category',
        'subcategory',
        'language',
        'is_active',
    ]
    list_filter = ['target_type', 'language', 'is_active', 'category']
    search_fields = ['alias_text', 'normalized_text']
    raw_id_fields = ['category', 'subcategory']


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
