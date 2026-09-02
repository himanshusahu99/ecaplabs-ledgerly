"""Runs the agent on an invoice and stores a validated result."""

import logging
from datetime import date

from core.abstractions.base_service import BaseService
from core.utils.money_utilities import MoneyUtilities
from invoices.agents.invoice_extraction_agent import InvoiceExtractionAgent
from invoices.choices import InvoiceStatus
from invoices.clients.llm_client_factory import LLMClientFactory
from invoices.dtos import ExtractedLineItemDTO, InvoiceExtractionDTO
from invoices.exceptions import ExtractionError
from invoices.repositories.invoice_repository import InvoiceRepository

logger = logging.getLogger(__name__)


class InvoiceExtractionService(BaseService):
    """Extracts, normalises and validates one invoice."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invoice_repository = InvoiceRepository()

    def extract(self, *, invoice_id):
        """Runs extraction and leaves the invoice in needs_review or failed."""
        invoice = self.invoice_repository.get_by_id(invoice_id=invoice_id)
        self.invoice_repository.set_status(
            invoice=invoice, status=InvoiceStatus.EXTRACTING
        )
        agent = None
        try:
            agent = InvoiceExtractionAgent(
                business=invoice.business,
                llm_client=LLMClientFactory.build(
                    document_sha256=invoice.document_sha256
                ),
            )
            run = agent.run(document_text=invoice.document_text)
            extraction = self._normalise(submission=run.submission)
            self._validate(extraction=extraction)
        except (ExtractionError, ValueError) as error:
            logger.warning("invoice %s extraction failed: %s", invoice.pk, error)
            transcript = agent.run_state.transcript if agent else []
            return self.invoice_repository.save_failure(
                invoice=invoice, error=str(error), transcript=transcript
            )
        return self.invoice_repository.save_extraction(
            invoice=invoice,
            extraction=extraction,
            payee=run.payee,
            transcript=run.transcript,
        )

    @staticmethod
    def _normalise(*, submission):
        """Turns the agent's strings into typed fields."""
        return InvoiceExtractionDTO(
            vendor_name=submission["vendor_name"],
            invoice_number=submission["invoice_number"] or "",
            currency=submission["currency"].upper(),
            total_amount=MoneyUtilities.parse_amount(value=submission["total"]),
            due_date=(
                date.fromisoformat(submission["due_date"])
                if submission["due_date"]
                else None
            ),
            line_items=[
                ExtractedLineItemDTO(
                    description=item["description"],
                    amount=MoneyUtilities.parse_amount(value=item["amount"]),
                )
                for item in submission["line_items"]
            ],
        )

    @staticmethod
    def _validate(*, extraction):
        """Rejects extractions whose line items do not add up to the total."""
        if not extraction.line_items:
            return
        line_total = MoneyUtilities.sum_amounts(
            amounts=[item.amount for item in extraction.line_items]
        )
        if line_total != extraction.total_amount:
            raise ExtractionError(
                f"line items sum to {line_total}, invoice total is {extraction.total_amount}"
            )
