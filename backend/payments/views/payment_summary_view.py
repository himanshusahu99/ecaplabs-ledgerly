"""Dashboard totals endpoint."""

from core.abstractions.base_view import BaseBusinessView
from payments.services.payment_query_service import PaymentQueryService
from rest_framework.response import Response


class PaymentSummaryView(BaseBusinessView):
    """Totals for the dashboard cards."""

    def get(self, request, business_id):
        summary = PaymentQueryService().summary_for_business(business_id=business_id)
        return Response(summary.to_response())
