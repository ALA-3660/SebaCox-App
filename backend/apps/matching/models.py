"""
Matching Models for SebaCox.
Phase 7: Matching Engine Foundation.
Architecture: Demand -> Matching Engine -> Eligible Candidates (Provider References)
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from .constants import (
    MatchStatus,
    MatchingRunStatus,
    MatchingTrigger,
)


class MatchingRun(models.Model):
    """
    Execution run audit record for tracking matching engine invocations.
    Allows asynchronous execution tracking, versioned policy runs, and performance telemetry.
    """
    id = models.BigAutoField(primary_key=True)
    demand = models.ForeignKey(
        'demands.Demand',
        on_delete=models.CASCADE,
        related_name='matching_runs',
        db_index=True,
        help_text="যে প্রয়োজনের জন্য ম্যাচিং রান সম্পন্ন হয়েছে"
    )
    version = models.CharField(
        max_length=20,
        default='v1',
        db_index=True,
        help_text="ম্যাচিং পলিসি সংস্করণ (e.g. v1, v2)"
    )
    trigger = models.CharField(
        max_length=30,
        choices=MatchingTrigger.choices,
        default=MatchingTrigger.DEMAND_PUBLISHED,
        db_index=True,
        help_text="রান শুরুর উৎস"
    )
    status = models.CharField(
        max_length=30,
        choices=MatchingRunStatus.choices,
        default=MatchingRunStatus.PENDING,
        db_index=True,
        help_text="রানের অবস্থা (PENDING, RUNNING, COMPLETED, FAILED)"
    )
    candidate_count = models.PositiveIntegerField(
        default=0,
        help_text="মোট প্রাপ্ত উপযুক্ত প্রোভাইডার সংখ্যা"
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="রান শুরুর সময়"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="রান সমাপ্তির সময়"
    )
    execution_duration_ms = models.IntegerField(
        null=True,
        blank=True,
        help_text="রান সময়কাল (মিলিসেকেন্ড)"
    )
    error = models.TextField(
        blank=True,
        default='',
        help_text="ব্যর্থতার বিবরণ (যদি ঘটে)"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="অতিরিক্ত রান কনটেক্সট বা প্যারামিটার"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ম্যাচিং রান (Matching Run)'
        verbose_name_plural = 'ম্যাচিং রানসমূহ (Matching Runs)'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['demand', 'status']),
            models.Index(fields=['version', 'status']),
        ]

    def __str__(self):
        return f"MatchingRun #{self.id} for Demand #{self.demand_id} [{self.get_status_display()}]"


class MatchCandidate(models.Model):
    """
    Candidate match record connecting a Demand to an Eligible Provider.
    
    Architectural Principles:
    1. Reference, do NOT duplicate Provider data.
    2. Matching ≠ Ranking: stores separate score and rank.
    3. Idempotent: Unique on (demand, provider, matching_version).
    4. Explainable: stores structured matched/unmatched factors and Bengali explanations.
    5. Zero fake data: no artificial ratings or reviews.
    """
    id = models.BigAutoField(primary_key=True)
    matching_run = models.ForeignKey(
        MatchingRun,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candidates',
        help_text="সংশ্লিষ্ট ম্যাচিং রান"
    )
    demand = models.ForeignKey(
        'demands.Demand',
        on_delete=models.CASCADE,
        related_name='match_candidates',
        db_index=True,
        help_text="প্রয়োজন রেফারেন্স (Demand)"
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.CASCADE,
        related_name='demand_matches',
        db_index=True,
        help_text="উপযুক্ত সেবাদাতা রেফারেন্স (Provider)"
    )
    provider_service = models.ForeignKey(
        'providers.ProviderService',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demand_matches',
        help_text="নির্দিষ্ট অফারিং সেবা রেফারেন্স (যদি প্রযোজ্য)"
    )
    matching_version = models.CharField(
        max_length=20,
        default='v1',
        db_index=True,
        help_text="পলিসি সংস্করণ"
    )
    match_status = models.CharField(
        max_length=30,
        choices=MatchStatus.choices,
        default=MatchStatus.ELIGIBLE,
        db_index=True,
        help_text="প্রার্থীর অবস্থা (CANDIDATE, ELIGIBLE, INELIGIBLE, DISMISSED, EXPIRED)"
    )
    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        db_index=True,
        help_text="সার্ভার-সাইড নির্ধারিত সামগ্রিক স্কোর (০-১০০)"
    )
    rank = models.PositiveIntegerField(
        default=1,
        db_index=True,
        help_text="তালিকাভুক্ত ক্রম বা র‍্যাংক"
    )
    distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="দূরত্ব কিলোমিটারে (যদি প্রযোজ্য ও হিসাবযোগ্য হয়)"
    )
    matched_factors = models.JSONField(
        default=dict,
        blank=True,
        help_text="সন্তুষ্ট ম্যাচিং ফ্যাক্টর কোড ও স্কোর"
    )
    unmatched_factors = models.JSONField(
        default=dict,
        blank=True,
        help_text="অনুপস্থিত বা অপর্যাপ্ত ফ্যাক্টর"
    )
    explanations_bn = models.JSONField(
        default=list,
        blank=True,
        help_text="ব্যবহারকারীর জন্য বাংলা ব্যাখ্যা পয়েন্টসমূহ"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="সক্রিয় ম্যাচিং রেকর্ড কিনা"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ম্যাচ ক্যান্ডিডেট (Match Candidate)'
        verbose_name_plural = 'ম্যাচ ক্যান্ডিডেটগণ (Match Candidates)'
        ordering = ['rank', '-match_score', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['demand', 'provider', 'matching_version'],
                name='unique_demand_provider_matching_version'
            )
        ]
        indexes = [
            models.Index(fields=['demand', 'match_status', 'rank']),
            models.Index(fields=['provider', 'match_status']),
            models.Index(fields=['matching_version', 'match_score']),
        ]

    def __str__(self):
        return f"Match #{self.id} | Demand #{self.demand_id} <-> Provider #{self.provider_id} ({self.match_score} pts, Rank #{self.rank})"
