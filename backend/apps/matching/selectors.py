"""
Selectors for SebaCox Matching Engine.
Phase 7: High-Performance, Query-Optimized Candidate Selection.
Prevents N+1 database queries through select_related and prefetch_related.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from typing import Optional, List
from django.db.models import Q, QuerySet
from apps.providers.models import Provider, ProviderStatus
from apps.demands.models import Demand
from .models import MatchCandidate, MatchingRun
from .constants import MatchStatus


def get_candidate_providers_for_demand(demand: Demand) -> QuerySet:
    """
    Selects potential Provider candidates for a Demand based on Master Taxonomy.
    
    Query optimization:
    1. Filter only Provider.status = ACTIVE and is_active = True
    2. Filter providers having at least one active & available service matching demand's service, subcategory, or category
    3. Prefetch related service offerings and service areas to eliminate N+1 queries.
    """
    base_filter = Q(status=ProviderStatus.ACTIVE, is_active=True)

    taxonomy_or = Q()
    if demand.service_id:
        taxonomy_or |= Q(services__service_id=demand.service_id)
    if demand.subcategory_id:
        taxonomy_or |= Q(services__subcategory_id=demand.subcategory_id)
        taxonomy_or |= Q(services__service__subcategory_id=demand.subcategory_id)
    if demand.category_id:
        taxonomy_or |= Q(services__category_id=demand.category_id)
        taxonomy_or |= Q(services__service__category_id=demand.category_id)

    service_filter = Q(services__is_active=True, services__is_available=True)
    if taxonomy_or:
        service_filter &= taxonomy_or

    queryset = (
        Provider.objects.filter(base_filter)
        .filter(service_filter)
        .select_related('user')
        .prefetch_related(
            'services',
            'services__service',
            'services__subcategory',
            'services__category',
            'services__service__category',
            'services__service__subcategory',
            'service_areas',
            'service_areas__district',
            'service_areas__upazila',
            'service_areas__union',
            'service_areas__ward',
        )
        .distinct()
    )

    return queryset


def get_matches_for_demand(
    demand_id: int,
    status: Optional[str] = MatchStatus.ELIGIBLE,
    version: str = 'v1'
) -> QuerySet:
    """
    Retrieves ranked match candidates for a demand.
    """
    qs = (
        MatchCandidate.objects.filter(demand_id=demand_id, matching_version=version, is_active=True)
        .select_related(
            'provider',
            'provider_service',
            'provider_service__service',
            'matching_run'
        )
        .order_by('rank', '-match_score')
    )
    if status:
        qs = qs.filter(match_status=status)
    return qs


def get_match_detail(match_id: int) -> Optional[MatchCandidate]:
    """
    Retrieves a single match candidate with full relational context.
    """
    return (
        MatchCandidate.objects.select_related(
            'demand',
            'demand__requester',
            'provider',
            'provider__user',
            'provider_service',
            'provider_service__service',
            'matching_run'
        )
        .filter(id=match_id)
        .first()
    )
