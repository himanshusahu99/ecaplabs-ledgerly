"""Background tasks for invoices."""

from celery import shared_task


@shared_task
def extract_invoice_task(invoice_id):
    """Runs the extraction agent for one invoice."""
    from invoices.services.invoice_extraction_service import InvoiceExtractionService

    InvoiceExtractionService().extract(invoice_id=invoice_id)
