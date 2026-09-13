"""
Category & Service Domain Services.
Universal Category Tree Builder, Bilingual Search Engine, and Taxonomy Seeder.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import unicodedata
from typing import List, Dict, Any, Optional
from django.db.models import Q, Count

from .models import Category, Service
from .constants import CategoryKind, ServiceType, INITIAL_46_TAXONOMY_MODULES


def normalize_search_text(text: str) -> str:
    """Normalizes query text in Bangla (Unicode NFC) and English (case-folded)."""
    if not text:
        return ''
    cleaned = unicodedata.normalize('NFC', text.strip())
    return cleaned.lower()


class CategoryTreeService:
    """
    Builds optimized hierarchical category trees for mobile and web clients.
    Prevents deep N+1 queries by fetching active records in bulk.
    """

    @classmethod
    def get_tree(
        cls,
        kind: Optional[str] = CategoryKind.PUBLIC_SERVICE_CATEGORY,
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Builds a nested tree of categories up to arbitrary depth.
        """
        query = Q()
        if not include_inactive:
            query &= Q(is_active=True)
        if kind:
            query &= Q(kind=kind)

        all_categories = list(
            Category.objects.filter(query)
            .annotate(
                services_count=Count('services', filter=Q(services__is_active=True)),
                child_count=Count('children', filter=Q(children__is_active=True))
            )
            .order_by('level', 'sort_order', 'name_bn')
        )

        category_map: Dict[int, Dict[str, Any]] = {}
        for cat in all_categories:
            category_map[cat.id] = {
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
                'parent_id': cat.parent_id,
                'services_count': cat.services_count,
                'children': []
            }

        tree: List[Dict[str, Any]] = []
        for cat in all_categories:
            cat_dict = category_map[cat.id]
            if cat.parent_id and cat.parent_id in category_map:
                category_map[cat.parent_id]['children'].append(cat_dict)
            else:
                tree.append(cat_dict)

        return tree


