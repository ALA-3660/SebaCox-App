"""
Category, SubCategory & Service Domain Services.
Master Taxonomy v1.0 Universal Hierarchy, Alias Matching & Bilingual Search.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import unicodedata
from typing import List, Dict, Any, Optional
from django.db.models import Q, Count

from .models import Category, SubCategory, Service, TaxonomyAlias
from .constants import CategoryKind, ServiceType, SEBACOX_31_MASTER_CATEGORIES, INITIAL_TAXONOMY_ALIASES


def normalize_search_text(text: str) -> str:
    """Normalizes query text in Bangla (Unicode NFC) and English (case-folded)."""
    if not text:
        return ''
    cleaned = unicodedata.normalize('NFC', text.strip())
    return cleaned.lower()


class CategoryTreeService:
    """
    Builds optimized hierarchical category trees for mobile and web clients.
    Includes both direct SubCategories and deep child relationships.
    """

    @classmethod
    def get_tree(
        cls,
        kind: Optional[str] = CategoryKind.PUBLIC_SERVICE_CATEGORY,
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Builds a nested tree of master categories and subcategories.
        """
        query = Q()
        if not include_inactive:
            query &= Q(is_active=True)
        if kind:
            query &= Q(kind=kind)

        master_categories = list(
            Category.objects.filter(query, level=0)
            .prefetch_related('subcategories')
            .annotate(
                services_count=Count('services', filter=Q(services__is_active=True)),
            )
            .order_by('sort_order', 'name_bn')
        )

        tree: List[Dict[str, Any]] = []
        for cat in master_categories:
            subs = [
                {
                    'id': sub.id,
                    'category_id': cat.id,
                    'name_bn': sub.name_bn,
                    'name_en': sub.name_en,
                    'slug': sub.slug,
                    'icon': sub.icon,
                    'short_description_bn': sub.short_description_bn,
                    'short_description_en': sub.short_description_en,
                    'sort_order': sub.sort_order,
                    'is_popular': sub.is_popular,
                    'is_active': sub.is_active,
                }
                for sub in cat.subcategories.filter(is_active=True).order_by('sort_order', 'name_bn')
            ]

            tree.append({
                'id': cat.id,
                'name_bn': cat.name_bn,
                'name_en': cat.name_en,
                'slug': cat.slug,
                'icon': cat.icon,
                'description_bn': cat.description_bn,
                'description_en': cat.description_en,
                'level': cat.level,
                'sort_order': cat.sort_order,
                'kind': cat.kind,
                'is_active': cat.is_active,
                'is_featured': cat.is_featured,
                'is_popular': cat.is_popular,
                'services_count': cat.services_count,
                'subcategories': subs,
            })

        return tree


class TaxonomySearchService:
    """
    Unified Bilingual Search Service for Categories, Subcategories, Services & Aliases.
    Resolves colloquial queries (e.g. 'রাজমিস্ত্রি', 'মেস্ত্রি', 'গাড়ি ভাড়া', 'doctor') to precise taxonomy nodes.
    """

    @classmethod
    def search(cls, query: str, limit: int = 20) -> Dict[str, Any]:
        normalized = normalize_search_text(query)
        if not normalized or len(normalized) < 2:
            return {
                'query': query,
                'normalized': normalized,
                'categories': [],
                'subcategories': [],
                'services': [],
                'aliases': [],
            }

        # 1. Search Aliases
        alias_matches = list(
            TaxonomyAlias.objects.filter(
                is_active=True,
                normalized_text__icontains=normalized
            ).select_related('category', 'subcategory')[:limit]
        )

        # 2. Search SubCategories
        subcategory_q = Q(is_active=True) & (
            Q(name_bn__icontains=normalized) |
            Q(name_en__icontains=normalized) |
            Q(slug__icontains=normalized)
        )
        subcategories = list(
            SubCategory.objects.filter(subcategory_q)
            .select_related('category')
            .order_by('sort_order', 'name_bn')[:limit]
        )

        # 3. Search Master Categories
        category_q = Q(is_active=True) & (
            Q(name_bn__icontains=normalized) |
            Q(name_en__icontains=normalized) |
            Q(slug__icontains=normalized) |
            Q(description_bn__icontains=normalized)
        )
        categories = list(
            Category.objects.filter(category_q)
            .order_by('sort_order', 'name_bn')[:limit]
        )

        # 4. Search Services
        service_q = Q(is_active=True) & (
            Q(name_bn__icontains=normalized) |
            Q(name_en__icontains=normalized) |
            Q(slug__icontains=normalized)
        )
        services = list(
            Service.objects.filter(service_q)
            .select_related('category', 'subcategory')
            .order_by('sort_order', 'name_bn')[:limit]
        )

        return {
            'query': query,
            'normalized': normalized,
            'categories': [
                {
                    'id': c.id,
                    'name_bn': c.name_bn,
                    'name_en': c.name_en,
                    'slug': c.slug,
                    'icon': c.icon,
                }
                for c in categories
            ],
            'subcategories': [
                {
                    'id': s.id,
                    'category_id': s.category_id,
                    'category_name_bn': s.category.name_bn,
                    'name_bn': s.name_bn,
                    'name_en': s.name_en,
                    'slug': s.slug,
                }
                for s in subcategories
            ],
            'services': [
                {
                    'id': sv.id,
                    'category_id': sv.category_id,
                    'category_name_bn': sv.category.name_bn,
                    'name_bn': sv.name_bn,
                    'name_en': sv.name_en,
                    'slug': sv.slug,
                }
                for sv in services
            ],
            'aliases': [
                {
                    'alias_text': a.alias_text,
                    'target_type': a.target_type,
                    'target_id': a.target_id,
                    'category_name_bn': a.category.name_bn if a.category else '',
                }
                for a in alias_matches
            ]
        }


