"""Data access for memberships."""

from core.abstractions.base_repository import BaseRepository
from core.models import Membership


class MembershipRepository(BaseRepository):
    """Queries over Membership."""

    model = Membership

    def is_member(self, *, user, business_id):
        """True when the user can act for the business."""
        return self.objects.filter(
            user=user, business__business_id=business_id
        ).exists()
