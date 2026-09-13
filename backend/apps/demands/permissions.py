"""
Object-Level Permissions for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from rest_framework import permissions
from .constants import DemandVisibility


class IsDemandOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a Demand to edit or mutate it.
    Read permissions depend on visibility and publication status.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions: check demand visibility
        if request.method in permissions.SAFE_METHODS:
            return obj.can_view_by(request.user)

        # Write permissions: strictly owner or staff/superuser
        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.requester_id == request.user.id


class IsDemandOwner(permissions.BasePermission):
    """
    Strict permission requiring requester ownership for actions like publish, pause, cancel.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.requester_id == request.user.id
