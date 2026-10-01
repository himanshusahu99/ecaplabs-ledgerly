"""Data access for payees."""

from core.abstractions.base_repository import BaseRepository
from django.utils import timezone
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

    def update_remittance(self, *, payee, routing_number, account_number, updated_by):
        """Changes where payments to this payee are sent."""
        payee.remittance_routing_number = routing_number
        payee.remittance_account_number = account_number
        payee.remittance_updated_at = timezone.now()
        payee.remittance_updated_by = updated_by
        payee.save(
            update_fields=[
                "remittance_routing_number",
                "remittance_account_number",
                "remittance_updated_at",
                "remittance_updated_by",
            ]
        )
        return payee
