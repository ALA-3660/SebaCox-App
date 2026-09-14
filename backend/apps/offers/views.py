"""
Offer API Views for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError, PermissionDenied

from .models import Offer
from .serializers import (
    OfferSerializer,
    CreateInitialOfferSerializer,
    CreateCounterOfferSerializer,
    RejectOfferSerializer,
    CancelOfferSerializer,
    OfferAuditLogSerializer,
)
from .services import OfferService
from .selectors import (
    get_user_offers,
    get_demand_offers,
    get_offer_by_id,
    get_offer_chain_history,
    get_offer_audit_logs,
)
from .permissions import IsOfferPartyOrAdmin


class OfferListCreateView(APIView):
    """
    GET: List offers for current user (requester, provider, or proposer).
    POST: Create an INITIAL offer (provider only).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status')
        demand_id = request.query_params.get('demand_id')
        role = request.query_params.get('role')

        try:
            d_id = int(demand_id) if demand_id else None
        except ValueError:
            return Response({'error': 'অবৈধ ডিমান্ড আইডি'}, status=status.HTTP_400_BAD_REQUEST)

        offers = get_user_offers(request.user, status=status_filter, demand_id=d_id, role=role)
        serializer = OfferSerializer(offers, many=True)
        return Response({
            'success': True,
            'count': offers.count(),
            'results': serializer.data,
        })

    def post(self, request):
        serializer = CreateInitialOfferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            offer = OfferService.create_initial_offer(
                demand_id=data['demand_id'],
                provider_id=data['provider_id'],
                proposer_user=request.user,
                price=data['price'],
                title_bn=data['title_bn'],
                delivery_fee=data.get('delivery_fee', 0),
                service_fee=data.get('service_fee', 0),
                description_bn=data.get('description_bn', ''),
                quantity=data.get('quantity'),
                unit=data.get('unit', ''),
                terms_bn=data.get('terms_bn', ''),
                estimated_delivery_duration=data.get('estimated_delivery_duration', ''),
                expires_at=data.get('expires_at'),
                match_candidate_id=data.get('match_candidate_id'),
                currency=data.get('currency', 'BDT'),
            )
            out = OfferSerializer(offer)
            return Response({
                'success': True,
                'message': 'প্রস্তাব সফলভাবে প্রেরণ করা হয়েছে।',
                'offer': out.data,
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'success': False, 'error': e.message if hasattr(e, 'message') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferDetailView(APIView):
    """
    GET: Retrieve details of a specific offer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            offer = get_offer_by_id(pk, request.user)
            serializer = OfferSerializer(offer)
            return Response({
                'success': True,
                'offer': serializer.data,
            })
        except ValidationError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferAcceptView(APIView):
    """
    POST: Accept a PENDING offer.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            offer = OfferService.accept_offer(offer_id=pk, user=request.user)
            serializer = OfferSerializer(offer)
            return Response({
                'success': True,
                'message': 'প্রস্তাব সফলভাবে গ্রহণ করা হয়েছে।',
                'offer': serializer.data,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'success': False, 'error': e.message if hasattr(e, 'message') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferRejectView(APIView):
    """
    POST: Reject a PENDING offer.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = RejectOfferSerializer(data=request.data)
        serializer.is_valid() # optional reason
        reason = serializer.validated_data.get('rejection_reason_bn', '')

        try:
            offer = OfferService.reject_offer(offer_id=pk, user=request.user, rejection_reason_bn=reason)
            out = OfferSerializer(offer)
            return Response({
                'success': True,
                'message': 'প্রস্তাব প্রত্যাখ্যান করা হয়েছে।',
                'offer': out.data,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'success': False, 'error': e.message if hasattr(e, 'message') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferCancelView(APIView):
    """
    POST: Cancel a PENDING offer by the proposer.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CancelOfferSerializer(data=request.data)
        serializer.is_valid()
        reason = serializer.validated_data.get('cancellation_reason_bn', '')

        try:
            offer = OfferService.cancel_offer(offer_id=pk, user=request.user, cancellation_reason_bn=reason)
            out = OfferSerializer(offer)
            return Response({
                'success': True,
                'message': 'প্রস্তাব বাতিল করা হয়েছে।',
                'offer': out.data,
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'success': False, 'error': e.message if hasattr(e, 'message') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferCounterView(APIView):
    """
    POST: Create a COUNTER-OFFER against a PENDING parent offer.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CreateCounterOfferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            counter_offer = OfferService.create_counter_offer(
                parent_offer_id=pk,
                user=request.user,
                price=data['price'],
                title_bn=data.get('title_bn'),
                delivery_fee=data.get('delivery_fee', 0),
                service_fee=data.get('service_fee', 0),
                description_bn=data.get('description_bn'),
                quantity=data.get('quantity'),
                unit=data.get('unit'),
                terms_bn=data.get('terms_bn'),
                estimated_delivery_duration=data.get('estimated_delivery_duration'),
                expires_at=data.get('expires_at'),
            )
            out = OfferSerializer(counter_offer)
            return Response({
                'success': True,
                'message': 'পাল্টা প্রস্তাব সফলভাবে পাঠানো হয়েছে।',
                'counter_offer': out.data,
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'success': False, 'error': e.message if hasattr(e, 'message') else str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OfferHistoryView(APIView):
    """
    GET: Retrieve full version history / chain for an offer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            chain = get_offer_chain_history(pk, request.user)
            serializer = OfferSerializer(chain, many=True)
            audit_logs = get_offer_audit_logs(pk, request.user)
            audit_serializer = OfferAuditLogSerializer(audit_logs, many=True)
            return Response({
                'success': True,
                'offer_id': pk,
                'chain_length': chain.count(),
                'chain': serializer.data,
                'audit_trail': audit_serializer.data,
            })
        except ValidationError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class DemandOffersListView(APIView):
    """
    GET: Retrieve offers for a specific Demand.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, demand_id):
        try:
            offers = get_demand_offers(demand_id, request.user)
            serializer = OfferSerializer(offers, many=True)
            return Response({
                'success': True,
                'demand_id': demand_id,
                'count': offers.count(),
                'offers': serializer.data,
            })
        except ValidationError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
