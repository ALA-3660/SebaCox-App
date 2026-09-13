"""
Views and API Endpoints for SebaCox Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from common.responses import StandardResponse
from .models import Provider, ProviderService, ProviderServiceArea
from .constants import ProviderStatus, AvailabilityStatus
from .serializers import (
    ProviderListSerializer,
    ProviderDetailSerializer,
    ProviderCreateSerializer,
    ProviderUpdateSerializer,
    ProviderServiceSerializer,
    ProviderServiceAreaSerializer,
    ProviderAvailabilitySerializer,
)
from .permissions import IsProviderOwnerOrReadOnly, IsProviderOwner
from .services import ProviderDomainService


class ProviderListCreateView(APIView):
    """
    GET  /api/v1/providers/ - Public discoverable providers list with filters.
    POST /api/v1/providers/ - Register new provider profile (Authenticated users).
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request):
        query = request.query_params.get('q')
        service_id = request.query_params.get('service_id')
        category_id = request.query_params.get('category_id')
        upazila_id = request.query_params.get('upazila_id')
        district_id = request.query_params.get('district_id')
        provider_type = request.query_params.get('provider_type')
        status_param = request.query_params.get('status', ProviderStatus.ACTIVE)
        is_verified = request.query_params.get('is_verified')
        availability = request.query_params.get('availability')

        # Convert numeric & boolean params safely
        s_id = int(service_id) if service_id and service_id.isdigit() else None
        c_id = int(category_id) if category_id and category_id.isdigit() else None
        u_id = int(upazila_id) if upazila_id and upazila_id.isdigit() else None
        d_id = int(district_id) if district_id and district_id.isdigit() else None
        v_bool = True if is_verified == 'true' else (False if is_verified == 'false' else None)

        # Allow non-active status filtering only for staff/admin or user's own listings
        if status_param != ProviderStatus.ACTIVE and not (request.user and request.user.is_staff):
            status_param = ProviderStatus.ACTIVE

        qs = ProviderDomainService.filter_providers(
            query=query,
            service_id=s_id,
            category_id=c_id,
            upazila_id=u_id,
            district_id=d_id,
            provider_type=provider_type,
            status=status_param,
            is_verified=v_bool,
            availability=availability,
        )

        serializer = ProviderListSerializer(qs, many=True, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message="সেবাদাতাদের তালিকা সফলভাবে লোড হয়েছে"
        )

    def post(self, request):
        serializer = ProviderCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return StandardResponse.error(
                message="সেবাদাতা তথ্য সঠিক নয়",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        provider = serializer.save()
        detail_serializer = ProviderDetailSerializer(provider, context={'request': request})
        return StandardResponse.success(
            data=detail_serializer.data,
            message="সেবাদাতা প্রোফাইল সফলভাবে তৈরি হয়েছে (খসড়া হিসেবে সংরক্ষিত)",
            status_code=status.HTTP_201_CREATED
        )


class ProviderDetailView(APIView):
    """
    GET   /api/v1/providers/<id>/ - Public view of provider details.
    PATCH /api/v1/providers/<id>/ - Edit provider details (Owner/Admin only).
    """
    permission_classes = [IsProviderOwnerOrReadOnly]

    def get_object(self, pk):
        if str(pk).isdigit():
            obj = get_object_or_404(Provider.objects.prefetch_related('services', 'service_areas'), pk=int(pk))
        else:
            obj = get_object_or_404(Provider.objects.prefetch_related('services', 'service_areas'), slug=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        provider = self.get_object(pk)
        serializer = ProviderDetailSerializer(provider, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message="সেবাদাতা প্রোফাইল বিবরণ সফলভাবে লোড হয়েছে"
        )

    def patch(self, request, pk):
        provider = self.get_object(pk)
        serializer = ProviderUpdateSerializer(provider, data=request.data, partial=True)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="তথ্য হালনাগাদ করা সম্ভব হয়নি",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        detail = ProviderDetailSerializer(provider, context={'request': request})
        return StandardResponse.success(
            data=detail.data,
            message="সেবাদাতা প্রোফাইল সফলভাবে হালনাগাদ হয়েছে"
        )


class MyProviderProfileView(APIView):
    """
    GET   /api/v1/providers/me/ - Get current authenticated user's provider profile.
    PATCH /api/v1/providers/me/ - Quick update current authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        provider = Provider.objects.filter(user=request.user).first()
        if not provider:
            return StandardResponse.error(
                message="আপনার কোনো সেবাদাতা প্রোফাইল তৈরি করা নেই। 'আমি সেবা দিব' বিকল্পের মাধ্যমে নতুন প্রোফাইল তৈরি করুন।",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = ProviderDetailSerializer(provider, context={'request': request})
        return StandardResponse.success(
            data=serializer.data,
            message="আপনার সেবাদাতা প্রোফাইল সফলভাবে লোড হয়েছে"
        )

    def patch(self, request):
        provider = Provider.objects.filter(user=request.user).first()
        if not provider:
            return StandardResponse.error(
                message="কোনো সেবাদাতা প্রোফাইল খুঁজে পাওয়া যায়নি",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = ProviderUpdateSerializer(provider, data=request.data, partial=True)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="হালনাগাদে ত্রুটি",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        detail = ProviderDetailSerializer(provider, context={'request': request})
        return StandardResponse.success(
            data=detail.data,
            message="আপনার সেবাদাতা প্রোফাইল সফলভাবে হালনাগাদ হয়েছে"
        )


class ProviderServiceListCreateView(APIView):
    """
    GET  /api/v1/providers/<id>/services/ - List provider services.
    POST /api/v1/providers/<id>/services/ - Add service to provider (Owner/Admin).
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsProviderOwner()]
        return [permissions.AllowAny()]

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        services = provider.services.filter(is_active=True)
        serializer = ProviderServiceSerializer(services, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="সেবাদাতার সেবাসমূহ সফলভাবে লোড হয়েছে"
        )

    def post(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        service_id = request.data.get('service') or request.data.get('service_id')
        if not service_id:
            return StandardResponse.error(
                message="সেবা (service_id) আবশ্যক",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            ps = ProviderDomainService.add_service_to_provider(
                provider=provider,
                service_id=int(service_id),
                title_bn=request.data.get('title_bn', ''),
                title_en=request.data.get('title_en', ''),
                description_bn=request.data.get('description_bn', ''),
                description_en=request.data.get('description_en', ''),
                starting_price=request.data.get('starting_price'),
                price_type=request.data.get('price_type', 'STARTING_FROM'),
                actor=request.user
            )
            serializer = ProviderServiceSerializer(ps)
            return StandardResponse.success(
                data=serializer.data,
                message="সেবাটি সফলভাবে সেবাদাতার প্রোফাইলে যুক্ত হয়েছে",
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.messages[0] if hasattr(e, 'messages') else e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class ProviderServiceDetailView(APIView):
    """
    PATCH  /api/v1/providers/<id>/services/<service_id>/ - Update provider service.
    DELETE /api/v1/providers/<id>/services/<service_id>/ - Remove/deactivate service.
    """
    permission_classes = [IsProviderOwner]

    def patch(self, request, pk, service_id):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        ps = get_object_or_404(ProviderService, provider=provider, pk=service_id)
        serializer = ProviderServiceSerializer(ps, data=request.data, partial=True)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="সেবা হালনাগাদ ত্রুটি",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return StandardResponse.success(
            data=serializer.data,
            message="সেবাটি সফলভাবে হালনাগাদ হয়েছে"
        )

    def delete(self, request, pk, service_id):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        ps = get_object_or_404(ProviderService, provider=provider, pk=service_id)
        ps.delete()
        return StandardResponse.success(
            data={},
            message="সেবাটি সফলভাবে অপসারণ করা হয়েছে"
        )


class ProviderServiceAreaListCreateView(APIView):
    """
    GET  /api/v1/providers/<id>/service-areas/ - List service areas.
    POST /api/v1/providers/<id>/service-areas/ - Add service area (Owner/Admin).
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsProviderOwner()]
        return [permissions.AllowAny()]

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        areas = provider.service_areas.filter(is_active=True)
        serializer = ProviderServiceAreaSerializer(areas, many=True)
        return StandardResponse.success(
            data=serializer.data,
            message="সেবা এলাকাসমূহ সফলভাবে লোড হয়েছে"
        )

    def post(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        upazila_id = request.data.get('upazila') or request.data.get('upazila_id')
        district_id = request.data.get('district') or request.data.get('district_id')

        try:
            area = ProviderDomainService.add_service_area_to_provider(
                provider=provider,
                upazila_id=int(upazila_id) if upazila_id else None,
                district_id=int(district_id) if district_id else None,
                actor=request.user
            )
            serializer = ProviderServiceAreaSerializer(area)
            return StandardResponse.success(
                data=serializer.data,
                message="সেবা এলাকা সফলভাবে যুক্ত হয়েছে",
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.messages[0] if hasattr(e, 'messages') else e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class ProviderServiceAreaDetailView(APIView):
    """
    DELETE /api/v1/providers/<id>/service-areas/<area_id>/ - Remove service area.
    """
    permission_classes = [IsProviderOwner]

    def delete(self, request, pk, area_id):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        area = get_object_or_404(ProviderServiceArea, provider=provider, pk=area_id)
        area.delete()
        return StandardResponse.success(
            data={},
            message="সেবা এলাকা সফলভাবে অপসারণ করা হয়েছে"
        )


class ProviderAvailabilityView(APIView):
    """
    GET   /api/v1/providers/<id>/availability/ - Check availability status.
    PATCH /api/v1/providers/<id>/availability/ - Update availability (Owner/Admin).
    """
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsProviderOwner()]
        return [permissions.AllowAny()]

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        return StandardResponse.success(
            data={
                'id': provider.id,
                'availability_status': provider.availability_status,
                'availability_label': provider.get_availability_status_display(),
                'status': provider.status,
            },
            message="উপলব্ধতা তথ্য সফলভাবে লোড হয়েছে"
        )

    def patch(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        self.check_object_permissions(request, provider)

        serializer = ProviderAvailabilitySerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="অবৈধ অনুরোধ",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        new_status = serializer.validated_data['availability_status']
        note = serializer.validated_data.get('note', '')

        ProviderDomainService.update_availability(
            provider=provider,
            new_availability=new_status,
            actor=request.user,
            note=note
        )

        return StandardResponse.success(
            data={
                'id': provider.id,
                'availability_status': provider.availability_status,
                'availability_label': provider.get_availability_status_display(),
            },
            message="সেবাদাতার উপলব্ধতা সফলভাবে হালনাগাদ করা হয়েছে"
        )
