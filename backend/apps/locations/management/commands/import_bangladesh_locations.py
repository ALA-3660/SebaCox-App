"""
Django management command to import verified Bangladesh administrative datasets.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Usage:
  python manage.py import_bangladesh_locations --file=/path/to/bbs_dataset.json
"""
import json
import os
from django.core.management.base import BaseCommand, CommandError
from apps.locations.models import (
    Country, Division, District, Upazila, Municipality, Union, Ward, Locality
)
from apps.locations.services import BangladeshLocationImportService


class Command(BaseCommand):
    help = 'Imports verified Bangladesh administrative geographic hierarchy from a validated JSON data file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to verified JSON file containing BBS/government geographic hierarchy.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate records and schema without persisting to the database.'
        )

    def handle(self, *args, **options):
        file_path = options.get('file')
        dry_run = options.get('dry_run', False)

        if not file_path:
            self.stdout.write(self.style.WARNING(
                "Notice: No dataset file provided. A verified dataset file path is required.\n"
                "Example: python manage.py import_bangladesh_locations --file=/path/to/bbs_dataset.json\n"
                "In accordance with SebaCox Phase 3 architectural policy, no fake or fabricated\n"
                "records will be automatically generated."
            ))
            return

        if not os.path.exists(file_path):
            raise CommandError(f"Dataset file not found at: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise CommandError(f"Failed to read or parse JSON file: {e}")

        # Validate structure
        if not isinstance(data, dict) or 'country' not in data:
            raise CommandError("Invalid dataset structure. Root must contain 'country' object.")

        self.stdout.write(f"Validating dataset from: {file_path} (dry_run={dry_run})")

        # 1. Country
        country_data = data['country']
        valid, errors = BangladeshLocationImportService.validate_record(country_data, 'Country')
        if not valid:
            raise CommandError(f"Validation failed: {', '.join(errors)}")

        if not dry_run:
            country = BangladeshLocationImportService.import_country(country_data)
            self.stdout.write(self.style.SUCCESS(f"Imported Country: {country.name_en} ({country.code})"))

        self.stdout.write(self.style.SUCCESS("Dataset ingestion pipeline verified successfully."))
