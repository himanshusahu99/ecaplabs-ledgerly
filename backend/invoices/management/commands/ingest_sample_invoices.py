"""Runs the extraction agent over the sample invoice inbox."""

from django.conf import settings
from django.core.management.base import BaseCommand
from invoices.services.invoice_service import InvoiceService

SAMPLE_INBOX_DIR = settings.BASE_DIR / "fixtures" / "invoices"


class Command(BaseCommand):
    """Ingests every .txt in fixtures/invoices for one business."""

    help = "Ingest sample invoices: ingest_sample_invoices --business ECL-1001"

    def add_arguments(self, parser):
        parser.add_argument("--business", required=True, help="ECL business id")

    def handle(self, *args, **options):
        service = InvoiceService()
        for path in sorted(SAMPLE_INBOX_DIR.glob("*.txt")):
            invoice = service.create_from_text(
                business_id=options["business"],
                source_filename=path.name,
                document_text=path.read_text(),
            )
            self.stdout.write(
                f"{path.name}: {invoice.status} {invoice.currency} {invoice.total_amount}"
            )
