"""
API Views for Categories, SubCategories, Services & Taxonomy Aliases.
Master Taxonomy v1.0 Universal Foundation.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework import views, status, permissions
from common.responses import StandardResponse

from .models import Category, SubCategory, Service, TaxonomyAlias
from .constants import CategoryKind, ServiceType
from .serializers import (
    CategorySerializer,
    CategorySummarySerializer,
    CategoryTreeSerializer,
    SubCategorySerializer,
    SubCategorySummarySerializer,
    ServiceSerializer,
    ServiceSummarySerializer,
    TaxonomyAliasSerializer,
)
from .services import CategoryTreeService, ServiceSearchService, TaxonomySearchService


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only requests for any user,
    write/modify requests strictly require authenticated staff/superuser.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class CategoryListView(views.APIView):
    """
    GET /api/v1/categories/ - List active master categories (31 Master Categories).
    POST /api/v1/categories/ - Create a new category (Admin only).
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Category.objects.filter(is_active=True)

        kind = request.query_params.get('kind')
        if kind:
            queryset = queryset.filter(kind=kind)
        else:
            queryset = queryset.filter(kind=CategoryKind.PUBLIC_SERVICE_CATEGORY)

        parent_id = request.query_params.get('parent')
        if parent_id is not None:
            if parent_id in ('null', 'none', '', '0'):
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent_id)

        is_featured = request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=(is_featured.lower() in ('true', '1')))

        is_popular = request.query_params.get('is_popular')
        if is_popular is not None:
            queryset = queryset.filter(is_popular=(is_popular.lower() in ('true', '1')))

        search = request.query_params.get('search') or request.query_params.get('q')
        if search:
            q_clean = search.strip()
            queryset = queryset.filter(
                Q(name_bn__icontains=q_clean) |
                Q(name_en__icontains=q_clean) |
                Q(slug__icontains=q_clean) |
                Q(description_bn__icontains=q_clean)
            )

        queryset = queryset.prefetch_related('subcategories').annotate(
            active_subcategories_count=Count('subcategories', filter=Q(subcategories__is_active=True)),
            active_services_count=Count('services', filter=Q(services__is_active=True))
        ).order_by('sort_order', 'name_bn')

        serializer = CategorySerializer(queryset, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ক্যাটাগরি তালিকা সফলভাবে পাওয়া গেছে।"
        )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            cat = serializer.save()
            return StandardResponse.success(
                data=CategorySerializer(cat).data,
                message="ক্যাটাগরি সফলভাবে তৈরি করা হয়েছে।",
                status_code=status.HTTP_201_CREATED
            )
        return StandardResponse.error(
            message="ক্যাটাগরি তৈরিতে ত্রুটি হয়েছে।",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class CategoryDetailView(views.APIView):
    """
    GET /api/v1/categories/<id>/ - Retrieve single category with subcategories.
    PATCH/DELETE - Admin modification.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        cat = get_object_or_404(
            Category.objects.prefetch_related('subcategories').annotate(
                active_subcategories_count=Count('subcategories', filter=Q(subcategories__is_active=True)),
                active_services_count=Count('services', filter=Q(services__is_active=True))
            ),
            pk=pk
        )
        serializer = CategorySerializer(cat)
        return StandardResponse.success(
            data=serializer.data,
            message="ক্যাটাগরি তথ্য পাওয়া গেছে।"
        )

    def patch(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return StandardResponse.success(
                data=CategorySerializer(updated).data,
                message="ক্যাটাগরি সফলভাবে আপডেট করা হয়েছে।"
            )
        return StandardResponse.error(
            message="ক্যাটাগরি আপডেটে ত্রুটি।",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        cat.is_active = False
        cat.save(update_fields=['is_active'])
        return StandardResponse.success(
            data={'id': pk, 'is_active': False},
            message="ক্যাটাগরি নিষ্ক্রিয় করা হয়েছে।"
        )


class CategorySubcategoriesView(views.APIView):
    """
    GET /api/v1/categories/<id>/subcategories/ - Direct cascading subcategories under a master category.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        subcategories = category.subcategories.filter(is_active=True).order_by('sort_order', 'name_bn')
        serializer = SubCategorySummarySerializer(subcategories, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"{category.name_bn}-এর সাব-ক্যাটাগরি তালিকা পাওয়া গেছে।"
        )


class SubCategoryListView(views.APIView):
    """
    GET /api/v1/subcategories/ - List subcategories with optional category filter.
    POST /api/v1/subcategories/ - Create subcategory (Admin only).
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = SubCategory.objects.filter(is_active=True).select_related('category')

        category_id = request.query_params.get('category_id') or request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        is_popular = request.query_params.get('is_popular')
        if is_popular is not None:
            queryset = queryset.filter(is_popular=(is_popular.lower() in ('true', '1')))

        search = request.query_params.get('search') or request.query_params.get('q')
        if search:
            q_clean = search.strip()
            queryset = queryset.filter(
                Q(name_bn__icontains=q_clean) |
                Q(name_en__icontains=q_clean) |
                Q(slug__icontains=q_clean) |
                Q(short_description_bn__icontains=q_clean)
            )

        queryset = queryset.order_by('category__sort_order', 'sort_order', 'name_bn')
        serializer = SubCategorySerializer(queryset, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="সাব-ক্যাটাগরি তালিকা পাওয়া গেছে।"
        )

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            sub = serializer.save()
            return StandardResponse.success(
                data=SubCategorySerializer(sub).data,
                message="সাব-ক্যাটাগরি সফলভাবে তৈরি করা হয়েছে।",
                status_code=status.HTTP_201_CREATED
            )
        return StandardResponse.error(
            message="সাব-ক্যাটাগরি তৈরিতে ত্রুটি হয়েছে।",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class SubCategoryDetailView(views.APIView):
    """
    GET /api/v1/subcategories/<id>/ - Single subcategory detail.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        sub = get_object_or_404(SubCategory.objects.select_related('category'), pk=pk)
        serializer = SubCategorySerializer(sub)
        return StandardResponse.success(
            data=serializer.data,
            message="সাব-ক্যাটাগরি তথ্য পাওয়া গেছে।"
        )


class CategoryChildrenView(views.APIView):
    """
    GET /api/v1/categories/<id>/children/ - Backward compatibility for child categories.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        # Returns subcategories or children
        subcategories = category.subcategories.filter(is_active=True).order_by('sort_order', 'name_bn')
        if subcategories.exists():
            serializer = SubCategorySummarySerializer(subcategories, many=True)
            return StandardResponse.success(
                data=serializer.data,
                message=f"{category.name_bn}-এর সাব-ক্যাটাগরি তালিকা পাওয়া গেছে।"
            )

        children = category.children.filter(is_active=True).order_by('sort_order', 'name_bn')
        serializer = CategorySummarySerializer(children, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"{category.name_bn}-এর সাব-ক্যাটাগরি তালিকা পাওয়া গেছে।"
        )


class CategoryTreeViewView(views.APIView):
    """
    GET /api/v1/categories/tree/ - Retrieve structured 31 Master Category tree with subcategories.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        kind = request.query_params.get('kind', CategoryKind.PUBLIC_SERVICE_CATEGORY)
        tree = CategoryTreeService.get_tree(kind=kind if kind != 'ALL' else None)
        return StandardResponse.success(
            data=tree,
            message="মাস্টার ট্যাক্সোনমি হায়ারার্কি ট্রি সফলভাবে পাওয়া গেছে।"
        )


class CategoryFeaturedView(views.APIView):
    """
    GET /api/v1/categories/featured/ - Retrieve featured master categories.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        featured = Category.objects.filter(
            is_active=True,
            is_featured=True,
            kind=CategoryKind.PUBLIC_SERVICE_CATEGORY
        ).order_by('sort_order', 'name_bn')

        serializer = CategorySummarySerializer(featured, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="নির্বাচিত ক্যাটাগরি তালিকা পাওয়া গেছে।"
        )


class ServiceListView(views.APIView):
    """
    GET /api/v1/services/ - List active services with filtering.
    POST /api/v1/services/ - Create new service (Admin only).
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Service.objects.filter(is_active=True).select_related('category', 'subcategory')

        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        subcategory_id = request.query_params.get('subcategory')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        service_type = request.query_params.get('service_type')
        if service_type:
            queryset = queryset.filter(service_type=service_type)

        is_featured = request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=(is_featured.lower() in ('true', '1')))

        queryset = queryset.order_by('sort_order', 'name_bn')
        serializer = ServiceSummarySerializer(queryset, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="সেবা তালিকা সফলভাবে পাওয়া গেছে।"
        )

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            return StandardResponse.success(
                data=ServiceSerializer(service).data,
                message="নতুন সেবা সফলভাবে তৈরি হয়েছে।",
                status_code=status.HTTP_201_CREATED
            )
        return StandardResponse.error(
            message="সেবা তৈরিতে ত্রুটি হয়েছে।",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ServiceDetailView(views.APIView):
    """
    GET /api/v1/services/<id>/ - Full service details with capability matrix.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        service = get_object_or_404(Service.objects.select_related('category', 'subcategory'), pk=pk)
        serializer = ServiceSerializer(service)
        return StandardResponse.success(
            data=serializer.data,
            message="সেবার বিস্তারিত তথ্য পাওয়া গেছে।"
        )


class TaxonomySearchView(views.APIView):
    """
    GET /api/v1/taxonomy/search/?q=... - Unified search for categories, subcategories, services and aliases.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        results = TaxonomySearchService.search(query=q)
        return StandardResponse.success(
            data=results,
            message="ট্যাক্সোনমি অনুসন্ধান ফলাফল পাওয়া গেছে।"
        )


class TaxonomyAliasListView(views.APIView):
    """
    GET /api/v1/taxonomy/aliases/ - List taxonomy synonyms/aliases.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        aliases = TaxonomyAlias.objects.filter(is_active=True).order_by('alias_text')
        serializer = TaxonomyAliasSerializer(aliases, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ট্যাক্সোনমি এলিয়াস তালিকা পাওয়া গেছে।"
        )
