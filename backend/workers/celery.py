"""
Celery Application Initialization for SebaCox.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Configures asynchronous task execution, scheduled jobs, and Redis message broker.
"""
import os
from celery import Celery

# Set default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('sebacox')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix in settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Sanity check worker task."""
    print(f'SebaCox Worker Task Request: {self.request!r}')
