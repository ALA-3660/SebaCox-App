"""
Scoring Calculator for SebaCox Matching Engine.
Phase 7: Deterministic Server-Side Scoring (0 - 100 Range).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from decimal import Decimal
from typing import Dict, Any, List, Optional
from .constants import (
    DEFAULT_SCORING_WEIGHTS,
    MAX_POSSIBLE_SCORE,
    MIN_POSSIBLE_SCORE,
    MatchFactorCode,
)
from .rules import RuleEvaluationResult


class MatchScoringCalculator:
    """
    Calculates deterministic, explainable match scores for eligible candidates.
    Never uses fake data or probabilistic hallucinations.
    """

    @classmethod
    def calculate_score(
        cls,
        evaluations: List[RuleEvaluationResult],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculates total score and builds structured matched/unmatched factor logs.

        Args:
            evaluations: List of RuleEvaluationResult instances from eligibility evaluation
            custom_weights: Optional override for scoring weights

        Returns:
            Dict containing:
            - 'match_score': Decimal (0.00 - 100.00)
            - 'matched_factors': Dict[str, Dict[str, Any]]
            - 'unmatched_factors': Dict[str, Dict[str, Any]]
            - 'explanations_bn': List[str]
        """
        weights = custom_weights or DEFAULT_SCORING_WEIGHTS
        total_score = 0.0

        matched_factors = {}
        unmatched_factors = {}
        explanations_bn = []

        for eval_res in evaluations:
            weight_key = eval_res.score_weight_key
            points = weights.get(weight_key, 0.0)

            factor_data = {
                'rule': eval_res.rule_name,
                'factor_code': eval_res.factor_code,
                'points': points,
                'details': eval_res.details,
            }

            if points > 0.0:
                total_score += points
                matched_factors[eval_res.factor_code] = factor_data
                if eval_res.explanation_bn:
                    explanations_bn.append(eval_res.explanation_bn)
            else:
                unmatched_factors[eval_res.factor_code] = factor_data
                if eval_res.explanation_bn and not eval_res.is_eligible:
                    explanations_bn.append(eval_res.explanation_bn)

        # Enforce boundary bounds
        final_score = max(MIN_POSSIBLE_SCORE, min(MAX_POSSIBLE_SCORE, total_score))
        decimal_score = Decimal(str(round(final_score, 2)))

        return {
            'match_score': decimal_score,
            'matched_factors': matched_factors,
            'unmatched_factors': unmatched_factors,
            'explanations_bn': explanations_bn,
        }
