"""Payment list endpoint."""

from core.abstractions.base_view import BaseBusinessView
from payments.serializers import PaymentSerializer
from payments.services.payment_query_service import PaymentQueryService
from rest_framework.response import Response


class PaymentListView(BaseBusinessView):
    """Lists a business's payments, newest first."""

    def get(self, request, business_id):
        payments = PaymentQueryService().list_for_business(business_id=business_id)
        return Response(PaymentSerializer(payments, many=True).data)
