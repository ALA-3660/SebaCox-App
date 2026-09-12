"""
Serializers for Category and Service Engine.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from rest_framework import serializers
from .models import Category, Service


class CategorySummarySerializer(serializers.ModelSerializer):
    """Lightweight parent/child category representation."""
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
            'sort_order',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Full Category Serializer with parent hierarchy and metadata."""
    parent_summary = CategorySummarySerializer(source='parent', read_only=True)
    active_children_count = serializers.IntegerField(read_only=True)
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
            'parent_summary',
            'level',
            'sort_order',
            'kind',
            'is_active',
            'is_featured',
            'active_children_count',
            'active_services_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['level', 'created_at', 'updated_at']


class RecursiveCategoryChildSerializer(serializers.Serializer):
    """Helper serializer for recursive child tree rendering."""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Recursive Tree Serializer for structured navigation."""
    children = serializers.SerializerMethodField()
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
            'services_count',
            'children',
        ]

    def get_children(self, obj):
        if hasattr(obj, 'prefetched_active_children'):
            children = obj.prefetched_active_children
        else:
            children = obj.children.filter(is_active=True).order_by('sort_order', 'name_bn')
        return CategoryTreeSerializer(children, many=True, context=self.context).data


class ServiceSummarySerializer(serializers.ModelSerializer):
    """Lightweight Service representation for lists and quick search."""
    category_name_bn = serializers.CharField(source='category.name_bn', read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'category',
            'category_name_bn',
            'category_name_en',
            'category_slug',
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
    capability_matrix = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = [
            'id',
            'name_bn',
            'name_en',
            'slug',
            'category',
            'category_detail',
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
