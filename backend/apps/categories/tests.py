"""
Unit and Integration Tests for SebaCox Master Taxonomy v1.0.
Universal Category, SubCategory, Cascading Relations and Search Aliases.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.categories.models import Category, SubCategory, Service, TaxonomyAlias
from apps.categories.constants import CategoryKind, SEBACOX_31_MASTER_CATEGORIES
from apps.categories.services import TaxonomySeedService, TaxonomySearchService


class MasterTaxonomyModelTests(TestCase):
    """Test model constraints, relationships, and validation."""

    def setUp(self):
        self.category = Category.objects.create(
            name_bn="নির্মাণ ও প্রকৌশল",
            name_en="Construction & Engineering",
            slug="construction-engineering",
            sort_order=1,
            is_active=True
        )

    def test_subcategory_creation_and_cascade(self):
        sub = SubCategory.objects.create(
            category=self.category,
            name_bn="নির্মাণ শ্রমিক ও মিস্ত্রি",
            name_en="Masonry & Casting Labour",
            slug="masonry-casting-labour",
            sort_order=1,
            is_active=True
        )
        self.assertEqual(sub.category.slug, "construction-engineering")
        self.assertEqual(self.category.subcategories.count(), 1)
        self.assertTrue(self.category.subcategories.filter(slug="masonry-casting-labour").exists())

    def test_alias_normalization(self):
        alias = TaxonomyAlias.objects.create(
            alias_text="রাজমিস্ত্রি",
            category=self.category,
            target_type="SUBCATEGORY",
            target_id=102,
        )
        self.assertEqual(alias.normalized_text, "রাজমিস্ত্রি")


class TaxonomySeedServiceTests(TestCase):
    """Test idempotency and integrity of Master Taxonomy v1.0 Seeder."""

    def test_idempotent_seed(self):
        # 1st run
        res1 = TaxonomySeedService.seed_master_taxonomy()
        self.assertEqual(res1['categories_created'], 31)
        self.assertEqual(Category.objects.filter(is_active=True, level=0).count(), 31)

        # 2nd run (MUST NOT duplicate)
        res2 = TaxonomySeedService.seed_master_taxonomy()
        self.assertEqual(res2['categories_created'], 0)
        self.assertEqual(Category.objects.filter(is_active=True, level=0).count(), 31)


class TaxonomyAPITests(APITestCase):
    """Test REST API responses for Categories, Subcategories, Tree and Search."""

    def setUp(self):
        TaxonomySeedService.seed_master_taxonomy()

    def test_get_categories_list(self):
        url = reverse('categories:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 31)

    def test_get_category_tree(self):
        url = reverse('categories:category-tree')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 31)
        # Verify first item has subcategories list
        first_cat = response.data['data'][0]
        self.assertIn('subcategories', first_cat)
        self.assertGreater(len(first_cat['subcategories']), 0)

    def test_get_subcategories_for_category(self):
        cat = Category.objects.filter(slug='construction-engineering').first()
        url = reverse('categories:category-subcategories', kwargs={'pk': cat.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreater(len(response.data['data']), 0)

    def test_taxonomy_search(self):
        url = reverse('categories:taxonomy-search')
        response = self.client.get(url, {'q': 'নির্মাণ'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('categories', response.data['data'])
