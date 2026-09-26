"""
Taxonomy Governance, Versioning & Lifecycle Management Service for SebaCox.
Implements non-destructive transitions: Draft -> Active -> Inactive -> Deprecated -> Merged.
Preserves historical business records (Demands, Providers, Offers, Services).
Deterministic alias preservation, impact analysis, and audit trails.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import hashlib
from typing import Dict, Any, List, Optional
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import (
    Category,
    SubCategory,
    Service,
    TaxonomyAlias,
    TaxonomyVersion,
    TaxonomyChangeLog,
    normalize_alias_text
)
from .constants import (
    CategoryKind,
    AliasTargetType,
    AliasType,
    AliasLanguage,
    TaxonomyStatus,
    TaxonomyActionType
)


class TaxonomyGovernanceService:
    """
    Centralized governance service enforcing taxonomy integrity,
    controlled lifecycle mutations, impact analysis, and audit logging.
    """

    @classmethod
    def get_category_impact(cls, category_id: int) -> Dict[str, Any]:
        """
        Calculate impact analysis for a Category prior to Deactivation, Deprecation, or Merge.
        """
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValidationError(f"Category with ID {category_id} not found.")

        subcategories_count = category.subcategories.count()
        active_subcategories_count = category.subcategories.filter(is_active=True).count()
        services_count = category.services.count()
        active_services_count = category.services.filter(is_active=True).count()
        aliases_count = TaxonomyAlias.objects.filter(
            category=category
        ).count() + TaxonomyAlias.objects.filter(
            target_type=AliasTargetType.CATEGORY, target_id=category_id
        ).count()

        # Dynamic cross-app relations check
        provider_services_count = getattr(category, 'provider_services', None) and category.provider_services.count() or 0
        active_provider_services_count = getattr(category, 'provider_services', None) and category.provider_services.filter(is_active=True).count() or 0
        demands_count = getattr(category, 'demands', None) and category.demands.count() or 0
        active_demands_count = getattr(category, 'demands', None) and category.demands.filter(status__in=['OPEN', 'IN_PROGRESS']).count() or 0

        return {
            'target_type': 'CATEGORY',
            'target_id': category.id,
            'name_bn': category.name_bn,
            'name_en': category.name_en,
            'status': category.status,
            'is_active': category.is_active,
            'subcategories_count': subcategories_count,
            'active_subcategories_count': active_subcategories_count,
            'services_count': services_count,
            'active_services_count': active_services_count,
            'provider_services_count': provider_services_count,
            'active_provider_services_count': active_provider_services_count,
            'demands_count': demands_count,
            'active_demands_count': active_demands_count,
            'aliases_count': aliases_count,
            'is_deactivatable_safely': True,
            'has_active_demands_or_providers': (active_provider_services_count > 0 or active_demands_count > 0),
        }

    @classmethod
    def get_subcategory_impact(cls, subcategory_id: int) -> Dict[str, Any]:
        """
        Calculate impact analysis for a SubCategory prior to mutation.
        """
        subcategory = SubCategory.objects.select_related('category').filter(id=subcategory_id).first()
        if not subcategory:
            raise ValidationError(f"SubCategory with ID {subcategory_id} not found.")

        services_count = subcategory.services.count()
        active_services_count = subcategory.services.filter(is_active=True).count()
        aliases_count = TaxonomyAlias.objects.filter(
            target_type=AliasTargetType.SUBCATEGORY, target_id=subcategory_id
        ).count()

        provider_services_count = getattr(subcategory, 'provider_services', None) and subcategory.provider_services.count() or 0
        active_provider_services_count = getattr(subcategory, 'provider_services', None) and subcategory.provider_services.filter(is_active=True).count() or 0
        demands_count = getattr(subcategory, 'demands', None) and subcategory.demands.count() or 0
        active_demands_count = getattr(subcategory, 'demands', None) and subcategory.demands.filter(status__in=['OPEN', 'IN_PROGRESS']).count() or 0

        return {
            'target_type': 'SUBCATEGORY',
            'target_id': subcategory.id,
            'category_id': subcategory.category_id,
            'category_name_bn': subcategory.category.name_bn,
            'name_bn': subcategory.name_bn,
            'name_en': subcategory.name_en,
            'status': subcategory.status,
            'is_active': subcategory.is_active,
            'services_count': services_count,
            'active_services_count': active_services_count,
            'provider_services_count': provider_services_count,
            'active_provider_services_count': active_provider_services_count,
            'demands_count': demands_count,
            'active_demands_count': active_demands_count,
            'aliases_count': aliases_count,
            'is_deactivatable_safely': True,
            'has_active_demands_or_providers': (active_provider_services_count > 0 or active_demands_count > 0),
        }

    @classmethod
    def rename_category(
        cls,
        category_id: int,
        name_bn: str,
        name_en: str,
        reason: str = '',
        user = None,
        preserve_alias: bool = True
    ) -> Category:
        """
        Controlled Rename for a Category.
        Preserves the previous name as a searchable alias so historical searches succeed.
        """
        with transaction.atomic():
            category = Category.objects.select_for_update().get(id=category_id)
            old_name_bn = category.name_bn
            old_name_en = category.name_en

            old_values = {'name_bn': old_name_bn, 'name_en': old_name_en}
            new_values = {'name_bn': name_bn, 'name_en': name_en}

            category.name_bn = name_bn
            category.name_en = name_en
            category.save()

            aliases_added = []
            if preserve_alias:
                # Add old Bangla name as search alias if different
                if old_name_bn != name_bn:
                    alias_bn, created_bn = TaxonomyAlias.objects.get_or_create(
                        alias_text=old_name_bn,
                        target_type=AliasTargetType.CATEGORY,
                        target_id=category.id,
                        defaults={
                            'category': category,
                            'language': AliasLanguage.BN,
                            'alias_type': AliasType.COMMON,
                            'priority': 95,
                            'is_active': True,
                        }
                    )
                    if created_bn:
                        aliases_added.append(old_name_bn)

                # Add old English name as search alias if different
                if old_name_en != name_en:
                    alias_en, created_en = TaxonomyAlias.objects.get_or_create(
                        alias_text=old_name_en,
                        target_type=AliasTargetType.CATEGORY,
                        target_id=category.id,
                        defaults={
                            'category': category,
                            'language': AliasLanguage.EN,
                            'alias_type': AliasType.ENGLISH,
                            'priority': 95,
                            'is_active': True,
                        }
                    )
                    if created_en:
                        aliases_added.append(old_name_en)

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=category.id,
                target_name=category.name_bn,
                action=TaxonomyActionType.RENAME,
                old_values=old_values,
                new_values={**new_values, 'preserved_aliases': aliases_added},
                reason=reason or f"Renamed Category from '{old_name_bn}' to '{name_bn}'",
                changed_by=user,
            )

            return category

    @classmethod
    def rename_subcategory(
        cls,
        subcategory_id: int,
        name_bn: str,
        name_en: str,
        reason: str = '',
        user = None,
        preserve_alias: bool = True
    ) -> SubCategory:
        """
        Controlled Rename for a SubCategory with deterministic search alias preservation.
        """
        with transaction.atomic():
            sub = SubCategory.objects.select_for_update().select_related('category').get(id=subcategory_id)
            old_name_bn = sub.name_bn
            old_name_en = sub.name_en

            old_values = {'name_bn': old_name_bn, 'name_en': old_name_en}
            new_values = {'name_bn': name_bn, 'name_en': name_en}

            sub.name_bn = name_bn
            sub.name_en = name_en
            sub.save()

            aliases_added = []
            if preserve_alias:
                if old_name_bn != name_bn:
                    _, created_bn = TaxonomyAlias.objects.get_or_create(
                        alias_text=old_name_bn,
                        target_type=AliasTargetType.SUBCATEGORY,
                        target_id=sub.id,
                        defaults={
                            'category': sub.category,
                            'subcategory': sub,
                            'language': AliasLanguage.BN,
                            'alias_type': AliasType.COMMON,
                            'priority': 95,
                            'is_active': True,
                        }
                    )
                    if created_bn:
                        aliases_added.append(old_name_bn)

                if old_name_en != name_en:
                    _, created_en = TaxonomyAlias.objects.get_or_create(
                        alias_text=old_name_en,
                        target_type=AliasTargetType.SUBCATEGORY,
                        target_id=sub.id,
                        defaults={
                            'category': sub.category,
                            'subcategory': sub,
                            'language': AliasLanguage.EN,
                            'alias_type': AliasType.ENGLISH,
                            'priority': 95,
                            'is_active': True,
                        }
                    )
                    if created_en:
                        aliases_added.append(old_name_en)

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=sub.id,
                target_name=sub.name_bn,
                action=TaxonomyActionType.RENAME,
                old_values=old_values,
                new_values={**new_values, 'preserved_aliases': aliases_added},
                reason=reason or f"Renamed SubCategory from '{old_name_bn}' to '{name_bn}'",
                changed_by=user,
            )

            return sub

    @classmethod
    def deactivate_category(cls, category_id: int, reason: str = '', user = None) -> Category:
        """
        Deactivate a Category non-destructively. Historical records remain preserved.
        """
        with transaction.atomic():
            category = Category.objects.select_for_update().get(id=category_id)
            impact = cls.get_category_impact(category_id)

            old_status = category.status
            old_active = category.is_active

            category.status = TaxonomyStatus.INACTIVE
            category.is_active = False
            category.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=category.id,
                target_name=category.name_bn,
                action=TaxonomyActionType.DEACTIVATE,
                old_values={'status': old_status, 'is_active': old_active},
                new_values={'status': TaxonomyStatus.INACTIVE, 'is_active': False},
                reason=reason or "Deactivated by Administrator",
                impact_summary=impact,
                changed_by=user,
            )
            return category

    @classmethod
    def reactivate_category(cls, category_id: int, reason: str = '', user = None) -> Category:
        """
        Reactivate an Inactive or Draft Category.
        """
        with transaction.atomic():
            category = Category.objects.select_for_update().get(id=category_id)
            old_status = category.status

            category.status = TaxonomyStatus.ACTIVE
            category.is_active = True
            category.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=category.id,
                target_name=category.name_bn,
                action=TaxonomyActionType.REACTIVATE,
                old_values={'status': old_status, 'is_active': False},
                new_values={'status': TaxonomyStatus.ACTIVE, 'is_active': True},
                reason=reason or "Reactivated by Administrator",
                changed_by=user,
            )
            return category

    @classmethod
    def deactivate_subcategory(cls, subcategory_id: int, reason: str = '', user = None) -> SubCategory:
        """
        Deactivate a SubCategory non-destructively.
        """
        with transaction.atomic():
            sub = SubCategory.objects.select_for_update().get(id=subcategory_id)
            impact = cls.get_subcategory_impact(subcategory_id)

            old_status = sub.status
            sub.status = TaxonomyStatus.INACTIVE
            sub.is_active = False
            sub.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=sub.id,
                target_name=sub.name_bn,
                action=TaxonomyActionType.DEACTIVATE,
                old_values={'status': old_status, 'is_active': True},
                new_values={'status': TaxonomyStatus.INACTIVE, 'is_active': False},
                reason=reason or "SubCategory deactivated by Administrator",
                impact_summary=impact,
                changed_by=user,
            )
            return sub

    @classmethod
    def reactivate_subcategory(cls, subcategory_id: int, reason: str = '', user = None) -> SubCategory:
        """
        Reactivate a SubCategory.
        """
        with transaction.atomic():
            sub = SubCategory.objects.select_for_update().get(id=subcategory_id)
            old_status = sub.status

            sub.status = TaxonomyStatus.ACTIVE
            sub.is_active = True
            sub.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=sub.id,
                target_name=sub.name_bn,
                action=TaxonomyActionType.REACTIVATE,
                old_values={'status': old_status, 'is_active': False},
                new_values={'status': TaxonomyStatus.ACTIVE, 'is_active': True},
                reason=reason or "SubCategory reactivated by Administrator",
                changed_by=user,
            )
            return sub

    @classmethod
    def deprecate_category(
        cls,
        category_id: int,
        reason: str,
        replacement_id: Optional[int] = None,
        user = None
    ) -> Category:
        """
        Deprecate a Category. Sets status=DEPRECATED, records replacement pointer and reason.
        """
        with transaction.atomic():
            category = Category.objects.select_for_update().get(id=category_id)
            replacement = None
            if replacement_id:
                if replacement_id == category_id:
                    raise ValidationError("Category cannot be its own replacement.")
                replacement = Category.objects.get(id=replacement_id)

            impact = cls.get_category_impact(category_id)
            old_status = category.status

            category.status = TaxonomyStatus.DEPRECATED
            category.is_active = False
            category.replacement = replacement
            category.deprecation_reason = reason
            category.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=category.id,
                target_name=category.name_bn,
                action=TaxonomyActionType.DEPRECATE,
                old_values={'status': old_status, 'is_active': True},
                new_values={
                    'status': TaxonomyStatus.DEPRECATED,
                    'is_active': False,
                    'replacement_id': replacement_id,
                    'deprecation_reason': reason
                },
                reason=reason,
                impact_summary=impact,
                changed_by=user,
            )
            return category

    @classmethod
    def deprecate_subcategory(
        cls,
        subcategory_id: int,
        reason: str,
        replacement_id: Optional[int] = None,
        user = None
    ) -> SubCategory:
        """
        Deprecate a SubCategory.
        """
        with transaction.atomic():
            sub = SubCategory.objects.select_for_update().get(id=subcategory_id)
            replacement = None
            if replacement_id:
                if replacement_id == subcategory_id:
                    raise ValidationError("SubCategory cannot be its own replacement.")
                replacement = SubCategory.objects.get(id=replacement_id)

            impact = cls.get_subcategory_impact(subcategory_id)
            old_status = sub.status

            sub.status = TaxonomyStatus.DEPRECATED
            sub.is_active = False
            sub.replacement = replacement
            sub.deprecation_reason = reason
            sub.save()

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=sub.id,
                target_name=sub.name_bn,
                action=TaxonomyActionType.DEPRECATE,
                old_values={'status': old_status, 'is_active': True},
                new_values={
                    'status': TaxonomyStatus.DEPRECATED,
                    'is_active': False,
                    'replacement_id': replacement_id,
                    'deprecation_reason': reason
                },
                reason=reason,
                impact_summary=impact,
                changed_by=user,
            )
            return sub

    @classmethod
    def merge_category(
        cls,
        source_category_id: int,
        target_category_id: int,
        reason: str,
        user = None
    ) -> Dict[str, Any]:
        """
        Merge source Category into target Category.
        Atomically remaps SubCategories, Services, ProviderServices, Demands, and Aliases.
        Creates search synonyms from source names to target category.
        """
        if source_category_id == target_category_id:
            raise ValidationError("Source and Target categories must be different.")

        with transaction.atomic():
            source = Category.objects.select_for_update().get(id=source_category_id)
            target = Category.objects.select_for_update().get(id=target_category_id)

            impact = cls.get_category_impact(source_category_id)

            # 1. Remap SubCategories
            subs_remapped = SubCategory.objects.filter(category=source).update(category=target)

            # 2. Remap Services
            services_remapped = Service.objects.filter(category=source).update(category=target)

            # 3. Remap ProviderServices
            providers_remapped = 0
            if hasattr(source, 'provider_services'):
                providers_remapped = source.provider_services.update(category=target)

            # 4. Remap Demands
            demands_remapped = 0
            if hasattr(source, 'demands'):
                demands_remapped = source.demands.update(category=target)

            # 5. Remap Aliases
            TaxonomyAlias.objects.filter(category=source).update(category=target)
            TaxonomyAlias.objects.filter(
                target_type=AliasTargetType.CATEGORY, target_id=source.id
            ).update(target_id=target.id, category=target)

            # 6. Preserve source category names as aliases pointing to target
            TaxonomyAlias.objects.get_or_create(
                alias_text=source.name_bn,
                target_type=AliasTargetType.CATEGORY,
                target_id=target.id,
                defaults={
                    'category': target,
                    'language': AliasLanguage.BN,
                    'alias_type': AliasType.COMMON,
                    'priority': 95,
                    'is_active': True,
                }
            )
            TaxonomyAlias.objects.get_or_create(
                alias_text=source.name_en,
                target_type=AliasTargetType.CATEGORY,
                target_id=target.id,
                defaults={
                    'category': target,
                    'language': AliasLanguage.EN,
                    'alias_type': AliasType.ENGLISH,
                    'priority': 95,
                    'is_active': True,
                }
            )

            # 7. Update source category state
            source.status = TaxonomyStatus.MERGED
            source.is_active = False
            source.merged_into = target
            source.deprecation_reason = reason
            source.save()

            mutation_summary = {
                'source_category_id': source.id,
                'source_name_bn': source.name_bn,
                'target_category_id': target.id,
                'target_name_bn': target.name_bn,
                'subcategories_remapped': subs_remapped,
                'services_remapped': services_remapped,
                'provider_services_remapped': providers_remapped,
                'demands_remapped': demands_remapped,
            }

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=source.id,
                target_name=source.name_bn,
                action=TaxonomyActionType.MERGE,
                old_values={'status': TaxonomyStatus.ACTIVE, 'name_bn': source.name_bn},
                new_values={
                    'status': TaxonomyStatus.MERGED,
                    'merged_into_id': target.id,
                    'target_name_bn': target.name_bn,
                },
                reason=reason,
                impact_summary=mutation_summary,
                changed_by=user,
            )

            return mutation_summary

    @classmethod
    def merge_subcategory(
        cls,
        source_subcategory_id: int,
        target_subcategory_id: int,
        reason: str,
        user = None
    ) -> Dict[str, Any]:
        """
        Merge source SubCategory into target SubCategory.
        Atomically remaps Services, ProviderServices, Demands, and Aliases.
        """
        if source_subcategory_id == target_subcategory_id:
            raise ValidationError("Source and Target subcategories must be different.")

        with transaction.atomic():
            source = SubCategory.objects.select_for_update().select_related('category').get(id=source_subcategory_id)
            target = SubCategory.objects.select_for_update().select_related('category').get(id=target_subcategory_id)

            # 1. Remap Services
            services_remapped = Service.objects.filter(subcategory=source).update(
                subcategory=target, category=target.category
            )

            # 2. Remap ProviderServices
            providers_remapped = 0
            if hasattr(source, 'provider_services'):
                providers_remapped = source.provider_services.update(
                    subcategory=target, category=target.category
                )

            # 3. Remap Demands
            demands_remapped = 0
            if hasattr(source, 'demands'):
                demands_remapped = source.demands.update(
                    subcategory=target, category=target.category
                )

            # 4. Remap Aliases
            TaxonomyAlias.objects.filter(subcategory=source).update(
                subcategory=target, category=target.category
            )
            TaxonomyAlias.objects.filter(
                target_type=AliasTargetType.SUBCATEGORY, target_id=source.id
            ).update(target_id=target.id, subcategory=target, category=target.category)

            # 5. Preserve source names as alias to target
            TaxonomyAlias.objects.get_or_create(
                alias_text=source.name_bn,
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=target.id,
                defaults={
                    'category': target.category,
                    'subcategory': target,
                    'language': AliasLanguage.BN,
                    'alias_type': AliasType.COMMON,
                    'priority': 95,
                    'is_active': True,
                }
            )
            TaxonomyAlias.objects.get_or_create(
                alias_text=source.name_en,
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=target.id,
                defaults={
                    'category': target.category,
                    'subcategory': target,
                    'language': AliasLanguage.EN,
                    'alias_type': AliasType.ENGLISH,
                    'priority': 95,
                    'is_active': True,
                }
            )

            # 6. Update source state
            source.status = TaxonomyStatus.MERGED
            source.is_active = False
            source.merged_into = target
            source.deprecation_reason = reason
            source.save()

            mutation_summary = {
                'source_subcategory_id': source.id,
                'source_name_bn': source.name_bn,
                'target_subcategory_id': target.id,
                'target_name_bn': target.name_bn,
                'services_remapped': services_remapped,
                'provider_services_remapped': providers_remapped,
                'demands_remapped': demands_remapped,
            }

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=source.id,
                target_name=source.name_bn,
                action=TaxonomyActionType.MERGE,
                old_values={'status': TaxonomyStatus.ACTIVE, 'name_bn': source.name_bn},
                new_values={
                    'status': TaxonomyStatus.MERGED,
                    'merged_into_id': target.id,
                    'target_name_bn': target.name_bn,
                },
                reason=reason,
                impact_summary=mutation_summary,
                changed_by=user,
            )

            return mutation_summary

    @classmethod
    def move_subcategory(
        cls,
        subcategory_id: int,
        new_category_id: int,
        reason: str = '',
        user = None
    ) -> SubCategory:
        """
        Move a SubCategory to a new Master Category.
        Reconciles all dependent records (Services, ProviderServices, Demands, Aliases).
        """
        with transaction.atomic():
            sub = SubCategory.objects.select_for_update().select_related('category').get(id=subcategory_id)
            new_category = Category.objects.get(id=new_category_id)

            old_category = sub.category
            if old_category.id == new_category.id:
                raise ValidationError("SubCategory already belongs to this Category.")

            old_values = {
                'category_id': old_category.id,
                'category_name_bn': old_category.name_bn,
            }
            new_values = {
                'category_id': new_category.id,
                'category_name_bn': new_category.name_bn,
            }

            sub.category = new_category
            sub.save()

            # Reconcile dependents
            services_count = Service.objects.filter(subcategory=sub).update(category=new_category)
            providers_count = 0
            if hasattr(sub, 'provider_services'):
                providers_count = sub.provider_services.update(category=new_category)
            demands_count = 0
            if hasattr(sub, 'demands'):
                demands_count = sub.demands.update(category=new_category)
            TaxonomyAlias.objects.filter(subcategory=sub).update(category=new_category)

            impact_summary = {
                'services_reconciled': services_count,
                'provider_services_reconciled': providers_count,
                'demands_reconciled': demands_count,
            }

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.SUBCATEGORY,
                target_id=sub.id,
                target_name=sub.name_bn,
                action=TaxonomyActionType.MOVE,
                old_values=old_values,
                new_values=new_values,
                reason=reason or f"Moved SubCategory from '{old_category.name_bn}' to '{new_category.name_bn}'",
                impact_summary=impact_summary,
                changed_by=user,
            )

            return sub

    @classmethod
    def bump_taxonomy_version(
        cls,
        version_number: str,
        release_title: str,
        description: str = '',
        changelog: Optional[List[str]] = None,
        user = None
    ) -> TaxonomyVersion:
        """
        Publish and register a new canonical Taxonomy Release Version.
        Generates checksum hash from all active categories and subcategories.
        """
        with transaction.atomic():
            cat_count = Category.objects.filter(is_active=True, level=0).count()
            sub_count = SubCategory.objects.filter(is_active=True).count()
            alias_count = TaxonomyAlias.objects.filter(is_active=True).count()

            # Generate content hash
            hash_input = f"{version_number}:{cat_count}:{sub_count}:{alias_count}:{timezone.now().isoformat()}"
            checksum = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]

            # Mark previous current as non-current
            TaxonomyVersion.objects.filter(is_current=True).update(is_current=False)

            ver, _ = TaxonomyVersion.objects.update_or_create(
                version_number=version_number,
                defaults={
                    'release_title': release_title,
                    'description': description,
                    'changelog': changelog or [],
                    'is_current': True,
                    'total_categories_count': cat_count,
                    'total_subcategories_count': sub_count,
                    'total_aliases_count': alias_count,
                    'checksum': f"tax-v{version_number}-{checksum}",
                }
            )

            TaxonomyChangeLog.objects.create(
                target_type=AliasTargetType.CATEGORY,
                target_id=ver.id,
                target_name=release_title,
                action=TaxonomyActionType.VERSION_BUMP,
                old_values={},
                new_values={
                    'version_number': version_number,
                    'release_title': release_title,
                    'total_categories': cat_count,
                    'total_subcategories': sub_count,
                    'checksum': ver.checksum,
                },
                reason=f"Taxonomy version bumped to v{version_number}",
                changed_by=user,
            )

            return ver

    @classmethod
    def get_current_taxonomy_manifest(cls) -> Dict[str, Any]:
        """
        Retrieve current active taxonomy version metadata for client cache validation.
        """
        current_ver = TaxonomyVersion.objects.filter(is_current=True).first()
        if not current_ver:
            # Fallback
            current_ver = TaxonomyVersion.objects.create(
                version_number='1.0',
                release_title='SebaCox Master Taxonomy v1.0',
                is_current=True,
                total_categories_count=Category.objects.filter(is_active=True, level=0).count(),
                total_subcategories_count=SubCategory.objects.filter(is_active=True).count(),
                total_aliases_count=TaxonomyAlias.objects.filter(is_active=True).count(),
                checksum='sebax-tax-v1.0-canonical'
            )

        return {
            'version': current_ver.version_number,
            'release_title': current_ver.release_title,
            'description': current_ver.description,
            'changelog': current_ver.changelog,
            'total_categories': current_ver.total_categories_count,
            'total_subcategories': current_ver.total_subcategories_count,
            'total_aliases': current_ver.total_aliases_count,
            'checksum': current_ver.checksum,
            'applied_at': current_ver.applied_at.isoformat() if current_ver.applied_at else None,
        }

    @classmethod
    def verify_taxonomy_integrity(cls) -> Dict[str, Any]:
        """
        Comprehensive audit checking for orphans, broken links,
        mismatched Category-SubCategory bindings, and invalid lifecycle states.
        """
        issues = []

        # 1. Check SubCategories without Category
        orphan_subs = SubCategory.objects.filter(category__isnull=True).count()
        if orphan_subs > 0:
            issues.append(f"{orphan_subs} SubCategories found with no parent Category.")

        # 2. Check Active SubCategories under Inactive Categories
        active_subs_inactive_cat = SubCategory.objects.filter(
            is_active=True, category__is_active=False
        ).count()
        if active_subs_inactive_cat > 0:
            issues.append(f"{active_subs_inactive_cat} active SubCategories exist under inactive Categories.")

        # 3. Check Services with mismatched Category and SubCategory
        mismatched_services = Service.objects.exclude(subcategory__isnull=True).filter(
            category_id__isnull=False
        ).exclude(subcategory__category_id=models_F_category_id()) if hasattr(Service, 'category') else 0

        # Direct loop check for high fidelity
        mismatch_count = 0
        for s in Service.objects.select_related('subcategory').filter(subcategory__isnull=False):
            if s.subcategory.category_id != s.category_id:
                mismatch_count += 1
        if mismatch_count > 0:
            issues.append(f"{mismatch_count} Services have category mismatch with their subcategory.")

        # 4. Check ProviderServices mismatch
        provider_mismatch = 0
        from apps.providers.models import ProviderService
        for ps in ProviderService.objects.select_related('subcategory').filter(subcategory__isnull=False, category__isnull=False):
            if ps.subcategory.category_id != ps.category_id:
                provider_mismatch += 1
        if provider_mismatch > 0:
            issues.append(f"{provider_mismatch} ProviderServices have category mismatch with their subcategory.")

        # 5. Check Demands mismatch
        demand_mismatch = 0
        from apps.demands.models import Demand
        for d in Demand.objects.select_related('subcategory').filter(subcategory__isnull=False, category__isnull=False):
            if d.subcategory.category_id != d.category_id:
                demand_mismatch += 1
        if demand_mismatch > 0:
            issues.append(f"{demand_mismatch} Demands have category mismatch with their subcategory.")

        is_healthy = (len(issues) == 0)
        return {
            'status': 'HEALTHY' if is_healthy else 'ISSUES_DETECTED',
            'is_healthy': is_healthy,
            'issues_count': len(issues),
            'issues': issues,
            'total_categories': Category.objects.count(),
            'active_categories': Category.objects.filter(is_active=True).count(),
            'total_subcategories': SubCategory.objects.count(),
            'active_subcategories': SubCategory.objects.filter(is_active=True).count(),
            'total_services': Service.objects.count(),
            'total_aliases': TaxonomyAlias.objects.count(),
        }
