"""Tests for extraction, upload and approval."""

from unittest import mock

from core.tests.factories import CoreFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from invoices.choices import InvoiceStatus
from invoices.models import Invoice
from invoices.services.invoice_extraction_service import InvoiceExtractionService
from invoices.tests.factories import ScriptedLLMClient, TurnFactory
from payments.tests.factories import PaymentFactory

FACTORY_PATH = "invoices.services.invoice_extraction_service.LLMClientFactory.build"


class InvoiceFlowTests(TestCase):
    """Upload, extract, review."""

    def setUp(self):
        self.business = CoreFactory.business()
        self.payee = PaymentFactory.payee(business=self.business, name="Vendor")
        self.client = CoreFactory.api_client(
            user=CoreFactory.member(business=self.business)
        )

    def scripted(self, *, total="1,250.00", line_items=None):
        """Patches the LLM factory with a find-then-submit script."""
        return mock.patch(
            FACTORY_PATH,
            return_value=ScriptedLLMClient(
                turns=[
                    TurnFactory.tool_call(
                        name="find_payee", tool_input={"name": "Vendor"}
                    ),
                    TurnFactory.submission(total=total, line_items=line_items),
                ]
            ),
        )

    def upload(self):
        """Uploads a small OCR export."""
        return self.client.post(
            "/api/businesses/ECL-9001/invoices/",
            data={"file": SimpleUploadedFile("inv.txt", b"INVOICE INV-1")},
            format="multipart",
        )

    def test_upload_extracts_for_review(self):
        with self.scripted():
            response = self.upload()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], InvoiceStatus.NEEDS_REVIEW)
        self.assertEqual(response.json()["total_amount"], "1250.00")
        self.assertEqual(response.json()["payee_name"], "Vendor")

    def test_line_items_must_add_up(self):
        with self.scripted(
            total="100.00",
            line_items=[
                {"description": "a", "amount": "60.00"},
                {"description": "b", "amount": "30.00"},
            ],
        ):
            response = self.upload()
        self.assertEqual(response.json()["status"], InvoiceStatus.FAILED)
        self.assertIn("line items sum to 90.00", response.json()["extraction_error"])

    def test_rejects_non_text_upload(self):
        response = self.client.post(
            "/api/businesses/ECL-9001/invoices/",
            data={"file": SimpleUploadedFile("inv.pdf", b"%PDF")},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)

    def test_approve_schedules_payment(self):
        with self.scripted():
            invoice_id = self.upload().json()["id"]
        response = self.client.post(
            f"/api/businesses/ECL-9001/invoices/{invoice_id}/approve/"
        )
        self.assertEqual(response.json()["status"], InvoiceStatus.APPROVED)
        self.assertTrue(
            Invoice.objects.get(pk=invoice_id).processor_payment_id.startswith(
                "pp_stub_"
            )
        )

    def test_cannot_approve_twice(self):
        with self.scripted():
            invoice_id = self.upload().json()["id"]
        self.client.post(f"/api/businesses/ECL-9001/invoices/{invoice_id}/approve/")
        response = self.client.post(
            f"/api/businesses/ECL-9001/invoices/{invoice_id}/approve/"
        )
        self.assertEqual(response.status_code, 409)

    def test_missing_recording_fails_cleanly(self):
        invoice = Invoice.objects.create(
            business=self.business,
            source_filename="x.txt",
            document_sha256="0" * 64,
            document_text="x",
        )
        InvoiceExtractionService().extract(invoice_id=invoice.pk)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, InvoiceStatus.FAILED)
        self.assertIn("no recording", invoice.extraction_error)
        self.assertIsNone(invoice.total_amount)
