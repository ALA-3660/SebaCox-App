"""
Asynchronous & Scheduled Tasks for SebaCox Offers Engine.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from celery import shared_task
except ImportError:
    # Fallback decorator if celery is not installed in current environment
    def shared_task(func=None, **kwargs):
        if func is None:
            def decorator(f):
                f.delay = f
                return f
            return decorator
        func.delay = func
        return func


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def expire_pending_offers_task(self=None):
    """
    Idempotent periodic task that finds all PENDING offers where expires_at <= timezone.now()
    and transitions them to EXPIRED status, creating audit logs and dispatching domain events.
    """
    logger.info("Executing expire_pending_offers_task...")
    try:
        from .services import OfferService
        count = OfferService.expire_pending_offers()
        logger.info(f"expire_pending_offers_task finished: {count} offers marked as EXPIRED.")
        return count
    except Exception as exc:
        logger.exception(f"Error in expire_pending_offers_task: {exc}")
        if self and hasattr(self, 'retry'):
            raise self.retry(exc=exc)
        raise exc


# Alias for scheduled cron dispatcher
auto_expire_pending_offers_task = expire_pending_offers_task
