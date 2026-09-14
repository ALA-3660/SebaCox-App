"""
API Views for SebaCox Matching Engine.
Phase 7: Endpoints for Demand Matches, Match Details, and Re-matching.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError

from apps.demands.models import Demand
from .models import MatchCandidate, MatchingRun
from .constants import MatchStatus, SEBACOX_MAIN_SLOGAN_BN
from .selectors import get_matches_for_demand, get_match_detail
from .services import MatchingEngine
from .serializers import MatchCandidateSerializer, MatchingRunSerializer
from .permissions import CanViewDemandMatchesPermission, CanTriggerRematchPermission


class DemandMatchesListView(views.APIView):
    """
    GET /api/v1/demands/<demand_id>/matches/
    Lists ranked eligible match candidates for a specific Demand.
    Protected by object-level ownership and IDOR prevention.
    """
    permission_classes = [permissions.IsAuthenticated, CanViewDemandMatchesPermission]

    def get(self, request, demand_id: int):
        demand = get_object_or_404(Demand, id=demand_id, is_deleted=False)
        self.check_object_permissions(request, demand)

        match_status = request.query_params.get('status', MatchStatus.ELIGIBLE)
        version = request.query_params.get('version', 'v1')

        queryset = get_matches_for_demand(
            demand_id=demand.id,
            status=match_status if match_status != 'ALL' else None,
            version=version
        )

        # If user is a provider (and not the demand requester or staff), restrict to their own match
        if not (request.user.is_staff or request.user.is_superuser or demand.requester_id == request.user.id):
            queryset = queryset.filter(provider__user=request.user)

        serializer = MatchCandidateSerializer(queryset, many=True, context={'request': request})
        candidates = serializer.data
        count = len(candidates)

        if count > 0:
            msg_bn = f"{count} জন উপযুক্ত সম্ভাব্য সেবাদাতা পাওয়া গেছে।"
        else:
            msg_bn = "এখনও কোনো উপযুক্ত সেবাদাতা পাওয়া যায়নি।"

        return Response({
            'success': True,
            'demand_id': demand.id,
            'total_candidates': count,
            'matching_version': version,
            'message_bn': msg_bn,
            'matches': candidates,
        }, status=status.HTTP_200_OK)


class DemandMatchDetailView(views.APIView):
    """
    GET /api/v1/demands/<demand_id>/matches/<match_id>/
    Retrieves detailed breakdown of a specific match candidate.
    """
    permission_classes = [permissions.IsAuthenticated, CanViewDemandMatchesPermission]

    def get(self, request, demand_id: int, match_id: int):
        demand = get_object_or_404(Demand, id=demand_id, is_deleted=False)
        match_candidate = get_match_detail(match_id)

        if not match_candidate or match_candidate.demand_id != demand.id:
            return Response({
                'success': False,
                'detail': 'ম্যাচ ক্যান্ডিডেট পাওয়া যায়নি।'
            }, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, match_candidate)

        serializer = MatchCandidateSerializer(match_candidate, context={'request': request})
        return Response({
            'success': True,
            'match': serializer.data
        }, status=status.HTTP_200_OK)


class DemandRematchView(views.APIView):
    """
    POST /api/v1/demands/<demand_id>/rematch/
    Allows requester or platform admin to trigger fresh re-matching.
    """
    permission_classes = [permissions.IsAuthenticated, CanTriggerRematchPermission]

    def post(self, request, demand_id: int):
        demand = get_object_or_404(Demand, id=demand_id, is_deleted=False)
        self.check_object_permissions(request, demand)

        version = request.data.get('version', 'v1')

        try:
            matching_run = MatchingEngine.rematch_demand(
                demand_id=demand.id,
                user=request.user,
                version=version
            )
            serializer = MatchingRunSerializer(matching_run)

            return Response({
                'success': True,
                'message_bn': f"পুনঃম্যাচিং সম্পন্ন হয়েছে। {matching_run.candidate_count} জন সম্ভাব্য সেবাদাতা পাওয়া গেছে।",
                'matching_run': serializer.data
            }, status=status.HTTP_200_OK)

        except (ValidationError, PermissionDenied) as e:
            return Response({
                'success': False,
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class MatchingRunListView(views.APIView):
    """
    GET /api/v1/matching/runs/
    Administrative monitoring view for matching engine execution runs.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        runs = MatchingRun.objects.all().order_by('-created_at')[:50]
        serializer = MatchingRunSerializer(runs, many=True)
        return Response({
            'success': True,
            'count': runs.count(),
            'runs': serializer.data
        }, status=status.HTTP_200_OK)


class MatchingRunDetailView(views.APIView):
    """
    GET /api/v1/matching/runs/<int:run_id>/
    Administrative view for specific run details.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, run_id: int):
        run = get_object_or_404(MatchingRun, id=run_id)
        serializer = MatchingRunSerializer(run)
        return Response({
            'success': True,
            'run': serializer.data
        }, status=status.HTTP_200_OK)
