"""
Admin panel configuration for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.contrib import admin
from .models import Demand, DemandAuditLog


class DemandAuditLogInline(admin.TabularInline):
    model = DemandAuditLog
    extra = 0
    readonly_fields = ('action', 'from_status', 'to_status', 'message', 'actor', 'created_at')
    can_delete = False


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_bn',
        'requester',
        'demand_type',
        'status',
        'priority',
        'upazila',
        'visibility',
        'created_at',
    )
    list_filter = (
        'status',
        'demand_type',
        'priority',
        'visibility',
        'district',
        'upazila',
        'is_active',
        'is_deleted',
    )
    search_fields = (
        'title_bn',
        'title_en',
        'description_bn',
        'requester__phone',
        'requester__full_name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'published_at',
        'fulfilled_at',
        'cancelled_at',
        'closed_at',
    )
    inlines = [DemandAuditLogInline]


@admin.register(DemandAuditLog)
class DemandAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'demand', 'action', 'from_status', 'to_status', 'actor', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('demand__title_bn', 'actor__phone', 'message')
    readonly_fields = ('demand', 'actor', 'action', 'from_status', 'to_status', 'message', 'metadata', 'created_at')
