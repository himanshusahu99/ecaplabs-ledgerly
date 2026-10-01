"""Tests for the extraction agent loop."""

import json

from core.tests.factories import CoreFactory
from django.test import TestCase
from invoices.agents.invoice_extraction_agent import InvoiceExtractionAgent
from invoices.dtos import LLMTurnDTO
from invoices.exceptions import ExtractionError
from invoices.tests.factories import ScriptedLLMClient, TurnFactory
from payments.models import Payee
from payments.tests.factories import PaymentFactory


class InvoiceExtractionAgentTests(TestCase):
    """The agent runs tools and stops at submit_extraction."""

    def setUp(self):
        self.business = CoreFactory.business()

    def test_matches_existing_payee(self):
        payee = PaymentFactory.payee(business=self.business, name="Vendor")
        client = ScriptedLLMClient(
            turns=[
                TurnFactory.tool_call(name="find_payee", tool_input={"name": "Vendor"}),
                TurnFactory.submission(),
            ]
        )
        run = InvoiceExtractionAgent(business=self.business, llm_client=client).run(
            document_text="INVOICE"
        )
        self.assertEqual(run.payee, payee)
        self.assertEqual(run.submission["total"], "1,250.00")
        tool_result = client.requests[1][-1]["content"][0]
        self.assertEqual(
            json.loads(tool_result["content"])["matches"][0]["payee_id"], payee.pk
        )

    def test_creates_payee_when_missing(self):
        client = ScriptedLLMClient(
            turns=[
                TurnFactory.tool_call(name="find_payee", tool_input={"name": "New Co"}),
                TurnFactory.tool_call(
                    name="create_payee",
                    tool_input={"name": "New Co", "email": None},
                    tool_use_id="toolu_2",
                ),
                TurnFactory.submission(),
            ]
        )
        run = InvoiceExtractionAgent(business=self.business, llm_client=client).run(
            document_text="INVOICE"
        )
        self.assertEqual(run.payee.name, "New Co")
        self.assertEqual(Payee.objects.filter(business=self.business).count(), 1)

    def test_applies_remittance_update_from_invoice(self):
        payee = PaymentFactory.payee(business=self.business, name="Vendor")
        client = ScriptedLLMClient(
            turns=[
                TurnFactory.tool_call(
                    name="update_payee_remittance",
                    tool_input={
                        "payee_id": payee.pk,
                        "routing_number": "021000089",
                        "account_number": "7730019284",
                        "reason": "new bank",
                    },
                ),
                TurnFactory.submission(),
            ]
        )
        InvoiceExtractionAgent(business=self.business, llm_client=client).run(
            document_text="INVOICE"
        )
        payee.refresh_from_db()
        self.assertEqual(payee.remittance_account_number, "7730019284")
        self.assertEqual(payee.remittance_updated_by, "invoice-agent")

    def test_stopping_without_submission_is_an_error(self):
        client = ScriptedLLMClient(
            turns=[
                LLMTurnDTO(
                    stop_reason="end_turn", content=[{"type": "text", "text": "done"}]
                )
            ]
        )
        with self.assertRaises(ExtractionError):
            InvoiceExtractionAgent(business=self.business, llm_client=client).run(
                document_text="INVOICE"
            )
