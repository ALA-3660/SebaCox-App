"""
Provider application configuration for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.providers'
    label = 'providers'
    verbose_name = 'SebaCox Provider & Service Provider Foundation'
