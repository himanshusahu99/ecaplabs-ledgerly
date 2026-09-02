"""Paystream webhook endpoint."""

from core.abstractions.base_webhook_view import BaseWebhookView
from core.utils.signature_utilities import SignatureUtilities
from django.conf import settings
from payments.constants import PAYSTREAM_PROVIDER, PAYSTREAM_SIGNATURE_HEADER
from payments.webhook_processors.paystream_webhook_processor import (
    PaystreamWebhookProcessor,
)


class PaystreamWebhookView(BaseWebhookView):
    """Receives Paystream events."""

    provider = PAYSTREAM_PROVIDER

    def verify_signature(self, *, request):
        return SignatureUtilities.is_valid(
            secret=settings.PAYSTREAM_WEBHOOK_SECRET,
            body=request.body,
            signature=request.headers.get(PAYSTREAM_SIGNATURE_HEADER),
        )

    def build_processor(self):
        return PaystreamWebhookProcessor()
