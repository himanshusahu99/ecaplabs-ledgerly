"""Data access for businesses."""

from core.abstractions.base_repository import BaseRepository
from core.models import Business


class BusinessRepository(BaseRepository):
    """Queries over Business."""

    model = Business

    def get_by_business_id(self, *, business_id):
        """Returns the business with this ECL id, or None."""
        return self.objects.filter(business_id=business_id).first()

    def list_for_user(self, *, user):
        """Returns businesses the user is a member of, by name."""
        return self.objects.filter(memberships__user=user).order_by("name")
