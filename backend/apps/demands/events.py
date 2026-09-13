"""
Domain Events for SebaCox Demand Engine.
Event-ready foundation for future Notification, Analytics, and Audit modules.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class DemandBaseEvent:
    demand_id: int
    requester_id: int
    status: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DemandCreatedEvent(DemandBaseEvent):
    event_type: str = "demand.created"


@dataclass
class DemandUpdatedEvent(DemandBaseEvent):
    event_type: str = "demand.updated"


@dataclass
class DemandPublishedEvent(DemandBaseEvent):
    event_type: str = "demand.published"


@dataclass
class DemandPausedEvent(DemandBaseEvent):
    event_type: str = "demand.paused"


@dataclass
class DemandResumedEvent(DemandBaseEvent):
    event_type: str = "demand.resumed"


@dataclass
class DemandCancelledEvent(DemandBaseEvent):
    event_type: str = "demand.cancelled"


@dataclass
class DemandFulfilledEvent(DemandBaseEvent):
    event_type: str = "demand.fulfilled"


@dataclass
class DemandExpiredEvent(DemandBaseEvent):
    event_type: str = "demand.expired"


@dataclass
class DemandClosedEvent(DemandBaseEvent):
    event_type: str = "demand.closed"


class DemandEventDispatcher:
    """
    Lightweight Domain Event Dispatcher.
    Keeps audit and future notification listeners decoupled.
    """
    _handlers = []

    @classmethod
    def register_handler(cls, handler):
        cls._handlers.append(handler)

    @classmethod
    def clear_handlers(cls):
        cls._handlers = []

    @classmethod
    def dispatch(cls, event: DemandBaseEvent):
        for handler in cls._handlers:
            try:
                handler(event)
            except Exception:
                pass