class ServiceSearchService:
    """
    Bilingual search engine for Services supporting Bangla and English.
    """

    @classmethod
    def search(
        cls,
        query: str,
        category_id: Optional[int] = None,
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
            # Match directly or under category subtree
            q_filter &= (Q(category_id=category_id) | Q(category__parent_id=category_id))

        if service_type:
            q_filter &= Q(service_type=service_type)

        if is_featured is not None:
            q_filter &= Q(is_featured=is_featured)

        return list(
            Service.objects.filter(q_filter)
            .select_related('category')
            .order_by('sort_order', 'name_bn')[:limit]
        )


class TaxonomySeedService:
    """
    Idempotent Seeder for the 46 Master Taxonomy Categories and verified reference services.
    CRITICAL: Contains ONLY service taxonomy metadata, ZERO fake providers or businesses.
    """

    @classmethod
    def seed_initial_taxonomy(cls) -> Dict[str, int]:
        """Seeds the 46 Master Categories cleanly."""
        created_count = 0
        updated_count = 0

        for item in INITIAL_46_TAXONOMY_MODULES:
            cat, created = Category.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name_bn': item['name_bn'],
                    'name_en': item['name_en'],
                    'kind': item['kind'],
                    'icon': item['icon'],
                    'sort_order': item['order'],
                    'is_featured': item.get('featured', False),
                    'is_active': True,
                    'level': 0,
                    'parent': None,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        # Seed representative subcategories and services for core verified domains
        cls._seed_representative_services()

        return {'created': created_count, 'updated': updated_count}

    @classmethod
    def _seed_representative_services(cls):
        """
        Seeds representative hierarchy and service capabilities for verification.
        Pure taxonomy only.
        """
        # 1. স্বাস্থ্য ও চিকিৎসা (Health & Medical)
        health_cat = Category.objects.filter(slug='health-medical').first()
        if health_cat:
            doctor_sub, _ = Category.objects.get_or_create(
                slug='doctors-directory',
                defaults={
                    'name_bn': 'ডাক্তার',
                    'name_en': 'Doctors',
                    'parent': health_cat,
                    'level': 1,
                    'sort_order': 1,
                    'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
                    'icon': 'user-check',
                    'is_featured': True
                }
            )
            # Service: কার্ডিওলজি চিকিৎসা (Cardiology Care)
            Service.objects.update_or_create(
                slug='cardiology-care',
                defaults={
                    'category': doctor_sub,
                    'name_bn': 'কার্ডিওলজি চিকিৎসা',
                    'name_en': 'Cardiology Care',
                    'short_description_bn': 'অভিজ্ঞ হৃদরোগ বিশেষজ্ঞ দ্বারা চিকিৎসা পরামর্শ ও পরামর্শ সেবা।',
                    'short_description_en': 'Consultation and specialized treatment by cardiology specialists.',
                    'service_type': ServiceType.BOOKING,
                    'requires_booking': True,
                    'supports_demand': False,
                    'supports_location': True,
                    'supports_online': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )
            # Service: সাধারণ মেডিসিন (General Medicine)
            Service.objects.update_or_create(
                slug='general-medicine',
                defaults={
                    'category': doctor_sub,
                    'name_bn': 'জেনারেল মেডিসিন',
                    'name_en': 'General Medicine',
                    'short_description_bn': 'প্রাথমিক চিকিৎসা পরামর্শ ও স্বাস্থ্য সেবা।',
                    'short_description_en': 'Primary medical consultation and healthcare services.',
                    'service_type': ServiceType.BOOKING,
                    'requires_booking': True,
                    'supports_demand': False,
                    'supports_location': True,
                    'supports_online': True,
                    'is_featured': True,
                    'sort_order': 2
                }
            )

        # 2. নির্মাণ ও প্রকৌশল (Construction & Engineering)
        construct_cat = Category.objects.filter(slug='construction-engineering').first()
        if construct_cat:
            engineer_sub, _ = Category.objects.get_or_create(
                slug='engineers',
                defaults={
                    'name_bn': 'প্রকৌশলী',
                    'name_en': 'Engineers',
                    'parent': construct_cat,
                    'level': 1,
                    'sort_order': 1,
                    'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
                    'icon': 'compass'
                }
            )
            Service.objects.update_or_create(
                slug='civil-engineering-service',
                defaults={
                    'category': engineer_sub,
                    'name_bn': 'সিভিল ইঞ্জিনিয়ারিং সেবা',
                    'name_en': 'Civil Engineering Service',
                    'short_description_bn': 'ভবন ডিজাইন, প্ল্যান ও অবকাঠামো নির্মাণ পরিদর্শন সেবা।',
                    'short_description_en': 'Building design, structural planning, and site supervision.',
                    'service_type': ServiceType.SERVICE,
                    'requires_booking': True,
                    'supports_demand': True,
                    'supports_negotiation': True,
                    'supports_location': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )
            worker_sub, _ = Category.objects.get_or_create(
                slug='construction-workers',
                defaults={
                    'name_bn': 'নির্মাণ শ্রমিক ও কারিগর',
                    'name_en': 'Construction Workers & Artisans',
                    'parent': construct_cat,
                    'level': 1,
                    'sort_order': 2,
                    'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
                    'icon': 'users'
                }
            )
            Service.objects.update_or_create(
                slug='mason-service',
                defaults={
                    'category': worker_sub,
                    'name_bn': 'রাজমিস্ত্রি সেবা',
                    'name_en': 'Mason Service',
                    'short_description_bn': 'দক্ষ রাজমিস্ত্রি দ্বারা গাঁথুনি ও প্লাস্টার কাজ।',
                    'short_description_en': 'Masonry and plastering work by experienced masons.',
                    'service_type': ServiceType.SERVICE,
                    'requires_booking': True,
                    'supports_demand': True,
                    'supports_negotiation': True,
                    'supports_location': True,
                    'sort_order': 1
                }
            )

        # 3. নির্মাণ সামগ্রী (Building Materials)
        materials_cat = Category.objects.filter(slug='building-materials').first()
        if materials_cat:
            Service.objects.update_or_create(
                slug='building-bricks',
                defaults={
                    'category': materials_cat,
                    'name_bn': 'ইট ও বালু সরবরাহ',
                    'name_en': 'Brick & Sand Supply',
                    'short_description_bn': 'প্রথম শ্রেণির ইট ও উন্নত মানের বালু সাইটে সরবরাহ।',
                    'short_description_en': 'First class bricks and high quality sand supply to construction sites.',
                    'service_type': ServiceType.PRODUCT,
                    'supports_order': True,
                    'supports_delivery': True,
                    'supports_offer': True,
                    'supports_location': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )

        # 4. ভ্রমণ ও পর্যটন (Travel & Tourism)
        tourism_cat = Category.objects.filter(slug='travel-tourism').first()
        hotel_cat = Category.objects.filter(slug='hotel-accommodation').first()
        if hotel_cat:
            Service.objects.update_or_create(
                slug='hotel-room-booking',
                defaults={
                    'category': hotel_cat,
                    'name_bn': 'হোটেল রুম বুকিং',
                    'name_en': 'Hotel Room Booking',
                    'short_description_bn': 'কক্সবাজার সমুদ্র সৈকত সংলগ্ন হোটেল ও রিসোর্ট বুকিং সেবা।',
                    'short_description_en': 'Beachside hotel and resort room reservations in Cox\'s Bazar.',
                    'service_type': ServiceType.BOOKING,
                    'requires_booking': True,
                    'supports_location': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )

        # 5. খাবার ও রেস্তোরাঁ (Food & Restaurants)
        food_cat = Category.objects.filter(slug='food-restaurants').first()
        if food_cat:
            Service.objects.update_or_create(
                slug='restaurant-dine-in',
                defaults={
                    'category': food_cat,
                    'name_bn': 'রেস্তোরাঁ ও টেবিল বুকিং',
                    'name_en': 'Restaurant & Table Booking',
                    'short_description_bn': 'ঐতিহ্যবাহী সামুদ্রিক মাছ ও বাংলা খাবারের টেবিল সংরক্ষণ।',
                    'short_description_en': 'Table reservations and authentic seafood dining experiences.',
                    'service_type': ServiceType.BOOKING,
                    'requires_booking': True,
                    'supports_location': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )

        # 6. বাড়ি ও ব্যক্তিগত সেবা (Home & Personal Services)
        home_cat = Category.objects.filter(slug='home-personal-services').first()
        if home_cat:
            Service.objects.update_or_create(
                slug='electrician-service',
                defaults={
                    'category': home_cat,
                    'name_bn': 'ইলেকট্রিশিয়ান সেবা',
                    'name_en': 'Electrician Service',
                    'short_description_bn': 'বাসাবাড়ি ও অফিসের জরুরি বৈদ্যুতিক ওয়্যারিং ও মেরামত।',
                    'short_description_en': 'Emergency home and office electrical wiring and maintenance.',
                    'service_type': ServiceType.SERVICE,
                    'requires_booking': True,
                    'supports_demand': True,
                    'supports_location': True,
                    'supports_negotiation': True,
                    'is_featured': True,
                    'sort_order': 1
                }
            )
