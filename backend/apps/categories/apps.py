"""
Categories & Services application configuration.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.categories'
    label = 'categories'
    verbose_name = 'SebaCox Category & Service Engine'
