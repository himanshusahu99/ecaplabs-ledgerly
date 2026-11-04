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

    def test_duplicate_webhook_does_not_create_duplicate_payment(self):
        """Reproduces Acme Corp (ECL-1001): Paystream retried the same event_id after
        a timeout. Without an idempotency guard a second Payment row is inserted for
        the same processor payment, causing a ghost Pending record and an inflated
        Outstanding balance.
        """
        event_id = "evt_2e4e2decf15e1804"
        data = PaymentFactory.created_event_data(
            business=self.business,
            payee=self.payee,
            processor_payment_id="pp_22fd2ead98f621",
            amount="1250.00",
        )

        # Attempt 1 — Paystream sent this but our endpoint timed out on their side.
        # Our handler still processed it and created a Payment row.
        PaymentFactory.post_event(
            client=self.client,
            event_type="payment.created",
            data=data,
            event_id=event_id,
        )

        # Attempt 2 — Paystream retried with the SAME event_id one minute later.
        PaymentFactory.post_event(
            client=self.client,
            event_type="payment.created",
            data=data,
            event_id=event_id,
        )

        # There must be exactly ONE payment record — not two.
        count = Payment.objects.filter(processor_payment_id="pp_22fd2ead98f621").count()
        self.assertEqual(
            count,
            1,
            f"Expected 1 payment record but found {count}. "
            "Duplicate webhook event was not deduplicated.",
        )

    def test_settled_event_updates_the_correct_payment(self):
        """Guards against the ghost-record variant of the bug: when a duplicate
        payment.created produces two rows, the settled event should land on the
        payment that Paystream actually settled — and no Pending ghost should remain.

        Without the idempotency fix, payment.settled calls get_by_processor_payment_id
        which returns .first() — only one of the two rows is ever updated, leaving the
        other permanently stuck as Pending.
        """
        data = PaymentFactory.created_event_data(
            business=self.business,
            payee=self.payee,
            processor_payment_id="pp_22fd2ead98f621",
            amount="1250.00",
        )
        shared_event_id = "evt_2e4e2decf15e1804"

        # Send the same payment.created event twice (Paystream timeout + retry).
        for _ in range(2):
            PaymentFactory.post_event(
                client=self.client,
                event_type="payment.created",
                data=data,
                event_id=shared_event_id,
            )

        # Paystream reports the payment settled.
        PaymentFactory.post_event(
            client=self.client,
            event_type="payment.settled",
            data={"id": "pp_22fd2ead98f621"},
        )

        payments = list(Payment.objects.filter(processor_payment_id="pp_22fd2ead98f621"))

        # After the fix: exactly one record, and it must be Settled.
        self.assertEqual(
            len(payments),
            1,
            f"Expected 1 payment but found {len(payments)} — idempotency guard missing.",
        )
        self.assertEqual(
            payments[0].status,
            PaymentStatus.SETTLED,
            "The single payment record must be Settled after payment.settled fires.",
        )
