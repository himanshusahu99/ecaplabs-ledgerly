"""Invoice model."""

from core.models import Business
from django.db import models
from invoices.choices import InvoiceStatus
from payments.models import Payee


class Invoice(models.Model):
    """An uploaded vendor invoice and what the agent extracted from it."""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="invoices"
    )
    payee = models.ForeignKey(
        Payee, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices"
    )
    source_filename = models.CharField(max_length=255)
    document_sha256 = models.CharField(max_length=64, db_index=True)
    document_text = models.TextField()
    status = models.CharField(
        max_length=16, choices=InvoiceStatus.choices, default=InvoiceStatus.UPLOADED
    )
    vendor_name = models.CharField(max_length=255, blank=True)
    invoice_number = models.CharField(max_length=64, blank=True)
    currency = models.CharField(max_length=3, blank=True)
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    due_date = models.DateField(null=True, blank=True)
    line_items = models.JSONField(default=list, blank=True)
    extraction_error = models.TextField(blank=True)
    agent_transcript = models.JSONField(default=list, blank=True)
    processor_payment_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source_filename} {self.status}"
