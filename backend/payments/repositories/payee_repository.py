"""Data access for payees."""

from core.abstractions.base_repository import BaseRepository
from payments.models import Payee


class PayeeRepository(BaseRepository):
    """Queries over Payee."""

    model = Payee

    def get_for_business(self, *, business, payee_id):
        """Returns the business's payee with this id, or None."""
        return self.objects.filter(business=business, pk=payee_id).first()

    def find_by_name(self, *, business, name):
        """Returns the business's payees with exactly this name."""
        return list(self.objects.filter(business=business, name=name))

    def create(self, *, business, name, email):
        """Inserts a payee."""
        return self.objects.create(business=business, name=name, email=email)
