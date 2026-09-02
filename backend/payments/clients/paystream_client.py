"""Client for the Paystream payments API."""

import logging
import uuid

from core.abstractions.base_api_client import BaseAPIClient
from django.conf import settings

logger = logging.getLogger(__name__)

PAYSTREAM_TIMEOUT_SECONDS = 10


class PaystreamClient(BaseAPIClient):
    """Creates payments in Paystream; stubs locally when no URL is set."""

    service_name = "paystream"

    def __init__(self, **kwargs):
        super().__init__(
            base_url=settings.PAYSTREAM_API_URL,
            timeout_seconds=PAYSTREAM_TIMEOUT_SECONDS,
            **kwargs,
        )

    def create_payment(
        self, *, business_id, payee_id, amount, currency, memo, scheduled_for
    ):
        """Schedules a payment; Paystream confirms it later via payment.created."""
        payload = {
            "business_id": business_id,
            "payee_id": payee_id,
            "amount": str(amount),
            "currency": currency,
            "memo": memo,
            "scheduled_for": scheduled_for.isoformat() if scheduled_for else None,
        }
        if not self.is_configured:
            stub_id = f"pp_stub_{uuid.uuid4().hex[:10]}"
            logger.info(
                "paystream not configured, stubbed create_payment id=%s", stub_id
            )
            return {"id": stub_id, "status": "pending"}
        return self.post(path="/v1/payments", payload=payload)
