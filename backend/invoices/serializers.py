"""API shapes for invoices."""

from invoices.models import Invoice
from rest_framework import serializers


class InvoiceSerializer(serializers.ModelSerializer):
    """An invoice as the review screen shows it."""

    payee_id = serializers.IntegerField(source="payee.pk", read_only=True, default=None)
    payee_name = serializers.CharField(
        source="payee.name", read_only=True, default=None
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "source_filename",
            "status",
            "vendor_name",
            "invoice_number",
            "currency",
            "total_amount",
            "due_date",
            "payee_id",
            "payee_name",
            "line_items",
            "extraction_error",
            "created_at",
        ]
