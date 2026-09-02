"""Data access for payments."""

from core.abstractions.base_repository import BaseRepository
from core.utils.money_utilities import MoneyUtilities
from django.db.models import Sum
from payments.choices import PaymentStatus
from payments.constants import OUTSTANDING_STATUSES
from payments.models import Payment


class PaymentRepository(BaseRepository):
    """Queries over Payment."""

    model = Payment

    def list_for_business(self, *, business_id):
        """Returns a business's payments, newest first, with payees joined."""
        return self.objects.filter(business__business_id=business_id).select_related(
            "payee"
        )

    def get_by_processor_payment_id(self, *, processor_payment_id):
        """Returns the payment Paystream knows by this id, or None."""
        return self.objects.filter(processor_payment_id=processor_payment_id).first()

    @BaseRepository.log_execution_time("create payment from processor event")
    def create(
        self,
        *,
        business,
        payee,
        processor_payment_id,
        amount,
        currency,
        memo,
        scheduled_for,
    ):
        """Inserts a payment."""
        return self.objects.create(
            business=business,
            payee=payee,
            processor_payment_id=processor_payment_id,
            amount=amount,
            currency=currency,
            memo=memo,
            scheduled_for=scheduled_for,
        )

    def update_status(self, *, payment, status):
        """Moves a payment to a new status."""
        payment.status = status
        payment.save(update_fields=["status", "updated_at"])
        return payment

    def outstanding_total(self, *, business_id):
        """Sum of payments not yet settled, failed or cancelled."""
        return self._total(
            business_id=business_id, filters={"status__in": OUTSTANDING_STATUSES}
        )

    def settled_total_since(self, *, business_id, since):
        """Sum of payments that settled on or after since."""
        return self._total(
            business_id=business_id,
            filters={"status": PaymentStatus.SETTLED, "updated_at__gte": since},
        )

    def _total(self, *, business_id, filters):
        """Sums amount over a filtered slice of one business's payments."""
        total = (
            self.objects.filter(business__business_id=business_id, **filters)
            .aggregate(total=Sum("amount"))
            .get("total")
        )
        return MoneyUtilities.to_cents(value=total)
