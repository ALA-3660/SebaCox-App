"""
Ranking Engine for SebaCox Matching.
Phase 7: Matching ≠ Ranking Separation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from typing import List, Dict, Any
from decimal import Decimal
from apps.providers.constants import AvailabilityStatus


class MatchRankingEngine:
    """
    Ranks eligible match candidates deterministically.
    
    Ranking Hierarchy:
    1. match_score (Descending)
    2. is_verified (Descending: Verified first)
    3. availability_status (Available > Busy > Offline)
    4. distance_km (Ascending: Closer first, None last)
    5. provider_id (Ascending: Tie-breaker for stable determinism)
    """

    @classmethod
    def rank_candidates(cls, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts candidates and assigns sequential 1-based rank.

        Args:
            candidates: List of candidate dictionaries containing:
                - 'provider_id': int
                - 'match_score': Decimal or float
                - 'is_verified': bool
                - 'availability_status': str
                - 'distance_km': Optional[float or Decimal]
                ... other fields

        Returns:
            Ranked list with 'rank' assigned.
        """
        def availability_priority(status: str) -> int:
            if status == AvailabilityStatus.AVAILABLE:
                return 3
            if status == AvailabilityStatus.BUSY:
                return 2
            return 1 # OFFLINE or others

        def sort_key(item):
            score = float(item.get('match_score', 0.0))
            is_verified = 1 if item.get('is_verified') else 0
            avail_prio = availability_priority(item.get('availability_status', ''))
            
            dist = item.get('distance_km')
            dist_val = float(dist) if dist is not None else 999999.0
            
            provider_id = item.get('provider_id', 0)

            # Sort tuple:
            # -score (descending)
            # -is_verified (descending)
            # -avail_prio (descending)
            # dist_val (ascending)
            # provider_id (ascending)
            return (-score, -is_verified, -avail_prio, dist_val, provider_id)

        sorted_candidates = sorted(candidates, key=sort_key)

        for index, candidate in enumerate(sorted_candidates, start=1):
            candidate['rank'] = index

        return sorted_candidates
