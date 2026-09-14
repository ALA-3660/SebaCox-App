from django.apps import AppConfig


class MatchingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.matching'
    verbose_name = 'ম্যাচিং ইঞ্জিন (Matching Engine)'

    def ready(self):
        # Register domain event listeners
        try:
            from apps.demands.events import DemandEventDispatcher, DemandPublishedEvent
            from .events import handle_demand_published_event
            DemandEventDispatcher.register_handler(handle_demand_published_event)
        except Exception:
            pass
