"""Access rules shared across apps."""

from core.repositories.membership_repository import MembershipRepository
from rest_framework.permissions import BasePermission


class IsBusinessMember(BasePermission):
    """Allows access only to members of the business named in the URL."""

    def has_permission(self, request, view):
        return MembershipRepository().is_member(
            user=request.user, business_id=view.kwargs.get("business_id")
        )