class ServiceSearchService:
    """
    Bilingual search engine for Services supporting Bangla and English.
    """

    @classmethod
    def search(
        cls,
        query: str,
        category_id: Optional[int] = None,
        subcategory_id: Optional[int] = None,
        service_type: Optional[str] = None,
        is_featured: Optional[bool] = None,
        limit: int = 30
    ) -> List[Service]:
        normalized = normalize_search_text(query)
        if not normalized or len(normalized) < 2:
            return []

        q_filter = Q(is_active=True) & (
            Q(name_bn__icontains=normalized) |
            Q(name_en__icontains=normalized) |
            Q(slug__icontains=normalized) |
            Q(short_description_bn__icontains=normalized) |
            Q(short_description_en__icontains=normalized) |
            Q(category__name_bn__icontains=normalized) |
            Q(category__name_en__icontains=normalized)
        )

        if category_id:
            q_filter &= (Q(category_id=category_id) | Q(category__parent_id=category_id))

        if subcategory_id:
            q_filter &= Q(subcategory_id=subcategory_id)

        if service_type:
            q_filter &= Q(service_type=service_type)

        if is_featured is not None:
            q_filter &= Q(is_featured=is_featured)

        return list(
            Service.objects.filter(q_filter)
            .select_related('category', 'subcategory')
            .order_by('sort_order', 'name_bn')[:limit]
        )


class TaxonomySeedService:
    """
    Idempotent Seeder for Master Taxonomy Version 1.0 (31 Categories + SubCategories + Aliases).
    CRITICAL: Contains ONLY service taxonomy metadata, ZERO fake providers or businesses.
    """

    @classmethod
    def seed_master_taxonomy(cls) -> Dict[str, int]:
        """Seeds the 31 Master Categories and Subcategories."""
        cat_created = 0
        cat_updated = 0
        sub_created = 0
        sub_updated = 0

        valid_slugs = set()

        for cat_data in SEBACOX_31_MASTER_CATEGORIES:
            valid_slugs.add(cat_data['slug'])
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name_bn': cat_data['name_bn'],
                    'name_en': cat_data['name_en'],
                    'icon': cat_data.get('icon', ''),
                    'description_bn': cat_data.get('description_bn', ''),
                    'description_en': cat_data.get('description_en', ''),
                    'sort_order': cat_data['order'],
                    'kind': cat_data.get('kind', CategoryKind.PUBLIC_SERVICE_CATEGORY),
                    'is_active': True,
                    'is_featured': cat_data.get('is_featured', False),
                    'is_popular': cat_data.get('is_popular', False),
                    'level': 0,
                    'parent': None,
                }
            )
            if created:
                cat_created += 1
            else:
                cat_updated += 1

            for sub_data in cat_data.get('subcategories', []):
                _, s_created = SubCategory.objects.update_or_create(
                    slug=sub_data['slug'],
                    defaults={
                        'category': category,
                        'name_bn': sub_data['name_bn'],
                        'name_en': sub_data['name_en'],
                        'sort_order': sub_data.get('order', 0),
                        'is_active': True,
                        'is_popular': sub_data.get('is_popular', False),
                    }
                )
                if s_created:
                    sub_created += 1
                else:
                    sub_updated += 1

        # Non-destructively deactivate categories not in 31 Master list
        Category.objects.exclude(slug__in=valid_slugs).filter(level=0, kind=CategoryKind.PUBLIC_SERVICE_CATEGORY).update(
            is_active=False
        )

        # Seed Aliases
        alias_count = 0
        for alias_data in INITIAL_TAXONOMY_ALIASES:
            TaxonomyAlias.objects.update_or_create(
                alias_text=alias_data['alias_text'],
                defaults={
                    'normalized_text': alias_data['normalized_text'],
                    'target_type': alias_data['target_type'],
                    'target_id': alias_data['target_id'],
                    'language': alias_data['language'],
                    'is_active': True,
                }
            )
            alias_count += 1

        return {
            'categories_created': cat_created,
            'categories_updated': cat_updated,
            'subcategories_created': sub_created,
            'subcategories_updated': sub_updated,
            'aliases_seeded': alias_count,
        }
