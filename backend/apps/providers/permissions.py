"""
Permissions for Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from rest_framework import permissions


class IsProviderOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission allowing only the owner of a provider profile
    (or staff/admin) to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only requests are allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'is_staff', False):
            return True

        # Support Provider, ProviderService, and ProviderServiceArea objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'provider'):
            return obj.provider.user == request.user

        return False


class IsProviderOwner(permissions.BasePermission):
    """
    Strict permission requiring the user to be the owner of the provider profile.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'is_staff', False):
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'provider'):
            return obj.provider.user == request.user

        return False
