"""
Serializers for Category, SubCategory, Service and TaxonomyAlias Engine.
Master Taxonomy v1.0 Governance & Versioning
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework import serializers
from .models import Category, SubCategory, Service, TaxonomyAlias, TaxonomyVersion, TaxonomyChangeLog
from .constants import TaxonomyStatus, AliasTargetType, TaxonomyActionType


class SubCategorySummarySerializer(serializers.ModelSerializer):
    """Lightweight SubCategory representation for cascading dropdowns and lists."""
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category_id',
            'category_name_bn',
            'name_bn',
            'name_en',
            'slug',
            'icon',
            'short_description_bn',
            'short_description_en',
            'sort_order',
            'is_popular',
            'is_active',
            'status',
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    """Full SubCategory Serializer with category metadata and lifecycle state."""
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    merged_into_name_bn = serializers.CharField(source='merged_into.name_bn', read_only=True)
    replacement_name_bn = serializers.CharField(source='replacement.name_bn', read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category',
            'category_name_bn',
            'category_name_en',
            'category_slug',
            'name_bn',
            'name_en',
            'slug',
            'icon',
            'short_description_bn',
            'short_description_en',
            'sort_order',
            'is_popular',
            'is_active',
            'status',
            'merged_into',
            'merged_into_name_bn',
            'replacement',
            'replacement_name_bn',
            'deprecation_reason',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class CategorySummarySerializer(serializers.ModelSerializer):
    """Lightweight master category representation."""
    class Meta:
        model = Category
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'icon',
            'level',
            'kind',
            'is_active',
            'status',
            'is_featured',
            'is_popular',
            'sort_order',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Full Category Serializer with subcategories list and metadata."""
    subcategories = SubCategorySummarySerializer(many=True, read_only=True)
    active_subcategories_count = serializers.IntegerField(read_only=True)
    active_services_count = serializers.IntegerField(read_only=True)
    merged_into_name_bn = serializers.CharField(source='merged_into.name_bn', read_only=True)
    replacement_name_bn = serializers.CharField(source='replacement.name_bn', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'icon',
            'description_bn',
            'description_en',
            'parent',
            'level',
            'sort_order',
            'kind',
            'is_active',
            'status',
            'merged_into',
            'merged_into_name_bn',
            'replacement',
            'replacement_name_bn',
            'deprecation_reason',
            'is_featured',
            'is_popular',
            'subcategories',
            'active_subcategories_count',
            'active_services_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['level', 'created_at', 'updated_at']


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Recursive / Cascading Tree Serializer for master and sub categories."""
    subcategories = SubCategorySummarySerializer(many=True, read_only=True)
    services_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'icon',
            'description_bn',
            'description_en',
            'level',
            'sort_order',
            'kind',
            'is_active',
            'status',
            'is_featured',
            'is_popular',
            'services_count',
            'subcategories',
        ]


class TaxonomyAliasSerializer(serializers.ModelSerializer):
    """Serializer for taxonomy alias and search synonyms."""
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    subcategory_name_bn = serializers.CharField(source='subcategory.name_bn', read_only=True)

    class Meta:
        model = TaxonomyAlias
        fields = [
            'id',
            'alias_text',
            'normalized_text',
            'target_type',
            'target_id',
            'language',
            'alias_type',
            'priority',
            'service_type',
            'category',
            'category_name_bn',
            'subcategory',
            'subcategory_name_bn',
            'is_active',
        ]


class ServiceSummarySerializer(serializers.ModelSerializer):
    """Lightweight Service representation for lists and quick search."""
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    subcategory_name_bn = serializers.CharField(source='subcategory.name_bn', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'category',
            'subcategory',
            'category_name_bn',
            'category_name_en',
            'category_slug',
            'subcategory_name_bn',
            'icon',
            'service_type',
            'requires_booking',
            'supports_demand',
            'supports_location',
            'supports_delivery',
            'supports_online',
            'is_active',
            'is_featured',
            'sort_order',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """Comprehensive Service Serializer with full capability matrix."""
    category_detail = CategorySummarySerializer(source='category', read_only=True)
    subcategory_detail = SubCategorySummarySerializer(source='subcategory', read_only=True)
    capability_matrix = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'category',
            'subcategory',
            'category_detail',
            'subcategory_detail',
            'secondary_categories',
            'short_description_bn',
            'short_description_en',
            'icon',
            'service_type',
            'requires_booking',
            'supports_demand',
            'supports_offer',
            'supports_negotiation',
            'supports_delivery',
            'supports_location',
            'supports_online',
            'supports_order',
            'supports_rental',
            'supports_payment',
            'capability_matrix',
            'is_active',
            'is_featured',
            'sort_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# =============================================================================
# TAXONOMY GOVERNANCE & VERSIONING SERIALIZERS (Phase 4D)
# =============================================================================

class TaxonomyVersionSerializer(serializers.ModelSerializer):
    """Serializer for Master Taxonomy Release Version."""
    class Meta:
        model = TaxonomyVersion
        fields = [
            'id',
            'version_number',
            'release_title',
            'description',
            'changelog',
            'is_current',
            'total_categories_count',
            'total_subcategories_count',
            'total_aliases_count',
            'checksum',
            'applied_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['checksum', 'applied_at', 'created_at', 'updated_at']


class TaxonomyChangeLogSerializer(serializers.ModelSerializer):
    """Serializer for Taxonomy Change History and Audit Trail."""
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = TaxonomyChangeLog
        fields = [
            'id',
            'target_type',
            'target_id',
            'target_name',
            'action',
            'action_display',
            'old_values',
            'new_values',
            'reason',
            'impact_summary',
            'changed_by',
            'changed_by_name',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class TaxonomyImpactSerializer(serializers.Serializer):
    """Impact analysis representation before executing governance actions."""
    target_type = serializers.CharField()
    target_id = serializers.IntegerField()
    name_bn = serializers.CharField()
    name_en = serializers.CharField()
    status = serializers.CharField()
    is_active = serializers.BooleanField()
    subcategories_count = serializers.IntegerField(required=False)
    active_subcategories_count = serializers.IntegerField(required=False)
    services_count = serializers.IntegerField()
    active_services_count = serializers.IntegerField()
    provider_services_count = serializers.IntegerField()
    active_provider_services_count = serializers.IntegerField()
    demands_count = serializers.IntegerField()
    active_demands_count = serializers.IntegerField()
    aliases_count = serializers.IntegerField()
    is_deactivatable_safely = serializers.BooleanField()
    has_active_demands_or_providers = serializers.BooleanField()


class TaxonomyRenameSerializer(serializers.Serializer):
    """Input serializer for renaming a Category or SubCategory."""
    target_type = serializers.ChoiceField(choices=['CATEGORY', 'SUBCATEGORY'])
    target_id = serializers.IntegerField()
    name_bn = serializers.CharField(max_length=150)
    name_en = serializers.CharField(max_length=150)
    reason = serializers.CharField(required=False, allow_blank=True, default='')
    preserve_alias = serializers.BooleanField(default=True)


class TaxonomyDeactivateSerializer(serializers.Serializer):
    """Input serializer for deactivating a Category or SubCategory."""
    target_type = serializers.ChoiceField(choices=['CATEGORY', 'SUBCATEGORY'])
    target_id = serializers.IntegerField()
    reason = serializers.CharField(required=False, allow_blank=True, default='')


class TaxonomyReactivateSerializer(serializers.Serializer):
    """Input serializer for reactivating a Category or SubCategory."""
    target_type = serializers.ChoiceField(choices=['CATEGORY', 'SUBCATEGORY'])
    target_id = serializers.IntegerField()
    reason = serializers.CharField(required=False, allow_blank=True, default='')


class TaxonomyDeprecateSerializer(serializers.Serializer):
    """Input serializer for deprecating a Category or SubCategory."""
    target_type = serializers.ChoiceField(choices=['CATEGORY', 'SUBCATEGORY'])
    target_id = serializers.IntegerField()
    reason = serializers.CharField(min_length=3)
    replacement_id = serializers.IntegerField(required=False, allow_null=True)


class TaxonomyMergeCategorySerializer(serializers.Serializer):
    """Input serializer for merging a Category."""
    source_category_id = serializers.IntegerField()
    target_category_id = serializers.IntegerField()
    reason = serializers.CharField(min_length=3)


class TaxonomyMergeSubCategorySerializer(serializers.Serializer):
    """Input serializer for merging a SubCategory."""
    source_subcategory_id = serializers.IntegerField()
    target_subcategory_id = serializers.IntegerField()
    reason = serializers.CharField(min_length=3)


class TaxonomyMoveSubCategorySerializer(serializers.Serializer):
    """Input serializer for moving a SubCategory to another Category."""
    subcategory_id = serializers.IntegerField()
    new_category_id = serializers.IntegerField()
    reason = serializers.CharField(required=False, allow_blank=True, default='')


class TaxonomyVersionBumpSerializer(serializers.Serializer):
    """Input serializer for publishing a new Taxonomy Version."""
    version_number = serializers.CharField(max_length=20)
    release_title = serializers.CharField(max_length=150)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    changelog = serializers.ListField(child=serializers.CharField(), required=False, default=list)


class TaxonomyMigrationExecuteInputSerializer(serializers.Serializer):
    """Input serializer for executing live Master Taxonomy migration."""
    force = serializers.BooleanField(default=False, required=False)
    confirm_phrase = serializers.CharField(required=False, allow_blank=True, default='')


