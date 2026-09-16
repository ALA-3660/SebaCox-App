"""
Unit and Integration Tests for SebaCox Master Taxonomy Search & Alias Engine (Phase 4C.9).
Deterministic, Database-driven Search, Normalization & Relevance Verification.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.categories.models import Category, SubCategory, Service, TaxonomyAlias
from apps.categories.constants import CategoryKind, SEBACOX_31_MASTER_CATEGORIES
from apps.categories.services import (
    TaxonomySeedService,
    TaxonomySearchService,
    normalize_search_text
)


class TaxonomyNormalizationTests(TestCase):
    """Test bilingual and Unicode normalization mechanics."""

    def test_unicode_nfc_and_case_folding(self):
        # English lowercase
        self.assertEqual(normalize_search_text("ELECTRICIAN"), "electrician")
        self.assertEqual(normalize_search_text("  MaSoN  "), "mason")
        # Bangla Unicode NFC
        self.assertEqual(normalize_search_text("  রাজমিস্ত্রি  "), "রাজমিস্ত্রি")

    def test_punctuation_stripping(self):
        self.assertEqual(normalize_search_text("CCTV!"), "cctv")
        self.assertEqual(normalize_search_text("ডাক্তার?"), "ডাক্তার")
        self.assertEqual(normalize_search_text("এসি (AC) সার্ভিসিং"), "এসি ac সার্ভিসিং")
        self.assertEqual(normalize_search_text("ইলেকট্রিশিয়ান।"), "ইলেকট্রিশিয়ান")

    def test_multi_whitespace_and_zero_width_removal(self):
        self.assertEqual(normalize_search_text("রাজ   মিস্ত্রি"), "রাজ মিস্ত্রি")
        self.assertEqual(normalize_search_text("চাঁন্দের \u200c গাড়ি"), "চাঁন্দের গাড়ি")


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
            alias_text="রাজ   মিস্ত্রি!",
            category=self.category,
            target_type="SUBCATEGORY",
            target_id=102,
        )
        self.assertEqual(alias.normalized_text, "রাজ মিস্ত্রি")


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


class TaxonomySearchEngineTests(TestCase):
    """Comprehensive verification of deterministic ranking, synonyms & boundaries."""

    def setUp(self):
        TaxonomySeedService.seed_master_taxonomy()

    def test_exact_name_match_ranks_highest(self):
        results = TaxonomySearchService.search("নির্মাণ ও প্রকৌশল")
        ranked = results['ranked_results']
        self.assertGreater(len(ranked), 0)
        first = ranked[0]
        self.assertEqual(first['name_bn'], "নির্মাণ ও প্রকৌশল")
        self.assertEqual(first['matched_by'], 'EXACT_NAME')
        self.assertGreaterEqual(first['relevance_score'], 100)

    def test_vernacular_alias_match_rajmistri(self):
        # "মেস্ত্রি" should resolve to SubCategory 102 (নির্মাণ শ্রমিক ও মিস্ত্রি)
        results = TaxonomySearchService.search("মেস্ত্রি")
        self.assertGreater(results['total_matches'], 0)
        first = results['ranked_results'][0]
        self.assertEqual(first['target_type'], 'SUBCATEGORY')
        self.assertEqual(first['name_bn'], 'নির্মাণ শ্রমিক ও মিস্ত্রি')
        self.assertEqual(first['category_name_bn'], 'নির্মাণ ও প্রকৌশল')

    def test_english_alias_match_electrician(self):
        # English lowercase/uppercase "electrician"
        results = TaxonomySearchService.search("ELECTRICIAN")
        self.assertGreater(results['total_matches'], 0)
        first = results['ranked_results'][0]
        self.assertEqual(first['target_type'], 'SUBCATEGORY')
        self.assertEqual(first['category_id'], 2)

    def test_cox_local_vernacular_chander_gari(self):
        # "চাঁন্দের গাড়ি" -> SubCategory 603 / Category 6
        results = TaxonomySearchService.search("চাঁন্দের গাড়ি")
        self.assertGreater(results['total_matches'], 0)
        matched_cat_ids = [r['category_id'] for r in results['ranked_results']]
        self.assertIn(6, matched_cat_ids)

    def test_cctv_alias_and_boundary(self):
        # "cctv" -> Security (Category 29)
        results = TaxonomySearchService.search("cctv")
        self.assertGreater(results['total_matches'], 0)
        first = results['ranked_results'][0]
        self.assertEqual(first['category_id'], 29)

    def test_dry_fish_shutki_vernacular(self):
        # "শুঁটকি" -> Category 10 (মৎস্য ও কৃষি)
        results = TaxonomySearchService.search("শুঁটকি")
        self.assertGreater(results['total_matches'], 0)
        first = results['ranked_results'][0]
        self.assertEqual(first['category_id'], 10)

    def test_nonexistent_query_returns_empty_safely(self):
        results = TaxonomySearchService.search("xyznonexistentterm999")
        self.assertEqual(results['total_matches'], 0)
        self.assertEqual(len(results['ranked_results']), 0)


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

    def test_taxonomy_search_api_with_ranking(self):
        url = reverse('categories:taxonomy-search')
        response = self.client.get(url, {'q': 'রাজমিস্ত্রি'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        data = response.data['data']
        self.assertIn('ranked_results', data)
        self.assertGreater(data['total_matches'], 0)
        first = data['ranked_results'][0]
        self.assertEqual(first['category_id'], 1)
