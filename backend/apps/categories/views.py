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

from .models import Category, SubCategory, Service, TaxonomyAlias, TaxonomyVersion, TaxonomyChangeLog
from .constants import CategoryKind, ServiceType, TaxonomyStatus, TaxonomyActionType, AliasTargetType
from .serializers import (
    CategorySerializer,
    CategorySummarySerializer,
    CategoryTreeSerializer,
    SubCategorySerializer,
    SubCategorySummarySerializer,
    ServiceSerializer,
    ServiceSummarySerializer,
    TaxonomyAliasSerializer,
    TaxonomyVersionSerializer,
    TaxonomyChangeLogSerializer,
    TaxonomyImpactSerializer,
    TaxonomyRenameSerializer,
    TaxonomyDeactivateSerializer,
    TaxonomyReactivateSerializer,
    TaxonomyDeprecateSerializer,
    TaxonomyMergeCategorySerializer,
    TaxonomyMergeSubCategorySerializer,
    TaxonomyMoveSubCategorySerializer,
    TaxonomyVersionBumpSerializer,
)
from .services import CategoryTreeService, ServiceSearchService, TaxonomySearchService
from .governance import TaxonomyGovernanceService
from .migration_engine import TaxonomyMigrationEngine


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
        cat_id_param = request.query_params.get('category_id') or request.query_params.get('category')
        category_id = int(cat_id_param) if cat_id_param and cat_id_param.isdigit() else None
        limit_param = request.query_params.get('limit')
        limit = int(limit_param) if limit_param and limit_param.isdigit() else 25

        results = TaxonomySearchService.search(query=q, category_id=category_id, limit=limit)
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


# =============================================================================
# TAXONOMY GOVERNANCE & VERSIONING ENDPOINTS (Phase 4D)
# =============================================================================

class TaxonomyManifestView(views.APIView):
    """
    GET /api/v1/taxonomy/manifest/
    Publicly accessible endpoint returning current active taxonomy release version,
    metadata, checksum, and total counts for mobile cache synchronization.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        manifest = TaxonomyGovernanceService.get_current_taxonomy_manifest()
        return StandardResponse.success(
            data=manifest,
            message="ট্যাক্সোনমি ম্যানিফেস্ট এবং ভার্সন মেটাডাটা পাওয়া গেছে।"
        )


class TaxonomyVersionListView(views.APIView):
    """
    GET /api/v1/taxonomy/governance/versions/ - List all taxonomy releases.
    POST /api/v1/taxonomy/governance/versions/ - Bump / publish new version (Admin only).
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        versions = TaxonomyVersion.objects.all().order_by('-applied_at')
        serializer = TaxonomyVersionSerializer(versions, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ট্যাক্সোনমি ভার্সন ইতিহাস পাওয়া গেছে।"
        )

    def post(self, request):
        serializer = TaxonomyVersionBumpSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ভার্সন আপডেটে ত্রুটি রয়েছে।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        new_version = TaxonomyGovernanceService.bump_taxonomy_version(
            version_number=data['version_number'],
            release_title=data['release_title'],
            description=data.get('description', ''),
            changelog=data.get('changelog', []),
            user=request.user if request.user.is_authenticated else None
        )
        return StandardResponse.success(
            data=TaxonomyVersionSerializer(new_version).data,
            message=f"ট্যাক্সোনমি ভার্সন v{new_version.version_number} সফলভাবে প্রকাশিত হয়েছে।",
            status_code=status.HTTP_201_CREATED
        )


