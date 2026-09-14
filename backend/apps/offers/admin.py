"""
Admin Configuration for Offers.
Phase 8: Offer & Counter-Offer Foundation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.contrib import admin
from .models import Offer, OfferAuditLog


class OfferAuditLogInline(admin.TabularInline):
    model = OfferAuditLog
    extra = 0
    readonly_fields = ('actor', 'action', 'previous_status', 'new_status', 'metadata', 'created_at')
    can_delete = False


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'demand',
        'provider',
        'requester',
        'proposer',
        'version',
        'offer_type',
        'status',
        'price',
        'total_amount',
        'currency',
        'proposed_at',
        'expires_at',
    )
    list_filter = ('status', 'offer_type', 'currency', 'created_at')
    search_fields = ('title_bn', 'demand__title_bn', 'provider__business_name_bn', 'requester__phone_number')
    readonly_fields = ('total_amount', 'proposed_at', 'accepted_at', 'rejected_at', 'cancelled_at', 'created_at', 'updated_at')
    inlines = [OfferAuditLogInline]


@admin.register(OfferAuditLog)
class OfferAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer', 'actor', 'action', 'previous_status', 'new_status', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('offer__id', 'actor__phone_number', 'metadata')
    readonly_fields = ('offer', 'actor', 'action', 'previous_status', 'new_status', 'metadata', 'created_at')
