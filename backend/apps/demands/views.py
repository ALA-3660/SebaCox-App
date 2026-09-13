"""
Views and API Endpoints for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Q
from django.utils import timezone

from common.responses import StandardResponse
from .models import Demand
from .constants import (
    DemandStatus,
    DemandVisibility,
    DemandPriority,
    DemandType,
    EDITABLE_DEMAND_STATUSES,
)
from .serializers import (
    DemandListSerializer,
    DemandDetailSerializer,
    DemandCreateSerializer,
    DemandUpdateSerializer,
)
from .permissions import IsDemandOwnerOrReadOnly, IsDemandOwner
from .services import DemandService


class DemandListCreateView(APIView):
    """
    GET  /api/v1/demands/ - List public/accessible demands with filtering.
    POST /api/v1/demands/ - Post a new demand (as DRAFT or immediate PUBLISHED).
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        # Auto-expire any published demands whose time has passed
        DemandService.check_and_expire_demands()

        user = request.user
        qs = Demand.objects.filter(is_deleted=False)

        # Visibility filters
        if not user or not user.is_authenticated:
            # Anonymous users only see PUBLIC and PUBLISHED demands
            qs = qs.filter(visibility=DemandVisibility.PUBLIC, status=DemandStatus.PUBLISHED)
        elif user.is_staff or user.is_superuser:
            # Staff can see all non-deleted
            pass
        else:
            # Authenticated users see (PUBLIC or REGISTERED_USERS with PUBLISHED) OR their own demands
            qs = qs.filter(
                (Q(visibility__in=[DemandVisibility.PUBLIC, DemandVisibility.REGISTERED_USERS]) & Q(status=DemandStatus.PUBLISHED))
                | Q(requester=user)
            )

        # Query Filters
        q = request.query_params.get('q')
        if q and q.strip():
            term = q.strip()
            qs = qs.filter(
                Q(title_bn__icontains=term) |
                Q(title_en__icontains=term) |
                Q(description_bn__icontains=term) |
                Q(location_display_bn__icontains=term)
            )

        category_id = request.query_params.get('category_id')
        if category_id and category_id.isdigit():
            qs = qs.filter(category_id=int(category_id))

        service_id = request.query_params.get('service_id')
        if service_id and service_id.isdigit():
            qs = qs.filter(service_id=int(service_id))

        upazila_id = request.query_params.get('upazila_id')
        if upazila_id and upazila_id.isdigit():
            qs = qs.filter(upazila_id=int(upazila_id))

        district_id = request.query_params.get('district_id')
        if district_id and district_id.isdigit():
            qs = qs.filter(district_id=int(district_id))

        demand_type = request.query_params.get('demand_type')
        if demand_type:
            qs = qs.filter(demand_type=demand_type)

        priority = request.query_params.get('priority')
        if priority:
            qs = qs.filter(priority=priority)

        status_param = request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        # Sorting
        sort_by = request.query_params.get('sort_by', 'newest')
        if sort_by == 'oldest':
            qs = qs.order_by('created_at')
        elif sort_by == 'expires_at':
            qs = qs.order_by('expires_at')
        elif sort_by == 'urgent':
            qs = qs.order_by('-priority', '-created_at')
        else:
            qs = qs.order_by('-created_at')

        serializer = DemandListSerializer(qs[:100], many=True, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message=f"{len(serializer.data)}টি প্রয়োজন পাওয়া গেছে"
        )

    def post(self, request):
        serializer = DemandCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রয়োজনের তথ্য সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        publish_now = serializer.validated_data.pop('publish_now', False)
        # Prepare data dict
        val_data = serializer.validated_data.copy()
        if 'service' in val_data and val_data['service']:
            val_data['service_id'] = val_data.pop('service').id
        if 'category' in val_data and val_data['category']:
            val_data['category_id'] = val_data.pop('category').id
        if 'district' in val_data and val_data['district']:
            val_data['district_id'] = val_data.pop('district').id
        if 'upazila' in val_data and val_data['upazila']:
            val_data['upazila_id'] = val_data.pop('upazila').id
        if 'union' in val_data and val_data['union']:
            val_data['union_id'] = val_data.pop('union').id
        if 'ward' in val_data and val_data['ward']:
            val_data['ward_id'] = val_data.pop('ward').id
        if 'geo_location' in val_data and val_data['geo_location']:
            val_data['geo_location_id'] = val_data.pop('geo_location').id

        try:
            demand = DemandService.create_demand(
                requester=request.user,
                data=val_data,
                publish_immediately=publish_now
            )
            detail_serializer = DemandDetailSerializer(demand, context={'request': request})
            msg = "প্রয়োজনটি সফলভাবে প্রকাশিত হয়েছে।" if demand.status == DemandStatus.PUBLISHED else "প্রয়োজনটি খসড়া হিসেবে সংরক্ষিত হয়েছে।"
            return StandardResponse.success(
                data=detail_serializer.data,
                message=msg,
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return StandardResponse.error(
                message="যাচাইকরণ ব্যর্থ হয়েছে",
                errors=e.message_dict if hasattr(e, 'message_dict') else {'detail': str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return StandardResponse.error(
                message=str(e),
                status_code=status.HTTP_403_FORBIDDEN
            )


class DemandDetailView(APIView):
    """
    GET    /api/v1/demands/<id>/ - Detailed view of single Demand.
    PATCH  /api/v1/demands/<id>/ - Update an existing Demand.
    DELETE /api/v1/demands/<id>/ - Soft-delete Demand.
    """
    permission_classes = [IsDemandOwnerOrReadOnly]

    def get_object(self, pk):
        demand = get_object_or_404(
            Demand.objects.select_related('requester', 'service', 'category', 'upazila', 'district'),
            id=pk,
            is_deleted=False
        )
        self.check_object_permissions(self.request, demand)
        # Check automatic expiration
        if demand.status == DemandStatus.PUBLISHED and demand.is_expired():
            DemandService.expire_demand(demand)
        return demand

    def get(self, request, pk):
        demand = self.get_object()
        serializer = DemandDetailSerializer(demand, context={'request': request})
        return StandardResponse.success(data=serializer.data)

    def patch(self, request, pk):
        demand = self.get_object()
        serializer = DemandUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্য সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        val_data = serializer.validated_data.copy()
        if 'service' in val_data:
            svc = val_data.pop('service')
            val_data['service_id'] = svc.id if svc else None
        if 'category' in val_data:
            cat = val_data.pop('category')
            val_data['category_id'] = cat.id if cat else None
        if 'district' in val_data:
            dist = val_data.pop('district')
            val_data['district_id'] = dist.id if dist else None
        if 'upazila' in val_data:
            upz = val_data.pop('upazila')
            val_data['upazila_id'] = upz.id if upz else None
        if 'union' in val_data:
            uni = val_data.pop('union')
            val_data['union_id'] = uni.id if uni else None
        if 'ward' in val_data:
            wrd = val_data.pop('ward')
            val_data['ward_id'] = wrd.id if wrd else None
        if 'geo_location' in val_data:
            geo = val_data.pop('geo_location')
            val_data['geo_location_id'] = geo.id if geo else None

        try:
            updated = DemandService.update_demand(demand, request.user, val_data)
            detail = DemandDetailSerializer(updated, context={'request': request})
            return StandardResponse.success(
                data=detail.data,
                message="প্রয়োজন সফলভাবে আপডেট করা হয়েছে।"
            )
        except ValidationError as e:
            return StandardResponse.error(
                message="আপডেট ব্যর্থ হয়েছে",
                errors=e.message_dict if hasattr(e, 'message_dict') else {'detail': str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        demand = self.get_object()
        try:
            DemandService.soft_delete_demand(demand, request.user)
            return StandardResponse.success(message="প্রয়োজনটি সফলভাবে মুছে ফেলা হয়েছে।")
        except PermissionDenied as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_403_FORBIDDEN)


class DemandPublishView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        try:
            published = DemandService.publish_demand(demand, request.user)
            return StandardResponse.success(
                data=DemandDetailSerializer(published, context={'request': request}).data,
                message="আপনার প্রয়োজন সফলভাবে প্রকাশিত হয়েছে।"
            )
        except ValidationError as e:
            return StandardResponse.error(
                message="প্রকাশ ব্যর্থ হয়েছে",
                errors=e.message_dict if hasattr(e, 'message_dict') else {'detail': str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_403_FORBIDDEN)


class DemandPauseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        reason = request.data.get('reason', '')
        try:
            paused = DemandService.pause_demand(demand, request.user, reason=reason)
            return StandardResponse.success(
                data=DemandDetailSerializer(paused, context={'request': request}).data,
                message="প্রয়োজন সাময়িক স্থগিত রাখা হয়েছে।"
            )
        except (ValidationError, PermissionDenied) as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class DemandResumeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        try:
            resumed = DemandService.resume_demand(demand, request.user)
            return StandardResponse.success(
                data=DemandDetailSerializer(resumed, context={'request': request}).data,
                message="প্রয়োজনটি পুনরায় প্রকাশ করা হয়েছে।"
            )
        except (ValidationError, PermissionDenied) as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class DemandCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        reason = request.data.get('reason', '')
        try:
            cancelled = DemandService.cancel_demand(demand, request.user, reason=reason)
            return StandardResponse.success(
                data=DemandDetailSerializer(cancelled, context={'request': request}).data,
                message="প্রয়োজনটি বাতিল করা হয়েছে।"
            )
        except (ValidationError, PermissionDenied) as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class DemandFulfillView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        note = request.data.get('note', '')
        try:
            fulfilled = DemandService.fulfill_demand(demand, request.user, note=note)
            return StandardResponse.success(
                data=DemandDetailSerializer(fulfilled, context={'request': request}).data,
                message="প্রয়োজন সফলভাবে পূরণ হিসেবে চিহ্নিত হয়েছে।"
            )
        except (ValidationError, PermissionDenied) as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class DemandCloseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemandOwner]

    def post(self, request, pk):
        demand = get_object_or_404(Demand, id=pk, is_deleted=False)
        self.check_object_permissions(request, demand)
        reason = request.data.get('reason', '')
        try:
            closed = DemandService.close_demand(demand, request.user, reason=reason)
            return StandardResponse.success(
                data=DemandDetailSerializer(closed, context={'request': request}).data,
                message="প্রয়োজন স্থায়ীভাবে বন্ধ করা হয়েছে।"
            )
        except (ValidationError, PermissionDenied) as e:
            return StandardResponse.error(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class MyDemandListView(APIView):
    """
    GET /api/v1/demands/me/ - All demands belonging to authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        DemandService.check_and_expire_demands(
            queryset=Demand.objects.filter(requester=request.user, status=DemandStatus.PUBLISHED, is_deleted=False)
        )
        demands = Demand.objects.filter(
            requester=request.user,
            is_deleted=False
        ).order_by('-created_at')

        serializer = DemandListSerializer(demands, many=True, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message=f"আপনার সর্বমোট {len(serializer.data)}টি প্রয়োজন রয়েছে"
        )


class MyActiveDemandListView(APIView):
    """
    GET /api/v1/demands/me/active/ - Active demands (PUBLISHED, PAUSED, DRAFT) of authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        DemandService.check_and_expire_demands(
            queryset=Demand.objects.filter(requester=request.user, status=DemandStatus.PUBLISHED, is_deleted=False)
        )
        demands = Demand.objects.filter(
            requester=request.user,
            status__in=[DemandStatus.PUBLISHED, DemandStatus.PAUSED, DemandStatus.DRAFT],
            is_deleted=False
        ).order_by('-created_at')

        serializer = DemandListSerializer(demands, many=True, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message=f"আপনার সক্রিয় {len(serializer.data)}টি প্রয়োজন রয়েছে"
        )


class MyHistoryDemandListView(APIView):
    """
    GET /api/v1/demands/me/history/ - Completed/historical demands (FULFILLED, CANCELLED, EXPIRED, CLOSED).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        demands = Demand.objects.filter(
            requester=request.user,
            status__in=[DemandStatus.FULFILLED, DemandStatus.CANCELLED, DemandStatus.EXPIRED, DemandStatus.CLOSED],
            is_deleted=False
        ).order_by('-created_at')

        serializer = DemandListSerializer(demands, many=True, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message=f"আপনার ইতিহাসের {len(serializer.data)}টি রেকর্ড রয়েছে"
        )
