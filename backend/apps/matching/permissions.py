"""
Permissions for SebaCox Matching Engine.
Phase 7: Object-Level Authorization & IDOR Protection.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from rest_framework import permissions
from apps.demands.constants import DemandVisibility


class CanViewDemandMatchesPermission(permissions.BasePermission):
    """
    Object-level permission for viewing Demand matches:
    - Requester of the demand: ALLOWED
    - Admin / Staff: ALLOWED
    - Other users: DENIED
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # obj can be Demand or MatchCandidate
        demand = obj if hasattr(obj, 'requester_id') else getattr(obj, 'demand', None)

        if not demand:
            return False

        user = request.user
        if user.is_staff or user.is_superuser:
            return True

        # Private Demand isolation
        if getattr(demand, 'visibility', None) == DemandVisibility.PRIVATE:
            return demand.requester_id == user.id

        # Requester can view all matches for their demand
        if demand.requester_id == user.id:
            return True

        # If obj is a MatchCandidate and user is the provider owner, allow viewing their own candidate record
        if hasattr(obj, 'provider') and obj.provider and getattr(obj.provider, 'user_id', None) == user.id:
            return True

        return False


class CanTriggerRematchPermission(permissions.BasePermission):
    """
    Permission to trigger rematching on a demand:
    - Only demand requester or admin.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        demand = obj if hasattr(obj, 'requester_id') else getattr(obj, 'demand', None)
        if not demand:
            return False

        user = request.user
        return bool(user.is_staff or user.is_superuser or demand.requester_id == user.id)
