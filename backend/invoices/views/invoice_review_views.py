"""Approve and reject endpoints."""

from core.abstractions.base_view import BaseBusinessView
from invoices.serializers import InvoiceSerializer
from invoices.services.invoice_service import InvoiceService
from rest_framework.response import Response


class InvoiceApproveView(BaseBusinessView):
    """Approves an invoice and schedules its payment."""

    def post(self, request, business_id, invoice_id):
        invoice = InvoiceService().approve(
            business_id=business_id, invoice_id=invoice_id
        )
        return Response(InvoiceSerializer(invoice).data)


class InvoiceRejectView(BaseBusinessView):
    """Rejects an invoice."""

    def post(self, request, business_id, invoice_id):
        invoice = InvoiceService().reject(
            business_id=business_id, invoice_id=invoice_id
        )
        return Response(InvoiceSerializer(invoice).data)
