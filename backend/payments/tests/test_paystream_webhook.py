"""Tests for the Paystream webhook."""

from decimal import Decimal

from core.tests.factories import CoreFactory
from django.test import TestCase
from payments.choices import PaymentStatus
from payments.models import Payment
from payments.tests.factories import PaymentFactory
from rest_framework.test import APIClient


class PaystreamWebhookTests(TestCase):
    """Paystream events update local payments."""

    def setUp(self):
        self.business = CoreFactory.business()
        self.payee = PaymentFactory.payee(business=self.business)
        self.client = APIClient()

    def test_rejects_bad_signature(self):
        response = self.client.post(
            "/webhooks/paystream/",
            data=b"{}",
            content_type="application/json",
            headers={"X-Paystream-Signature": "nope"},
        )
        self.assertEqual(response.status_code, 401)

    def test_created_records_payment(self):
        response = PaymentFactory.post_event(
            client=self.client,
            event_type="payment.created",
            data=PaymentFactory.created_event_data(
                business=self.business, payee=self.payee, amount="1250.00"
            ),
        )
        self.assertEqual(response.status_code, 200)
        payment = Payment.objects.get(processor_payment_id="pp_1")
        self.assertEqual(payment.amount, Decimal("1250.00"))
        self.assertEqual(payment.status, PaymentStatus.PENDING)

    def test_status_events_move_payment(self):
        PaymentFactory.post_event(
            client=self.client,
            event_type="payment.created",
            data=PaymentFactory.created_event_data(
                business=self.business, payee=self.payee
            ),
        )
        for event_type in ("payment.processing", "payment.settled"):
            PaymentFactory.post_event(
                client=self.client, event_type=event_type, data={"id": "pp_1"}
            )
        self.assertEqual(
            Payment.objects.get(processor_payment_id="pp_1").status,
            PaymentStatus.SETTLED,
        )

    def test_status_event_for_unknown_payment_is_acknowledged(self):
        response = PaymentFactory.post_event(
            client=self.client, event_type="payment.settled", data={"id": "pp_missing"}
        )
        self.assertEqual(response.status_code, 200)
