"""
Asynchronous Tasks for SebaCox Matching Engine.
Phase 7: Celery/Worker Integration with Idempotent Fallbacks.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from celery import shared_task
except ImportError:
    # Fallback decorator if celery is not installed in the current environment
    def shared_task(func=None, **kwargs):
        if func is None:
            def decorator(f):
                f.delay = f
                return f
            return decorator
        func.delay = func
        return func


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def async_run_matching_task(self=None, demand_id: int = 0, trigger: str = 'DEMAND_PUBLISHED', version: str = 'v1'):
    """
    Asynchronous task executing the matching engine for a given Demand ID.
    Idempotent and resilient.
    """
    logger.info(f"Executing async_run_matching_task for Demand #{demand_id} (trigger={trigger}, version={version})")

    try:
        from apps.demands.models import Demand
        from .services import MatchingEngine

        if not hasattr(Demand, 'objects'):
            logger.info("Demand model has no objects manager in current environment. Skipping task.")
            return None

        demand = Demand.objects.filter(id=demand_id).first()
        if not demand:
            logger.warning(f"Demand #{demand_id} not found. Skipping matching run.")
            return None

        matching_run = MatchingEngine.run_matching(
            demand=demand,
            trigger=trigger,
            version=version
        )
        logger.info(f"Completed matching run #{matching_run.id} for Demand #{demand_id}: {matching_run.candidate_count} candidates found.")
        return matching_run.id

    except Exception as exc:
        logger.exception(f"Error in async_run_matching_task for Demand #{demand_id}: {exc}")
        if self and hasattr(self, 'retry'):
            raise self.retry(exc=exc)
        raise exc
