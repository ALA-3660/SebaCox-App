"""
Django Admin for SebaCox Matching Engine.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
"""
from django.contrib import admin
from .models import MatchingRun, MatchCandidate


@admin.register(MatchingRun)
class MatchingRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'demand_id', 'version', 'trigger', 'status', 'candidate_count', 'execution_duration_ms', 'created_at')
    list_filter = ('status', 'version', 'trigger', 'created_at')
    search_fields = ('demand__id', 'demand__title_bn', 'error')
    readonly_fields = ('created_at', 'started_at', 'completed_at', 'execution_duration_ms')


@admin.register(MatchCandidate)
class MatchCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'demand_id', 'provider', 'match_status', 'match_score', 'rank', 'distance_km', 'is_active', 'created_at')
    list_filter = ('match_status', 'matching_version', 'is_active', 'created_at')
    search_fields = ('demand__id', 'provider__display_name_bn', 'provider__display_name_en')
    readonly_fields = ('created_at', 'updated_at')
