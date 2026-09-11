"""
Locations application configuration.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.locations'
    label = 'locations'
    verbose_name = 'SebaCox Location & Geographic Engine'
