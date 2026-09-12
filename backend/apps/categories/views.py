"""
API Views for Categories & Services.
Universal Category & Service Foundation.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework import views, status, permissions
from common.responses import StandardResponse

from .models import Category, Service
from .constants import CategoryKind, ServiceType
from .serializers import (
    CategorySerializer,
    CategorySummarySerializer,
    CategoryTreeSerializer,
    ServiceSerializer,
    ServiceSummarySerializer
)
from .services import CategoryTreeService, ServiceSearchService


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
    GET /api/v1/categories/ - List active categories with optional filtering.
    POST /api/v1/categories/ - Create a new category (Admin only).
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Category.objects.filter(is_active=True)

        kind = request.query_params.get('kind')
        if kind:
            queryset = queryset.filter(kind=kind)
        else:
            # Default to public service categories for public browsing
            queryset = queryset.filter(kind=CategoryKind.PUBLIC_SERVICE_CATEGORY)

        parent_id = request.query_params.get('parent')
        if parent_id is not None:
            if parent_id in ('null', 'none', '', '0'):
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent_id)

        level = request.query_params.get('level')
        if level is not None:
            try:
                queryset = queryset.filter(level=int(level))
            except ValueError:
                pass

        is_featured = request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=(is_featured.lower() in ('true', '1')))

        queryset = queryset.annotate(
            active_children_count=Count('children', filter=Q(children__is_active=True)),
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
    GET /api/v1/categories/<id>/ - Retrieve single category.
    PUT/PATCH/DELETE - Admin modification.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        cat = get_object_or_404(
            Category.objects.annotate(
                active_children_count=Count('children', filter=Q(children__is_active=True)),
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


class CategoryChildrenView(views.APIView):
    """
    GET /api/v1/categories/<id>/children/ - Retrieve active direct children.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        children = category.children.filter(is_active=True).annotate(
            active_children_count=Count('children', filter=Q(children__is_active=True)),
            active_services_count=Count('services', filter=Q(services__is_active=True))
        ).order_by('sort_order', 'name_bn')

        serializer = CategorySerializer(children, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"{category.name_bn}-এর সাব-ক্যাটাগরি তালিকা পাওয়া গেছে।"
        )


class CategoryTreeViewView(views.APIView):
    """
    GET /api/v1/categories/tree/ - Retrieve structured category tree.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        kind = request.query_params.get('kind', CategoryKind.PUBLIC_SERVICE_CATEGORY)
        tree = CategoryTreeService.get_tree(kind=kind if kind != 'ALL' else None)
        return StandardResponse.success(
            data=tree,
            message="ক্যাটাগরি হায়ারার্কি ট্রি সফলভাবে তৈরি হয়েছে।"
        )


class CategoryFeaturedView(views.APIView):
    """
    GET /api/v1/categories/featured/ - Retrieve featured public categories.
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
        queryset = Service.objects.filter(is_active=True).select_related('category')

        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

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
    PUT/PATCH/DELETE - Admin modification.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        service = get_object_or_404(Service.objects.select_related('category'), pk=pk)
        serializer = ServiceSerializer(service)
        return StandardResponse.success(
            data=serializer.data,
            message="সেবার বিস্তারিত তথ্য পাওয়া গেছে।"
        )

    def patch(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return StandardResponse.success(
                data=ServiceSerializer(updated).data,
                message="সেবা সফলভাবে আপডেট হয়েছে।"
            )
        return StandardResponse.error(
            message="সেবা আপডেটে ত্রুটি।",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.is_active = False
        service.save(update_fields=['is_active'])
        return StandardResponse.success(
            data={'id': pk, 'is_active': False},
            message="সেবা নিষ্ক্রিয় করা হয়েছে।"
        )


class ServicesByCategoryView(views.APIView):
    """
    GET /api/v1/services/by-category/<category_id>/ - List services under category and subcategories.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        # Include services directly in category, or in child categories
        child_ids = list(category.children.filter(is_active=True).values_list('id', flat=True))
        all_cat_ids = [category.id] + child_ids

        services = Service.objects.filter(
            is_active=True,
            category_id__in=all_cat_ids
        ).select_related('category').order_by('sort_order', 'name_bn')

        serializer = ServiceSummarySerializer(services, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"{category.name_bn}-এর অধীন সেবাসমূহ পাওয়া গেছে।"
        )


class ServiceFeaturedView(views.APIView):
    """
    GET /api/v1/services/featured/ - List featured services.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        featured = Service.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category').order_by('sort_order', 'name_bn')

        serializer = ServiceSummarySerializer(featured, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="জনপ্রিয় সেবাসমূহ পাওয়া গেছে।"
        )


class ServiceSearchView(views.APIView):
    """
    GET /api/v1/services/search/?q=... - Bilingual search for services.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if not q:
            return StandardResponse.success(
                data=[],
                message="অনুসন্ধানের জন্য শব্দ লিখুন।"
            )

        category_id = request.query_params.get('category_id')
        service_type = request.query_params.get('service_type')
        is_featured_param = request.query_params.get('is_featured')
        is_featured = (is_featured_param.lower() in ('true', '1')) if is_featured_param else None

        results = ServiceSearchService.search(
            query=q,
            category_id=int(category_id) if category_id and category_id.isdigit() else None,
            service_type=service_type,
            is_featured=is_featured
        )

        serializer = ServiceSummarySerializer(results, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message=f"{len(results)}টি সেবা পাওয়া গেছে।"
        )
