"""
Django Management Command for SebaCox Master Taxonomy v1.0 Migration.
Phase 4H: Existing Data Migration & Taxonomy Compatibility Verification.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import json
from django.core.management.base import BaseCommand
from apps.categories.migration_engine import TaxonomyMigrationEngine


class Command(BaseCommand):
    help = 'Executes deterministic and non-destructive Master Taxonomy v1.0 Migration for SebaCox.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulates migration without committing changes to database.',
        )
        parser.add_argument(
            '--inventory-only',
            action='store_true',
            help='Collects and outputs the existing data inventory report without migration.',
        )
        parser.add_argument(
            '--export-report',
            type=str,
            help='File path to export the migration JSON report.',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        inventory_only = options.get('inventory_only', False)
        export_path = options.get('export_report')

        if inventory_only:
            self.stdout.write(self.style.SUCCESS("Collecting Existing Data Inventory..."))
            report = TaxonomyMigrationEngine.get_existing_data_inventory()
            self.stdout.write(json.dumps(report, indent=2, ensure_ascii=False))
            if export_path:
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                self.stdout.write(self.style.SUCCESS(f"Inventory report exported to {export_path}"))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING("Running Master Taxonomy v1.0 Migration DRY RUN..."))
            result = TaxonomyMigrationEngine.dry_run()
            self.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
            if export_path:
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                self.stdout.write(self.style.SUCCESS(f"Dry run report exported to {export_path}"))
            return

        self.stdout.write(self.style.NOTICE("Executing LIVE Master Taxonomy v1.0 Migration..."))
        result = TaxonomyMigrationEngine.execute_migration()
        self.stdout.write(self.style.SUCCESS("Migration Completed Successfully!"))
        self.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))

        if export_path:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            self.stdout.write(self.style.SUCCESS(f"Migration report exported to {export_path}"))
