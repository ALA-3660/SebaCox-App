"""
Django Admin interface for Categories & Services.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Category, Service
from .constants import CategoryKind, ServiceType


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name_bn',
        'name_en',
        'slug',
        'parent',
        'level',
        'kind',
        'sort_order',
        'is_active',
        'is_featured',
    ]
    list_filter = ['is_active', 'is_featured', 'kind', 'level']
    search_fields = ['name_bn', 'name_en', 'slug', 'description_bn', 'description_en']
    ordering = ['level', 'sort_order', 'name_bn']
    raw_id_fields = ['parent']
    readonly_fields = ['level', 'created_at', 'updated_at']
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured']

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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name_bn',
        'name_en',
        'category',
        'service_type',
        'requires_booking',
        'supports_demand',
        'supports_location',
        'is_active',
        'is_featured',
        'sort_order',
    ]
    list_filter = [
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
    raw_id_fields = ['category']
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
