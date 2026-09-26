"""
Unit and Integration Tests for Taxonomy Governance, Versioning & Lifecycle (Phase 4D).
Tests impact analysis, atomic merges, alias preservation, no hard deletes, versioning and audit trails.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.categories.models import Category, SubCategory, Service, TaxonomyAlias, TaxonomyVersion, TaxonomyChangeLog
from apps.categories.constants import TaxonomyStatus, TaxonomyActionType, AliasTargetType
from apps.categories.governance import TaxonomyGovernanceService
from apps.providers.models import Provider, ProviderService
from apps.demands.models import Demand

User = get_user_model()


class TaxonomyGovernanceServiceTests(TestCase):
    """Test core business logic of Taxonomy Governance Service."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            phone_number="+8801811111111",
            password="adminpassword123",
            name="Admin User"
        )
        self.cat1 = Category.objects.create(
            name_bn="ইলেকট্রিক্যাল ও ইলেকট্রনিক্স",
            name_en="Electrical & Electronics",
            slug="electrical-electronics",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=1
        )
        self.cat2 = Category.objects.create(
            name_bn="গৃহস্থালি ও যন্ত্র মেরামত",
            name_en="Home & Appliance Repair",
            slug="home-appliance-repair",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=2
        )
        self.sub1 = SubCategory.objects.create(
            category=self.cat1,
            name_bn="বাসাবাড়ি ওয়্যারিং",
            name_en="House Wiring",
            slug="house-wiring",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=1
        )
        self.sub2 = SubCategory.objects.create(
            category=self.cat2,
            name_bn="ফ্রিজ ও এসি মেরামত",
            name_en="Fridge & AC Repair",
            slug="fridge-ac-repair",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=1
        )
        self.service1 = Service.objects.create(
            category=self.cat1,
            subcategory=self.sub1,
            name_bn="ওয়্যারিং সার্ভিস",
            name_en="Wiring Service",
            slug="wiring-service",
            is_active=True
        )

    def test_no_hard_delete_when_relations_exist(self):
        """Deleting category/subcategory with active services must raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.cat1.delete()

        with self.assertRaises(ValidationError):
            self.sub1.delete()

    def test_safe_deactivation(self):
        """Deactivating Category updates status and logs action."""
        cat = TaxonomyGovernanceService.deactivate_category(
            category_id=self.cat1.id,
            reason="Temporary administrative pause",
            user=self.admin_user
        )
        self.assertEqual(cat.status, TaxonomyStatus.INACTIVE)
        self.assertFalse(cat.is_active)

        # Check changelog
        log = TaxonomyChangeLog.objects.filter(target_id=self.cat1.id, action=TaxonomyActionType.DEACTIVATE).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.changed_by, self.admin_user)

    def test_safe_reactivation(self):
        """Reactivating Category updates status to ACTIVE."""
        self.cat1.status = TaxonomyStatus.INACTIVE
        self.cat1.is_active = False
        self.cat1.save()

        cat = TaxonomyGovernanceService.reactivate_category(
            category_id=self.cat1.id,
            reason="Resumed operations",
            user=self.admin_user
        )
        self.assertEqual(cat.status, TaxonomyStatus.ACTIVE)
        self.assertTrue(cat.is_active)

    def test_rename_preserves_search_alias(self):
        """Renaming a category preserves previous names as searchable aliases."""
        old_bn = self.cat1.name_bn
        old_en = self.cat1.name_en

        updated_cat = TaxonomyGovernanceService.rename_category(
            category_id=self.cat1.id,
            name_bn="বিদ্যুৎ ও ইলেকট্রিক্যাল",
            name_en="Electricity & Electrical",
            reason="Brand refinement",
            user=self.admin_user,
            preserve_alias=True
        )

        self.assertEqual(updated_cat.name_bn, "বিদ্যুৎ ও ইলেকট্রিক্যাল")

        # Verify search aliases were created for old names
        alias_bn = TaxonomyAlias.objects.filter(
            alias_text=old_bn,
            target_type=AliasTargetType.CATEGORY,
            target_id=self.cat1.id
        ).first()
        self.assertIsNotNone(alias_bn)

        alias_en = TaxonomyAlias.objects.filter(
            alias_text=old_en,
            target_type=AliasTargetType.CATEGORY,
            target_id=self.cat1.id
        ).first()
        self.assertIsNotNone(alias_en)

    def test_deprecation_with_replacement(self):
        """Deprecating category attaches replacement reference and reason."""
        deprecated_cat = TaxonomyGovernanceService.deprecate_category(
            category_id=self.cat1.id,
            reason="Merged into Home Repair",
            replacement_id=self.cat2.id,
            user=self.admin_user
        )
        self.assertEqual(deprecated_cat.status, TaxonomyStatus.DEPRECATED)
        self.assertFalse(deprecated_cat.is_active)
        self.assertEqual(deprecated_cat.replacement_id, self.cat2.id)

    def test_atomic_category_merge(self):
        """Merging Category A into Category B re-maps subcategories, services, and aliases."""
        summary = TaxonomyGovernanceService.merge_category(
            source_category_id=self.cat1.id,
            target_category_id=self.cat2.id,
            reason="Taxonomy consolidation v1.1",
            user=self.admin_user
        )

        self.assertEqual(summary['subcategories_remapped'], 1)
        self.assertEqual(summary['services_remapped'], 1)

        # Re-fetch source and relations
        self.cat1.refresh_from_db()
        self.sub1.refresh_from_db()
        self.service1.refresh_from_db()

        self.assertEqual(self.cat1.status, TaxonomyStatus.MERGED)
        self.assertFalse(self.cat1.is_active)
        self.assertEqual(self.cat1.merged_into_id, self.cat2.id)
        self.assertEqual(self.sub1.category_id, self.cat2.id)
        self.assertEqual(self.service1.category_id, self.cat2.id)

    def test_move_subcategory(self):
        """Moving SubCategory from Cat1 to Cat2 updates category pointer and dependent services."""
        moved_sub = TaxonomyGovernanceService.move_subcategory(
            subcategory_id=self.sub1.id,
            new_category_id=self.cat2.id,
            reason="Organizational restructuring",
            user=self.admin_user
        )
        self.assertEqual(moved_sub.category_id, self.cat2.id)

        self.service1.refresh_from_db()
        self.assertEqual(self.service1.category_id, self.cat2.id)

    def test_version_bump_and_checksum(self):
        """Publishing a new version sets is_current=True and computes checksum."""
        v1 = TaxonomyGovernanceService.bump_taxonomy_version(
            version_number="1.1",
            release_title="Cox's Bazar 2026 Taxonomy Refresh",
            description="Expanded electrical and plumbing categories",
            changelog=["Added 2 new subcategories", "Merged legacy electronics"],
            user=self.admin_user
        )
        self.assertEqual(v1.version_number, "1.1")
        self.assertTrue(v1.is_current)
        self.assertTrue(v1.checksum.startswith("tax-v1.1-"))

        # Old versions should have is_current=False
        v2 = TaxonomyGovernanceService.bump_taxonomy_version(
            version_number="1.2",
            release_title="Cox's Bazar Version 1.2",
            user=self.admin_user
        )
        v1.refresh_from_db()
        self.assertFalse(v1.is_current)
        self.assertTrue(v2.is_current)


class TaxonomyGovernanceAPITests(APITestCase):
    """Test REST API endpoints for Taxonomy Governance and Versioning."""

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            phone_number="+8801822222222",
            password="adminpassword123",
            name="Admin User"
        )
        self.regular_user = User.objects.create_user(
            phone_number="+8801833333333",
            password="userpassword123",
            name="Regular User"
        )
        self.cat1 = Category.objects.create(
            name_bn="কৃষি ও খামার",
            name_en="Agriculture & Farming",
            slug="agriculture-farming",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=1
        )
        self.cat2 = Category.objects.create(
            name_bn="মৎস্য ও সামুদ্রিক",
            name_en="Fisheries & Marine",
            slug="fisheries-marine",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=2
        )
        self.sub1 = SubCategory.objects.create(
            category=self.cat1,
            name_bn="সার ও কীটনাশক প্রয়োগ",
            name_en="Fertilizer Application",
            slug="fertilizer-application",
            status=TaxonomyStatus.ACTIVE,
            is_active=True,
            sort_order=1
        )

    def test_public_manifest_endpoint(self):
        """Anonymous clients can query manifest for cache validation."""
        url = reverse('categories:taxonomy-manifest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('checksum', response.data['data'])
        self.assertIn('total_categories', response.data['data'])

    def test_admin_impact_analysis_endpoint(self):
        """Staff can fetch impact analysis before mutations."""
        url = reverse('categories:taxonomy-impact')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url, {'target_type': 'CATEGORY', 'target_id': self.cat1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['target_id'], self.cat1.id)
        self.assertEqual(response.data['data']['subcategories_count'], 1)

    def test_regular_user_forbidden_from_governance_actions(self):
        """Regular unprivileged users cannot execute governance mutations."""
        url = reverse('categories:taxonomy-deactivate')
        self.client.force_authenticate(user=self.regular_user)
        payload = {
            'target_type': 'CATEGORY',
            'target_id': self.cat1.id,
            'reason': 'Attempted unauthorized mutation'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_deactivate_and_audit_log(self):
        """Admin deactivates category via REST and log is generated."""
        url = reverse('categories:taxonomy-deactivate')
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'target_type': 'CATEGORY',
            'target_id': self.cat1.id,
            'reason': 'Seasonal suspension'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['data']['is_active'])

        # Check audit log API
        log_url = reverse('categories:taxonomy-audit-logs')
        log_response = self.client.get(log_url)
        self.assertEqual(log_response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(log_response.data['data']) > 0)
