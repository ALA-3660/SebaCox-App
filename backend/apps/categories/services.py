"""
Category, SubCategory & Service Domain Services.
Master Taxonomy v1.0 Universal Hierarchy, Alias Matching & Bilingual Search.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import re
import unicodedata
from typing import List, Dict, Any, Optional
from django.db.models import Q, Count

from .models import Category, SubCategory, Service, TaxonomyAlias, TaxonomyVersion
from .constants import (
    CategoryKind,
    ServiceType,
    SEBACOX_31_MASTER_CATEGORIES,
    INITIAL_TAXONOMY_ALIASES,
    AliasTargetType,
    TaxonomyStatus,
)


def normalize_search_text(text: str) -> str:
    """
    Normalizes query text in Bangla (Unicode NFC) and English (lowercase).
    Strips punctuation, collapses multiple whitespaces, and unifies variations.
    """
    if not text:
        return ''
    # Unicode NFC Normalization
    normalized = unicodedata.normalize('NFC', text.strip())
    # Remove Zero-Width Non-Joiner / Joiner
    normalized = normalized.replace('\u200c', '').replace('\u200d', '')
    # Lowercase English characters
    normalized = normalized.lower()
    # Strip common punctuation: commas, colons, dashes, question marks, bangs, Bangla Dari (।)
    normalized = re.sub(r'[\?!,;:\(\)\[\]\{\}\\\/\-_\."\'“”‘’।]+', ' ', normalized)
    # Collapse multiple whitespaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


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
    Deterministic, Database-driven Search & Alias Engine for Master Taxonomy v1.0.
    Implements multi-tiered scoring:
    - Exact Name match: 100 pts
    - Exact Alias match: 95 pts
    - Prefix Name match: 85 pts
    - Prefix Alias match: 80 pts
    - Token/Word match: 75 pts
    - Contains Alias match: 70 pts
    - Contains Name match: 65 pts
    - Description/Keyword match: 50 pts
    Plus popularity and alias priority weight boosts.
    """

    @classmethod
    def search(
        cls,
        query: str,
        category_id: Optional[int] = None,
        target_types: Optional[List[str]] = None,
        limit: int = 25
    ) -> Dict[str, Any]:
        normalized = normalize_search_text(query)
        if not normalized or len(normalized) < 2:
            return {
                'query': query,
                'normalized': normalized,
                'total_matches': 0,
                'ranked_results': [],
                'categories': [],
                'subcategories': [],
                'services': [],
                'aliases': [],
            }

        query_tokens = [t for t in normalized.split(' ') if len(t) > 1]
        results_map: Dict[str, Dict[str, Any]] = {}

        # -------------------------------------------------------------
        # 1. SEARCH TAXONOMY ALIASES (Synonyms & Vernacular)
        # -------------------------------------------------------------
        alias_q = Q(is_active=True) & (
            Q(normalized_text__iexact=normalized) |
            Q(normalized_text__istartswith=normalized) |
            Q(normalized_text__icontains=normalized)
        )
        if category_id:
            alias_q &= (Q(category_id=category_id) | Q(subcategory__category_id=category_id))

        alias_candidates = list(
            TaxonomyAlias.objects.filter(alias_q)
            .select_related('category', 'subcategory')
            .order_by('-priority', 'alias_text')[:50]
        )

        for alias in alias_candidates:
            alias_norm = alias.normalized_text
            score = 60
            match_type = 'CONTAINS_ALIAS'

            if alias_norm == normalized:
                score = 95
                match_type = 'EXACT_ALIAS'
            elif alias_norm.startswith(normalized):
                score = 80
                match_type = 'PREFIX_ALIAS'
            elif any(t in alias_norm for t in query_tokens):
                score = 70
                match_type = 'TOKEN_ALIAS'

            # Add priority weight boost (0-5 pts)
            priority_boost = min(5, (alias.priority or 100) // 20)
            score += priority_boost

            if alias.target_type == AliasTargetType.SUBCATEGORY and alias.subcategory:
                sub = alias.subcategory
                if not sub.is_active:
                    continue
                key = f"sub_{sub.id}"
                if key not in results_map or results_map[key]['relevance_score'] < score:
                    pop_boost = 5 if sub.is_popular else 0
                    results_map[key] = {
                        'id': sub.id,
                        'target_type': 'SUBCATEGORY',
                        'name_bn': sub.name_bn,
                        'name_en': sub.name_en,
                        'slug': sub.slug,
                        'icon': sub.icon or 'layers',
                        'category_id': sub.category_id,
                        'category_name_bn': sub.category.name_bn if sub.category else '',
                        'category_name_en': sub.category.name_en if sub.category else '',
                        'subcategory_id': sub.id,
                        'subcategory_name_bn': sub.name_bn,
                        'subcategory_name_en': sub.name_en,
                        'relevance_score': score + pop_boost,
                        'matched_by': match_type,
                        'matched_alias': alias.alias_text,
                        'sort_order': sub.sort_order,
                    }

            elif alias.target_type == AliasTargetType.CATEGORY and alias.category:
                cat = alias.category
                if not cat.is_active:
                    continue
                key = f"cat_{cat.id}"
                if key not in results_map or results_map[key]['relevance_score'] < score:
                    pop_boost = 5 if cat.is_popular else (3 if cat.is_featured else 0)
                    results_map[key] = {
                        'id': cat.id,
                        'target_type': 'CATEGORY',
                        'name_bn': cat.name_bn,
                        'name_en': cat.name_en,
                        'slug': cat.slug,
                        'icon': cat.icon or 'grid',
                        'category_id': cat.id,
                        'category_name_bn': cat.name_bn,
                        'category_name_en': cat.name_en,
                        'subcategory_id': None,
                        'subcategory_name_bn': '',
                        'subcategory_name_en': '',
                        'relevance_score': score + pop_boost,
                        'matched_by': match_type,
                        'matched_alias': alias.alias_text,
                        'sort_order': cat.sort_order,
                    }

        # -------------------------------------------------------------
        # 2. SEARCH SUBCATEGORIES DIRECTLY
        # -------------------------------------------------------------
        sub_q = Q(is_active=True)
        if category_id:
            sub_q &= Q(category_id=category_id)

        sub_filter = (
            Q(name_bn__iexact=normalized) |
            Q(name_en__iexact=normalized) |
            Q(slug__iexact=normalized) |
            Q(name_bn__istartswith=normalized) |
            Q(name_en__istartswith=normalized) |
            Q(name_bn__icontains=normalized) |
            Q(name_en__icontains=normalized) |
            Q(short_description_bn__icontains=normalized)
        )
        for token in query_tokens:
            sub_filter |= Q(name_bn__icontains=token) | Q(name_en__icontains=token)

        sub_candidates = list(
            SubCategory.objects.filter(sub_q & sub_filter)
            .select_related('category')
            .order_by('sort_order', 'name_bn')[:40]
        )

        for sub in sub_candidates:
            key = f"sub_{sub.id}"
            norm_bn = normalize_search_text(sub.name_bn)
            norm_en = normalize_search_text(sub.name_en)
            score = 65
            match_type = 'CONTAINS_NAME'

            if norm_bn == normalized or norm_en == normalized or sub.slug == normalized:
                score = 100
                match_type = 'EXACT_NAME'
            elif norm_bn.startswith(normalized) or norm_en.startswith(normalized) or sub.slug.startswith(normalized):
                score = 85
                match_type = 'PREFIX_NAME'
            elif any(t in norm_bn or t in norm_en for t in query_tokens):
                score = 75
                match_type = 'TOKEN_NAME'

            pop_boost = 5 if sub.is_popular else 0
            total_score = score + pop_boost

            if key not in results_map or results_map[key]['relevance_score'] < total_score:
                results_map[key] = {
                    'id': sub.id,
                    'target_type': 'SUBCATEGORY',
                    'name_bn': sub.name_bn,
                    'name_en': sub.name_en,
                    'slug': sub.slug,
                    'icon': sub.icon or 'layers',
                    'category_id': sub.category_id,
                    'category_name_bn': sub.category.name_bn if sub.category else '',
                    'category_name_en': sub.category.name_en if sub.category else '',
                    'subcategory_id': sub.id,
                    'subcategory_name_bn': sub.name_bn,
                    'subcategory_name_en': sub.name_en,
                    'relevance_score': total_score,
                    'matched_by': match_type,
                    'matched_alias': '',
                    'sort_order': sub.sort_order,
                }

        # -------------------------------------------------------------
        # 3. SEARCH MASTER CATEGORIES DIRECTLY
        # -------------------------------------------------------------
        cat_filter = (
            Q(is_active=True) & (
                Q(name_bn__iexact=normalized) |
                Q(name_en__iexact=normalized) |
                Q(slug__iexact=normalized) |
                Q(name_bn__istartswith=normalized) |
                Q(name_en__istartswith=normalized) |
                Q(name_bn__icontains=normalized) |
                Q(name_en__icontains=normalized) |
                Q(description_bn__icontains=normalized)
            )
        )
        for token in query_tokens:
            cat_filter |= Q(name_bn__icontains=token) | Q(name_en__icontains=token)

        cat_candidates = list(
            Category.objects.filter(cat_filter)
            .order_by('sort_order', 'name_bn')[:31]
        )

        for cat in cat_candidates:
            key = f"cat_{cat.id}"
            norm_bn = normalize_search_text(cat.name_bn)
            norm_en = normalize_search_text(cat.name_en)
            score = 60
            match_type = 'CONTAINS_NAME'

            if norm_bn == normalized or norm_en == normalized or cat.slug == normalized:
                score = 100
                match_type = 'EXACT_NAME'
            elif norm_bn.startswith(normalized) or norm_en.startswith(normalized) or cat.slug.startswith(normalized):
                score = 85
                match_type = 'PREFIX_NAME'
            elif any(t in norm_bn or t in norm_en for t in query_tokens):
                score = 75
                match_type = 'TOKEN_NAME'

            pop_boost = 5 if cat.is_popular else (3 if cat.is_featured else 0)
            total_score = score + pop_boost

            if key not in results_map or results_map[key]['relevance_score'] < total_score:
                results_map[key] = {
                    'id': cat.id,
                    'target_type': 'CATEGORY',
                    'name_bn': cat.name_bn,
                    'name_en': cat.name_en,
                    'slug': cat.slug,
                    'icon': cat.icon or 'grid',
                    'category_id': cat.id,
                    'category_name_bn': cat.name_bn,
                    'category_name_en': cat.name_en,
                    'subcategory_id': None,
                    'subcategory_name_bn': '',
                    'subcategory_name_en': '',
                    'relevance_score': total_score,
                    'matched_by': match_type,
                    'matched_alias': '',
                    'sort_order': cat.sort_order,
                }

        # -------------------------------------------------------------
        # 4. RANK & SORT RESULTS
        # -------------------------------------------------------------
        ranked_list = list(results_map.values())
        # Sort deterministically by relevance_score DESC, then sort_order ASC, then name_bn ASC
        ranked_list.sort(key=lambda item: (-item['relevance_score'], item['sort_order'], item['name_bn']))
        trimmed_ranked = ranked_list[:limit]

        # Extract categorized subsets for backward-compatible response formats
        matched_category_ids = set()
        matched_categories = []
        matched_subcategories = []

        for item in trimmed_ranked:
            if item['target_type'] == 'CATEGORY':
                if item['id'] not in matched_category_ids:
                    matched_category_ids.add(item['id'])
                    matched_categories.append({
                        'id': item['id'],
                        'name_bn': item['name_bn'],
                        'name_en': item['name_en'],
                        'slug': item['slug'],
                        'icon': item['icon'],
                    })
            elif item['target_type'] == 'SUBCATEGORY':
                matched_subcategories.append({
                    'id': item['id'],
                    'category_id': item['category_id'],
                    'category_name_bn': item['category_name_bn'],
                    'category_name_en': item['category_name_en'],
                    'name_bn': item['name_bn'],
                    'name_en': item['name_en'],
                    'slug': item['slug'],
                    'icon': item['icon'],
                    'relevance_score': item['relevance_score'],
                    'matched_by': item['matched_by'],
                    'matched_alias': item['matched_alias'],
                })

        return {
            'query': query,
            'normalized': normalized,
            'total_matches': len(trimmed_ranked),
            'ranked_results': trimmed_ranked,
            'categories': matched_categories,
            'subcategories': matched_subcategories,
            'services': [],
            'aliases': [
                {
                    'alias_text': a.alias_text,
                    'target_type': a.target_type,
                    'target_id': a.target_id,
                    'category_name_bn': a.category.name_bn if a.category else '',
                }
                for a in alias_candidates[:limit]
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
        """Seeds the 31 Master Categories, Subcategories and rich Aliases."""
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
                    'status': TaxonomyStatus.ACTIVE,
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
                        'status': TaxonomyStatus.ACTIVE,
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
            is_active=False,
            status=TaxonomyStatus.INACTIVE
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
                    'alias_type': alias_data.get('alias_type', 'COMMON'),
                    'priority': alias_data.get('priority', 100),
                    'is_active': True,
                }
            )
            alias_count += 1

        # Ensure TaxonomyVersion v1.0 is initialized
        active_cats = Category.objects.filter(is_active=True, level=0).count()
        active_subs = SubCategory.objects.filter(is_active=True).count()
        active_aliases = TaxonomyAlias.objects.filter(is_active=True).count()

        TaxonomyVersion.objects.get_or_create(
            version_number='1.0',
            defaults={
                'release_title': 'SebaCox Master Taxonomy v1.0',
                'description': '31 Master Categories and granular sub-categories for Cox\'s Bazar marketplace.',
                'changelog': ['Initial Canonical Release', 'Provider & Demand Alignment'],
                'is_current': True,
                'total_categories_count': active_cats,
                'total_subcategories_count': active_subs,
                'total_aliases_count': active_aliases,
                'checksum': 'sebax-tax-v1.0-master-canonical'
            }
        )

        return {
            'categories_created': cat_created,
            'categories_updated': cat_updated,
            'subcategories_created': sub_created,
            'subcategories_updated': sub_updated,
            'aliases_seeded': alias_count,
        }

