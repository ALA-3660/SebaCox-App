"""
Django Admin Configuration for SebaCox Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.contrib import admin
from .models import Provider, ProviderService, ProviderServiceArea, ProviderAuditLog


class ProviderServiceInline(admin.TabularInline):
    model = ProviderService
    extra = 1
    fields = ('service', 'title_bn', 'starting_price', 'price_type', 'is_available', 'is_active')


class ProviderServiceAreaInline(admin.TabularInline):
    model = ProviderServiceArea
    extra = 1
    fields = ('area_type', 'district', 'upazila', 'union', 'radius_km', 'is_active')


class ProviderAuditLogInLine(admin.TabularInline):
    model = ProviderAuditLog
    extra = 0
    readonly_fields = ('actor', 'action', 'from_state', 'to_state', 'note', 'created_at')
    can_delete = False


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'display_name_bn',
        'display_name_en',
        'provider_type',
        'status',
        'is_verified',
        'verification_status',
        'availability_status',
        'is_featured',
        'is_active',
        'created_at',
    )
    list_filter = (
        'status',
        'provider_type',
        'is_verified',
        'verification_status',
        'availability_status',
        'is_featured',
        'is_active',
    )
    search_fields = ('display_name_bn', 'display_name_en', 'slug', 'user__mobile_number', 'contact_phone')
    prepopulated_fields = {'slug': ('display_name_en',)}
    inlines = [ProviderServiceInline, ProviderServiceAreaInline, ProviderAuditLogInLine]


@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = ('provider', 'service', 'title_bn', 'starting_price', 'is_available', 'is_active')
    list_filter = ('is_available', 'is_active', 'price_type')
    search_fields = ('provider__display_name_bn', 'service__name_bn', 'title_bn')


@admin.register(ProviderServiceArea)
class ProviderServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('provider', 'area_type', 'district', 'upazila', 'union', 'is_active')
    list_filter = ('area_type', 'is_active', 'district', 'upazila')
    search_fields = ('provider__display_name_bn', 'upazila__name_bn', 'district__name_bn')


@admin.register(ProviderAuditLog)
class ProviderAuditLogAdmin(admin.ModelAdmin):
    list_display = ('provider', 'action', 'actor', 'from_state', 'to_state', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('provider__display_name_bn', 'note', 'actor__mobile_number')
    readonly_fields = ('provider', 'actor', 'action', 'from_state', 'to_state', 'note', 'created_at')
