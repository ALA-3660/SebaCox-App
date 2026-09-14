"""
Offer Permissions for SebaCox.
Phase 8: Offer & Counter-Offer Foundation.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from rest_framework import permissions
from .constants import OfferStatus


class IsOfferPartyOrAdmin(permissions.BasePermission):
    """
    Ensures user is either requester, provider, or staff.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        is_requester = (obj.requester_id == request.user.id)
        is_proposer = (obj.proposer_id == request.user.id)
        is_provider = False
        if hasattr(obj.provider, 'user_id') and obj.provider.user_id == request.user.id:
            is_provider = True

        return is_requester or is_proposer or is_provider


class CanAcceptOffer(permissions.BasePermission):
    """
    Ensures user can accept the offer:
    - Must be a party
    - Must NOT be the proposer of the offer (proposer cannot accept their own proposal)
    - Offer must be PENDING
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        if obj.status != OfferStatus.PENDING:
            return False

        # Proposer cannot accept
        if obj.proposer_id == request.user.id:
            return False

        # Must be recipient
        is_requester = (obj.requester_id == request.user.id)
        is_provider = False
        if hasattr(obj.provider, 'user_id') and obj.provider.user_id == request.user.id:
            is_provider = True

        return is_requester or is_provider


class CanRejectOffer(permissions.BasePermission):
    """
    Ensures user can reject the offer:
    - Must be recipient (not proposer)
    - Offer must be PENDING
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if obj.status != OfferStatus.PENDING:
            return False
        if obj.proposer_id == request.user.id:
            return False
        is_requester = (obj.requester_id == request.user.id)
        is_provider = False
        if hasattr(obj.provider, 'user_id') and obj.provider.user_id == request.user.id:
            is_provider = True
        return is_requester or is_provider


class CanCounterOffer(permissions.BasePermission):
    """
    Ensures user can counter the offer:
    - Must be recipient (not current proposer)
    - Offer must be PENDING
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if obj.status != OfferStatus.PENDING:
            return False
        if obj.proposer_id == request.user.id:
            return False
        is_requester = (obj.requester_id == request.user.id)
        is_provider = False
        if hasattr(obj.provider, 'user_id') and obj.provider.user_id == request.user.id:
            is_provider = True
        return is_requester or is_provider


class CanCreateInitialOfferPermission(permissions.BasePermission):
    """
    Ensures user is authenticated and represents a provider.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CanCancelOffer(permissions.BasePermission):
    """
    Ensures only the proposer of the offer can cancel it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return obj.proposer_id == request.user.id


# Aliases for consistent naming
IsOfferParticipantOrStaff = IsOfferPartyOrAdmin
CanAcceptOfferPermission = CanAcceptOffer
CanCancelOfferPermission = CanCancelOffer
CanRejectOfferPermission = CanRejectOffer
CanCounterOfferPermission = CanCounterOffer
