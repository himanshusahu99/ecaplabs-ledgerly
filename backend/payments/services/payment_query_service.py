"""Read-side logic for the payments dashboard."""

from core.abstractions.base_service import BaseService
from django.utils import timezone
from payments.constants import DEFAULT_CURRENCY
from payments.dtos import PaymentSummaryDTO
from payments.repositories.payment_repository import PaymentRepository


class PaymentQueryService(BaseService):
    """Lists payments and computes dashboard totals."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_repository = PaymentRepository()

    def list_for_business(self, *, business_id):
        """Returns a business's payments, newest first."""
        return self.payment_repository.list_for_business(business_id=business_id)

    def summary_for_business(self, *, business_id):
        """Returns outstanding and settled-this-month totals."""
        month_start = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return PaymentSummaryDTO(
            outstanding=self.payment_repository.outstanding_total(
                business_id=business_id
            ),
            settled_this_month=self.payment_repository.settled_total_since(
                business_id=business_id, since=month_start
            ),
            currency=DEFAULT_CURRENCY,
        )
