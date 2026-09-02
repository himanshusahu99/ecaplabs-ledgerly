"""Sends a signed Paystream event to the local webhook endpoint."""

import json
import uuid

from core.utils.signature_utilities import SignatureUtilities
from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client
from django.utils import timezone
from payments.constants import PAYSTREAM_SIGNATURE_HEADER


class Command(BaseCommand):
    """Posts one event, signed the way Paystream signs it."""

    help = 'Send a signed Paystream event: send_test_webhook payment.settled --data \'{"id": "pp_..."}\''

    def add_arguments(self, parser):
        parser.add_argument("type", help="Event type, e.g. payment.settled")
        parser.add_argument("--data", required=True, help="JSON for event.data")
        parser.add_argument("--event-id", help="Defaults to a fresh evt_ id")

    def handle(self, *args, **options):
        event = {
            "id": options["event_id"] or f"evt_{uuid.uuid4().hex[:16]}",
            "type": options["type"],
            "created": timezone.now().isoformat(),
            "data": json.loads(options["data"]),
        }
        body = json.dumps(event).encode()
        response = Client().post(
            "/webhooks/paystream/",
            data=body,
            content_type="application/json",
            headers={
                PAYSTREAM_SIGNATURE_HEADER: SignatureUtilities.sign(
                    secret=settings.PAYSTREAM_WEBHOOK_SECRET, body=body
                )
            },
        )
        self.stdout.write(f"{event['id']} -> {response.status_code}")
