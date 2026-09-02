"""Data access for invoices."""

from core.abstractions.base_repository import BaseRepository
from invoices.choices import InvoiceStatus
from invoices.models import Invoice


class InvoiceRepository(BaseRepository):
    """Queries over Invoice."""

    model = Invoice

    def list_for_business(self, *, business_id):
        """Returns a business's invoices, newest first."""
        return self.objects.filter(business__business_id=business_id).select_related(
            "payee"
        )

    def get_for_business(self, *, business_id, invoice_id):
        """Returns the business's invoice with this id, or None."""
        return (
            self.objects.filter(business__business_id=business_id, pk=invoice_id)
            .select_related("business", "payee")
            .first()
        )

    def get_by_id(self, *, invoice_id):
        """Returns the invoice with this id."""
        return self.objects.select_related("business").get(pk=invoice_id)

    def create(self, *, business, source_filename, document_sha256, document_text):
        """Inserts an uploaded invoice."""
        return self.objects.create(
            business=business,
            source_filename=source_filename,
            document_sha256=document_sha256,
            document_text=document_text,
        )

    def set_status(self, *, invoice, status):
        """Moves an invoice to a new status."""
        invoice.status = status
        invoice.save(update_fields=["status", "updated_at"])
        return invoice

    def save_extraction(self, *, invoice, extraction, payee, transcript):
        """Stores a successful extraction and queues it for review."""
        invoice.vendor_name = extraction.vendor_name
        invoice.invoice_number = extraction.invoice_number
        invoice.currency = extraction.currency
        invoice.total_amount = extraction.total_amount
        invoice.due_date = extraction.due_date
        invoice.line_items = [item.to_json() for item in extraction.line_items]
        invoice.payee = payee
        invoice.agent_transcript = transcript
        invoice.extraction_error = ""
        invoice.status = InvoiceStatus.NEEDS_REVIEW
        invoice.save()
        return invoice

    def save_failure(self, *, invoice, error, transcript):
        """Stores why extraction failed."""
        invoice.extraction_error = error
        invoice.agent_transcript = transcript
        invoice.status = InvoiceStatus.FAILED
        invoice.save(
            update_fields=[
                "extraction_error",
                "agent_transcript",
                "status",
                "updated_at",
            ]
        )
        return invoice

    def mark_approved(self, *, invoice, processor_payment_id):
        """Records the Paystream payment created for this invoice."""
        invoice.processor_payment_id = processor_payment_id
        invoice.status = InvoiceStatus.APPROVED
        invoice.save(update_fields=["processor_payment_id", "status", "updated_at"])
        return invoice
