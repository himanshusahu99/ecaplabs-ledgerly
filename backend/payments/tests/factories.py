"""Test data builders for payments."""

import json
from decimal import Decimal

from core.utils.signature_utilities import SignatureUtilities
from django.conf import settings
from payments.choices import PaymentStatus
from payments.constants import PAYSTREAM_SIGNATURE_HEADER
from payments.models import Payee, Payment


class PaymentFactory:
    """Creates payees, payments and signed Paystream events."""

    @staticmethod
    def payee(*, business, name="Vendor", email="ar@vendor.test"):
        """Creates a payee."""
        return Payee.objects.create(business=business, name=name, email=email)

    @staticmethod
    def payment(
        *,
        business,
        payee,
        processor_payment_id="pp_1",
        amount="100.00",
        status=PaymentStatus.PENDING,
    ):
        """Creates a payment directly, bypassing webhooks."""
        return Payment.objects.create(
            business=business,
            payee=payee,
            processor_payment_id=processor_payment_id,
            amount=Decimal(amount),
            status=status,
        )

    @staticmethod
    def created_event_data(
        *, business, payee, processor_payment_id="pp_1", amount="100.00"
    ):
        """Builds payment.created data."""
        return {
            "id": processor_payment_id,
            "business_id": business.business_id,
            "payee_id": payee.pk,
            "amount": amount,
            "currency": "USD",
        }

    @staticmethod
    def post_event(*, client, event_type, data, event_id="evt_test"):
        """Posts a signed Paystream event with any Django test client."""
        body = json.dumps({"id": event_id, "type": event_type, "data": data}).encode()
        return client.post(
            "/webhooks/paystream/",
            data=body,
            content_type="application/json",
            headers={
                PAYSTREAM_SIGNATURE_HEADER: SignatureUtilities.sign(
                    secret=settings.PAYSTREAM_WEBHOOK_SECRET, body=body
                )
            },
        )
