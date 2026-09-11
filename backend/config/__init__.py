"""SebaCox Django Configuration Package."""
from workers.celery import app as celery_app

__all__ = ('celery_app',)
