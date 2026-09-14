"""
Domain Events for SebaCox Offers.
Phase 8: Offer & Counter-Offer Foundation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BaseOfferEvent:
    offer_id: int
    demand_id: int
    provider_id: int
    requester_id: int
    proposer_id: int
    version: int
    total_amount: str # stringified Decimal for json serialization
    currency: str = "BDT"
    timestamp: str = ""
    event_type: str = "offer.event"


@dataclass(frozen=True)
class OfferCreatedEvent(BaseOfferEvent):
    event_type: str = "offer.created"
    status: str = "PENDING"
    expires_at: str = ""


@dataclass(frozen=True)
class OfferCounteredEvent(BaseOfferEvent):
    parent_offer_id: int = 0
    root_offer_id: int = 0
    event_type: str = "offer.countered"


@dataclass(frozen=True)
class OfferAcceptedEvent(BaseOfferEvent):
    accepted_by_id: int = 0
    event_type: str = "offer.accepted"


@dataclass(frozen=True)
class OfferRejectedEvent(BaseOfferEvent):
    rejection_reason_bn: str = ""
    rejected_by_id: int = 0
    event_type: str = "offer.rejected"


@dataclass(frozen=True)
class OfferCancelledEvent(BaseOfferEvent):
    cancellation_reason_bn: str = ""
    cancelled_by_id: int = 0
    event_type: str = "offer.cancelled"


@dataclass(frozen=True)
class OfferExpiredEvent(BaseOfferEvent):
    event_type: str = "offer.expired"


@dataclass(frozen=True)
class OfferSupersededEvent(BaseOfferEvent):
    superseded_by_offer_id: int = 0
    event_type: str = "offer.superseded"


# In-memory registry for domain event listeners
_OFFER_EVENT_LISTENERS = []


def register_offer_event_listener(listener):
    """Register a listener for offer domain events."""
    if listener not in _OFFER_EVENT_LISTENERS:
        _OFFER_EVENT_LISTENERS.append(listener)


def dispatch_offer_event(event: BaseOfferEvent):
    """
    Dispatches offer domain events to registered listeners and system logger.
    Prepares for future Notification Engine and Deal Engine integration.
    """
    event_data = asdict(event)
    logger.info(f"[DOMAIN EVENT] {event.event_type}: Offer #{event.offer_id} (Demand #{event.demand_id})")

    for listener in _OFFER_EVENT_LISTENERS:
        try:
            listener(event)
        except Exception as e:
            logger.error(f"Error in offer event listener {listener}: {e}", exc_info=True)

    return event_data
