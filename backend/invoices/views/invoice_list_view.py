"""Invoice list and upload endpoint."""

from core.abstractions.base_view import BaseBusinessView
from core.exceptions import BaseAPIException
from invoices.serializers import InvoiceSerializer
from invoices.services.invoice_service import InvoiceService
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class InvoiceListView(BaseBusinessView):
    """Lists invoices and accepts new uploads."""

    parser_classes = [MultiPartParser]

    def get(self, request, business_id):
        invoices = InvoiceService().list_for_business(business_id=business_id)
        return Response(InvoiceSerializer(invoices, many=True).data)

    def post(self, request, business_id):
        uploaded_file = request.FILES.get("file")
        if uploaded_file is None:
            raise BaseAPIException(detail="Attach a file.")
        invoice = InvoiceService().upload(
            business_id=business_id, uploaded_file=uploaded_file
        )
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
