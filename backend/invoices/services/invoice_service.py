"""Upload, approve and reject invoices."""

import hashlib
import logging
from pathlib import Path

from core.abstractions.base_service import BaseService
from core.exceptions import BaseAPIException, ConflictError, ObjectNotFoundError
from core.repositories.business_repository import BusinessRepository
from invoices.choices import InvoiceStatus
from invoices.constants import ALLOWED_UPLOAD_EXTENSIONS, MAX_UPLOAD_BYTES
from invoices.repositories.invoice_repository import InvoiceRepository
from invoices.tasks import extract_invoice_task
from payments.clients.paystream_client import PaystreamClient

logger = logging.getLogger(__name__)


class InvoiceService(BaseService):
    """Invoice lifecycle outside of extraction itself."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.business_repository = BusinessRepository()
        self.invoice_repository = InvoiceRepository()
        self.paystream_client = PaystreamClient()

    def list_for_business(self, *, business_id):
        """Returns a business's invoices, newest first."""
        return self.invoice_repository.list_for_business(business_id=business_id)

    def upload(self, *, business_id, uploaded_file):
        """Accepts an OCR text export and starts extraction."""
        if Path(uploaded_file.name).suffix.lower() not in ALLOWED_UPLOAD_EXTENSIONS:
            raise BaseAPIException(detail="Upload the OCR export as a .txt file.")
        if uploaded_file.size > MAX_UPLOAD_BYTES:
            raise BaseAPIException(detail="File is too large.")
        return self.create_from_text(
            business_id=business_id,
            source_filename=uploaded_file.name,
            document_text=uploaded_file.read().decode("utf-8"),
        )

    def create_from_text(self, *, business_id, source_filename, document_text):
        """Stores the document and runs extraction in the background."""
        business = self.business_repository.get_by_business_id(business_id=business_id)
        invoice = self.invoice_repository.create(
            business=business,
            source_filename=source_filename,
            document_sha256=hashlib.sha256(document_text.encode()).hexdigest(),
            document_text=document_text,
        )
        extract_invoice_task.delay(invoice_id=invoice.pk)
        invoice.refresh_from_db()
        return invoice

    def approve(self, *, business_id, invoice_id):
        """Schedules the payment in Paystream."""
        invoice = self._get_reviewable(business_id=business_id, invoice_id=invoice_id)
        if invoice.payee is None:
            raise ConflictError(detail="Invoice has no payee.")
        created = self.paystream_client.create_payment(
            business_id=business_id,
            payee_id=invoice.payee.pk,
            amount=invoice.total_amount,
            currency=invoice.currency,
            memo=f"Invoice {invoice.invoice_number}".strip(),
            scheduled_for=invoice.due_date,
        )
        logger.info("invoice %s approved, paystream id=%s", invoice.pk, created["id"])
        return self.invoice_repository.mark_approved(
            invoice=invoice, processor_payment_id=created["id"]
        )

    def reject(self, *, business_id, invoice_id):
        """Marks the invoice rejected."""
        invoice = self._get_reviewable(business_id=business_id, invoice_id=invoice_id)
        return self.invoice_repository.set_status(
            invoice=invoice, status=InvoiceStatus.REJECTED
        )

    def _get_reviewable(self, *, business_id, invoice_id):
        """Returns the invoice if it is waiting for review."""
        invoice = self.invoice_repository.get_for_business(
            business_id=business_id, invoice_id=invoice_id
        )
        if invoice is None:
            raise ObjectNotFoundError()
        if invoice.status != InvoiceStatus.NEEDS_REVIEW:
            raise ConflictError(detail=f"Invoice is {invoice.status}.")
        return invoice
