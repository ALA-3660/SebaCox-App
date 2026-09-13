"""
Demands AppConfig for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.apps import AppConfig


class DemandsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.demands'
    verbose_name = 'আমার প্রয়োজন (Demands Engine)'
