"""
Matching Engine Service Layer for SebaCox.
Phase 7: End-to-End Orchestration Pipeline.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import time
import logging
from typing import List, Dict, Any, Optional
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError

from apps.demands.models import Demand
from apps.demands.constants import DemandStatus
from apps.providers.models import Provider, ProviderService
from .models import MatchingRun, MatchCandidate
from .constants import (
    MatchStatus,
    MatchingRunStatus,
    MatchingTrigger,
    DEFAULT_ELIGIBILITY_SCORE_THRESHOLD,
)
from .rules import (
    DemandStatusRule,
    ProviderStatusRule,
    ProviderServiceStatusRule,
    ServiceMatchRule,
    LocationCoverageRule,
    ProviderAvailabilityRule,
    VerificationFactorRule,
    TimeCompatibilityRule,
)
from .scoring import MatchScoringCalculator
from .ranking import MatchRankingEngine
from .selectors import get_candidate_providers_for_demand
from .events import DemandMatchedEvent

logger = logging.getLogger(__name__)


class MatchingEngine:
    """
    Production-ready orchestration service for the SebaCox Matching Engine.
    
    Pipeline Steps:
    1. Demand Eligibility Validation
    2. Execution Run Audit Tracking
    3. Query-Optimized Candidate Selection
    4. Multi-Dimensional Eligibility Rules Evaluation
    5. Deterministic Server-Side Scoring (0-100)
    6. Multi-Factor Deterministic Ranking
    7. Idempotent Atomic Persistence
    8. Domain Event Notification
    """

    @classmethod
    def run_matching(
        cls,
        demand: Demand,
        trigger: str = MatchingTrigger.DEMAND_PUBLISHED,
        version: str = 'v1'
    ) -> MatchingRun:
        """
        Executes the matching pipeline for a given Demand.
        Guarantees idempotency and explainability.
        """
        start_time = time.time()
        now = timezone.now()

        # Step 1: Demand Eligibility Validation
        demand_eval = DemandStatusRule.evaluate(demand)
        if not demand_eval.is_eligible:
            logger.warning(f"Demand #{demand.id} is not eligible for matching: {demand_eval.explanation_bn}")
            # Mark existing candidates as EXPIRED or INELIGIBLE
            cls.invalidate_demand_matches(
                demand=demand,
                target_status=MatchStatus.EXPIRED if demand.status == DemandStatus.EXPIRED else MatchStatus.INELIGIBLE
            )
            # Record run as completed with 0 candidates
            run = MatchingRun.objects.create(
                demand=demand,
                version=version,
                trigger=trigger,
                status=MatchingRunStatus.COMPLETED,
                candidate_count=0,
                started_at=now,
                completed_at=now,
                execution_duration_ms=int((time.time() - start_time) * 1000),
                error=f"Demand not eligible for matching: {demand_eval.explanation_bn}"
            )
            return run

        # Step 2: Initialize MatchingRun
        run = MatchingRun.objects.create(
            demand=demand,
            version=version,
            trigger=trigger,
            status=MatchingRunStatus.RUNNING,
            started_at=now,
        )

        try:
            # Step 3: Select Candidate Providers
            potential_providers = get_candidate_providers_for_demand(demand)
            eligible_candidates_data = []

            # Step 4: Evaluate Eligibility & Score Each Provider
            for provider in potential_providers:
                # Rule 2: Provider Status
                p_status_eval = ProviderStatusRule.evaluate(provider)
                if not p_status_eval.is_eligible:
                    continue

                # Identify the most compatible ProviderService
                services = [s for s in provider.services.all() if s.is_active and s.is_available]
                if not services:
                    continue

                best_service_eval = None
                best_provider_service = None
                for ps in services:
                    s_eval = ServiceMatchRule.evaluate(demand, ps)
                    if s_eval.is_eligible:
                        # Prioritize EXACT over CATEGORY
                        if best_service_eval is None or s_eval.factor_code == 'SERVICE_EXACT':
                            best_service_eval = s_eval
                            best_provider_service = ps
                            if s_eval.factor_code == 'SERVICE_EXACT':
                                break

                if not best_service_eval or not best_service_eval.is_eligible:
                    continue

                # Rule 3: ProviderService Status
                ps_status_eval = ProviderServiceStatusRule.evaluate(best_provider_service)
                if not ps_status_eval.is_eligible:
                    continue

                # Rule 5: Location Coverage
                service_areas = list(provider.service_areas.all())
                loc_eval, computed_dist_km = LocationCoverageRule.evaluate(demand, service_areas)
                if not loc_eval.is_eligible:
                    continue

                # Rule 6: Availability Signal
                avail_eval = ProviderAvailabilityRule.evaluate(provider)

                # Rule 7: Verification Factor
                ver_eval = VerificationFactorRule.evaluate(provider)

                # Rule 8: Time Compatibility
                time_eval = TimeCompatibilityRule.evaluate(demand, provider)

                # Aggregate evaluations for scoring
                evaluations = [
                    best_service_eval,
                    loc_eval,
                    avail_eval,
                    ver_eval,
                    time_eval,
                ]

                # Step 5: Calculate Deterministic Score
                score_result = MatchScoringCalculator.calculate_score(evaluations)
                match_score = score_result['match_score']

                if float(match_score) >= DEFAULT_ELIGIBILITY_SCORE_THRESHOLD:
                    eligible_candidates_data.append({
                        'provider': provider,
                        'provider_id': provider.id,
                        'provider_service': best_provider_service,
                        'match_score': match_score,
                        'is_verified': provider.is_verified,
                        'availability_status': provider.availability_status,
                        'distance_km': Decimal(str(round(computed_dist_km, 2))) if computed_dist_km is not None else None,
                        'matched_factors': score_result['matched_factors'],
                        'unmatched_factors': score_result['unmatched_factors'],
                        'explanations_bn': score_result['explanations_bn'],
                    })

            # Step 6: Rank Candidates
            ranked_candidates = MatchRankingEngine.rank_candidates(eligible_candidates_data)

            # Step 7: Idempotent Atomic Persistence
            with transaction.atomic():
                active_provider_ids = set()

                for item in ranked_candidates:
                    p = item['provider']
                    active_provider_ids.add(p.id)

                    MatchCandidate.objects.update_or_create(
                        demand=demand,
                        provider=p,
                        matching_version=version,
                        defaults={
                            'matching_run': run,
                            'provider_service': item['provider_service'],
                            'match_status': MatchStatus.ELIGIBLE,
                            'match_score': item['match_score'],
                            'rank': item['rank'],
                            'distance_km': item['distance_km'],
                            'matched_factors': item['matched_factors'],
                            'unmatched_factors': item['unmatched_factors'],
                            'explanations_bn': item['explanations_bn'],
                            'is_active': True,
                        }
                    )

                # Deactivate or mark INELIGIBLE any candidates that previously matched this version but are no longer eligible
                MatchCandidate.objects.filter(
                    demand=demand,
                    matching_version=version,
                    is_active=True
                ).exclude(provider_id__in=active_provider_ids).update(
                    match_status=MatchStatus.INELIGIBLE,
                    is_active=False
                )

            # Step 8: Finalize MatchingRun
            duration_ms = int((time.time() - start_time) * 1000)
            run.status = MatchingRunStatus.COMPLETED
            run.completed_at = timezone.now()
            run.candidate_count = len(ranked_candidates)
            run.execution_duration_ms = duration_ms
            run.save(update_fields=['status', 'completed_at', 'candidate_count', 'execution_duration_ms'])

            # Step 9: Emit Domain Event
            top_score = float(ranked_candidates[0]['match_score']) if ranked_candidates else 0.0
            DemandMatchedEvent(
                demand_id=demand.id,
                requester_id=demand.requester_id,
                matching_run_id=run.id,
                candidates_count=len(ranked_candidates),
                top_score=top_score,
                version=version
            )

            return run

        except Exception as e:
            logger.exception(f"Matching run failed for Demand #{demand.id}: {e}")
            run.status = MatchingRunStatus.FAILED
            run.completed_at = timezone.now()
            run.error = str(e)
            run.execution_duration_ms = int((time.time() - start_time) * 1000)
            run.save(update_fields=['status', 'completed_at', 'error', 'execution_duration_ms'])
            raise e

    @classmethod
    def rematch_demand(cls, demand_id: int, user, version: str = 'v1') -> MatchingRun:
        """
        Manually re-triggers matching for a demand with authorization enforcement.
        Only demand requester or platform admin can trigger re-matching.
        """
        demand = Demand.objects.filter(id=demand_id).first()
        if not demand:
            raise ValidationError("প্রয়োজনটি পাওয়া যায়নি।")

        is_owner = (demand.requester_id == user.id)
        is_admin = getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False)

        if not (is_owner or is_admin):
            raise PermissionDenied("শুধুমাত্র অনুরোধকারী বা অ্যাডমিন পুনঃম্যাচিং করতে পারেন।")

        return cls.run_matching(
            demand=demand,
            trigger=MatchingTrigger.RE_MATCH,
            version=version
        )

    @classmethod
    def invalidate_demand_matches(cls, demand: Demand, target_status: str = MatchStatus.EXPIRED) -> int:
        """
        Invalidates existing matches when a demand is cancelled, expired, fulfilled, or closed.
        """
        count = MatchCandidate.objects.filter(
            demand=demand,
            is_active=True
        ).update(
            match_status=target_status,
            is_active=False,
            updated_at=timezone.now()
        )
        return count
