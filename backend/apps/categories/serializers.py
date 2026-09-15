"""
Serializers for Category, SubCategory, Service and TaxonomyAlias Engine.
Master Taxonomy v1.0
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework import serializers
from .models import Category, SubCategory, Service, TaxonomyAlias


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
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    """Full SubCategory Serializer with category metadata."""
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)

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
            'is_featured',
            'is_popular',
            'sort_order',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Full Category Serializer with subcategories list and metadata."""
    subcategories = SubCategorySummarySerializer(many=True, read_only=True)
    active_subcategories_count = serializers.IntegerField(read_only=True)
    active_services_count = serializers.IntegerField(read_only=True)

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
            'is_featured',
            'is_popular',
            'services_count',
            'subcategories',
        ]


class TaxonomyAliasSerializer(serializers.ModelSerializer):
    """Serializer for taxonomy alias and search synonyms."""
    class Meta:
        model = TaxonomyAlias
        fields = [
            'id',
            'alias_text',
            'normalized_text',
            'target_type',
            'target_id',
            'language',
            'category',
            'subcategory',
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