class TaxonomyChangeLogListView(views.APIView):
    """
    GET /api/v1/taxonomy/governance/audit-logs/
    View immutable taxonomy governance audit logs with filtering.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = TaxonomyChangeLog.objects.all().order_by('-created_at')

        target_type = request.query_params.get('target_type')
        if target_type:
            queryset = queryset.filter(target_type=target_type)

        target_id = request.query_params.get('target_id')
        if target_id and target_id.isdigit():
            queryset = queryset.filter(target_id=int(target_id))

        action = request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)

        limit_param = request.query_params.get('limit')
        limit = int(limit_param) if limit_param and limit_param.isdigit() else 50

        serializer = TaxonomyChangeLogSerializer(queryset[:limit], many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="ট্যাক্সোনমি অডিট লগ পাওয়া গেছে।"
        )


class TaxonomyImpactAnalysisView(views.APIView):
    """
    GET /api/v1/taxonomy/governance/impact/?target_type=CATEGORY|SUBCATEGORY&target_id=123
    Impact analysis preview prior to deactivation, deprecation, or merge.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        target_type = request.query_params.get('target_type')
        target_id_param = request.query_params.get('target_id')

        if not target_type or not target_id_param or not target_id_param.isdigit():
            return StandardResponse.error(
                message="target_type এবং target_id আবশ্যক।",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        target_id = int(target_id_param)
        try:
            if target_type.upper() == 'CATEGORY':
                impact = TaxonomyGovernanceService.get_category_impact(target_id)
            elif target_type.upper() == 'SUBCATEGORY':
                impact = TaxonomyGovernanceService.get_subcategory_impact(target_id)
            else:
                return StandardResponse.error(
                    message="অকার্যকর target_type (CATEGORY অথবা SUBCATEGORY দিন)।",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            return StandardResponse.success(
                data=impact,
                message="ইম্প্যাক্ট অ্যানালাইসিস সম্পন্ন হয়েছে।"
            )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyRenameView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/rename/
    Rename a Category or SubCategory with search alias preservation.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyRenameSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            if data['target_type'] == 'CATEGORY':
                cat = TaxonomyGovernanceService.rename_category(
                    category_id=data['target_id'],
                    name_bn=data['name_bn'],
                    name_en=data['name_en'],
                    reason=data.get('reason', ''),
                    user=request.user,
                    preserve_alias=data.get('preserve_alias', True)
                )
                return StandardResponse.success(
                    data=CategorySerializer(cat).data,
                    message="ক্যাটাগরি সফলভাবে পুনঃনামকরণ করা হয়েছে।"
                )
            else:
                sub = TaxonomyGovernanceService.rename_subcategory(
                    subcategory_id=data['target_id'],
                    name_bn=data['name_bn'],
                    name_en=data['name_en'],
                    reason=data.get('reason', ''),
                    user=request.user,
                    preserve_alias=data.get('preserve_alias', True)
                )
                return StandardResponse.success(
                    data=SubCategorySerializer(sub).data,
                    message="উপ-ক্যাটাগরি সফলভাবে পুনঃনামকরণ করা হয়েছে।"
                )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyDeactivateView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/deactivate/
    Deactivate a Category or SubCategory non-destructively.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyDeactivateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            if data['target_type'] == 'CATEGORY':
                cat = TaxonomyGovernanceService.deactivate_category(
                    category_id=data['target_id'],
                    reason=data.get('reason', ''),
                    user=request.user
                )
                return StandardResponse.success(
                    data=CategorySerializer(cat).data,
                    message="ক্যাটাগরি সফলভাবে নিষ্ক্রিয় করা হয়েছে।"
                )
            else:
                sub = TaxonomyGovernanceService.deactivate_subcategory(
                    subcategory_id=data['target_id'],
                    reason=data.get('reason', ''),
                    user=request.user
                )
                return StandardResponse.success(
                    data=SubCategorySerializer(sub).data,
                    message="উপ-ক্যাটাগরি সফলভাবে নিষ্ক্রিয় করা হয়েছে।"
                )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyReactivateView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/reactivate/
    Reactivate a Category or SubCategory.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyReactivateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            if data['target_type'] == 'CATEGORY':
                cat = TaxonomyGovernanceService.reactivate_category(
                    category_id=data['target_id'],
                    reason=data.get('reason', ''),
                    user=request.user
                )
                return StandardResponse.success(
                    data=CategorySerializer(cat).data,
                    message="ক্যাটাগরি সফলভাবে সক্রিয় করা হয়েছে।"
                )
            else:
                sub = TaxonomyGovernanceService.reactivate_subcategory(
                    subcategory_id=data['target_id'],
                    reason=data.get('reason', ''),
                    user=request.user
                )
                return StandardResponse.success(
                    data=SubCategorySerializer(sub).data,
                    message="উপ-ক্যাটাগরি সফলভাবে সক্রিয় করা হয়েছে।"
                )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyDeprecateView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/deprecate/
    Deprecate a Category or SubCategory with replacement pointer.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyDeprecateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            if data['target_type'] == 'CATEGORY':
                cat = TaxonomyGovernanceService.deprecate_category(
                    category_id=data['target_id'],
                    reason=data['reason'],
                    replacement_id=data.get('replacement_id'),
                    user=request.user
                )
                return StandardResponse.success(
                    data=CategorySerializer(cat).data,
                    message="ক্যাটাগরি সফলভাবে বাতিল/স্থগিত (Deprecated) ঘোষণা করা হয়েছে।"
                )
            else:
                sub = TaxonomyGovernanceService.deprecate_subcategory(
                    subcategory_id=data['target_id'],
                    reason=data['reason'],
                    replacement_id=data.get('replacement_id'),
                    user=request.user
                )
                return StandardResponse.success(
                    data=SubCategorySerializer(sub).data,
                    message="উপ-ক্যাটাগরি সফলভাবে বাতিল/স্থগিত (Deprecated) ঘোষণা করা হয়েছে।"
                )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyMergeCategoryView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/merge/category/
    Merge source Category into target Category with full dependency re-mapping.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyMergeCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            summary = TaxonomyGovernanceService.merge_category(
                source_category_id=data['source_category_id'],
                target_category_id=data['target_category_id'],
                reason=data['reason'],
                user=request.user
            )
            return StandardResponse.success(
                data=summary,
                message="ক্যাটাগরি সফলভাবে মার্জ করা হয়েছে এবং সকল সম্পর্ক পুনঃনির্ধারিত হয়েছে।"
            )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyMergeSubCategoryView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/merge/subcategory/
    Merge source SubCategory into target SubCategory.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyMergeSubCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            summary = TaxonomyGovernanceService.merge_subcategory(
                source_subcategory_id=data['source_subcategory_id'],
                target_subcategory_id=data['target_subcategory_id'],
                reason=data['reason'],
                user=request.user
            )
            return StandardResponse.success(
                data=summary,
                message="উপ-ক্যাটাগরি সফলভাবে মার্জ করা হয়েছে এবং সকল নির্ভরতা হালনাগাদ করা হয়েছে।"
            )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyMoveSubCategoryView(views.APIView):
    """
    POST /api/v1/taxonomy/governance/move/subcategory/
    Move a SubCategory to a new Master Category.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = TaxonomyMoveSubCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="ইনপুট ত্রুটি।",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            sub = TaxonomyGovernanceService.move_subcategory(
                subcategory_id=data['subcategory_id'],
                new_category_id=data['new_category_id'],
                reason=data.get('reason', ''),
                user=request.user
            )
            return StandardResponse.success(
                data=SubCategorySerializer(sub).data,
                message="উপ-ক্যাটাগরি সফলভাবে নতুন প্রধান ক্যাটাগরিতে স্থানান্তর করা হয়েছে।"
            )
        except Exception as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TaxonomyIntegrityCheckView(views.APIView):
    """
    GET /api/v1/categories/governance/integrity/
    Run system-wide taxonomy integrity checks.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        report = TaxonomyGovernanceService.verify_taxonomy_integrity()
        return StandardResponse.success(
            data=report,
            message="ট্যাক্সোনমি অখণ্ডতা পরীক্ষা সম্পন্ন হয়েছে।"
        )


class TaxonomyInventoryView(views.APIView):
    """
    GET /api/v1/categories/governance/inventory/
    Phase 4H: Returns comprehensive data counts and classifications across all 10 entities.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        inventory = TaxonomyMigrationEngine.get_existing_data_inventory()
        return StandardResponse.success(
            data=inventory,
            message="বিদ্যমান ডাটা ইনভেন্টরি ও কোয়ালিটি রিপোর্ট সফলভাবে প্রস্তুত হয়েছে।"
        )


class TaxonomyMigrationRulesView(views.APIView):
    """
    GET /api/v1/categories/governance/migration-map/
    Phase 4H: Returns the canonical migration mapping rules.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        rules = TaxonomyMigrationEngine.get_migration_rules()
        return StandardResponse.success(
            data=rules,
            message="মাস্টার ট্যাক্সোনমি মাইগ্রেশন ম্যাপিং রুলস লোড হয়েছে।"
        )


class TaxonomyOrphansView(views.APIView):
    """
    GET /api/v1/categories/governance/orphans/
    Phase 4H: Detects and returns orphaned relations and duplicates.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orphan_report = TaxonomyMigrationEngine.detect_orphans_and_duplicates()
        return StandardResponse.success(
            data=orphan_report,
            message="অরফ্যান ও ডুপ্লিকেট অ্যানালাইসিস রিপোর্ট প্রস্তুত।"
        )


class TaxonomyDryRunView(views.APIView):
    """
    POST /api/v1/categories/governance/dry-run/
    Phase 4H: Non-destructive dry-run migration simulation.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        result = TaxonomyMigrationEngine.dry_run()
        return StandardResponse.success(
            data=result,
            message="মাইগ্রেশন ড্রাই-রান সফলভাবে সম্পন্ন হয়েছে। কোনো ডাটাবেজ পরিবর্তন ঘটেনি।"
        )


class TaxonomyExecuteMigrationView(views.APIView):
    """
    POST /api/v1/categories/governance/migrate/
    Phase 4H: Executes live, transactional, and idempotent Master Taxonomy v1.0 migration.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        force = bool(request.data.get('force', False))
        result = TaxonomyMigrationEngine.execute_migration(user=request.user, force=force)
        return StandardResponse.success(
            data=result,
            message="মাস্টার ট্যাক্সোনমি v1.0 মাইগ্রেশন সফলভাবে এক্সিকিউট হয়েছে।"
        )


class TaxonomyRollbackManifestView(views.APIView):
    """
    GET /api/v1/categories/governance/rollback-manifest/
    Phase 4H: Returns audit trail manifest of taxonomy transformations.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        manifest = TaxonomyMigrationEngine.generate_rollback_manifest()
        return StandardResponse.success(
            data=manifest,
            message="মাইগ্রেশন রোলব্যাক অডিট ম্যানিফেস্ট প্রস্তুত।"
        )


