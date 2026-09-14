"""
Domain Events for SebaCox Matching Engine.
Phase 7: Event-driven decoupling & Demand publication triggers.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class DemandMatchedEvent:
    """
    Domain event emitted when a demand has been analyzed and matched with eligible providers.
    """
    demand_id: int
    requester_id: int
    matching_run_id: Optional[int]
    candidates_count: int
    top_score: float
    version: str = "v1"
    event_type: str = "demand.matched"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


def handle_demand_published_event(event) -> None:
    """
    Event listener triggered when a Demand transitions to PUBLISHED.
    Initiates the matching engine for the published demand.
    """
    if getattr(event, 'event_type', '') != 'demand.published':
        return

    demand_id = getattr(event, 'demand_id', None)
    if not demand_id:
        return

    logger.info(f"Received DemandPublishedEvent for demand #{demand_id}. Triggering matching engine.")

    # Execute matching asynchronously if Celery is available, else invoke service directly
    try:
        from .tasks import async_run_matching_task
        async_run_matching_task(demand_id=demand_id, trigger='DEMAND_PUBLISHED', version='v1')
    except Exception as e:
        logger.error(f"Failed to trigger matching task for demand #{demand_id}: {e}")
