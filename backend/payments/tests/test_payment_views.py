"""Tests for the payments dashboard endpoints."""

from core.tests.factories import CoreFactory
from django.test import TestCase
from payments.choices import PaymentStatus
from payments.tests.factories import PaymentFactory


class PaymentViewTests(TestCase):
    """List and summary endpoints."""

    def setUp(self):
        self.business = CoreFactory.business()
        self.payee = PaymentFactory.payee(business=self.business)
        self.client = CoreFactory.api_client(
            user=CoreFactory.member(business=self.business)
        )

    def test_summary_counts_pending_and_processing(self):
        PaymentFactory.payment(
            business=self.business,
            payee=self.payee,
            processor_payment_id="pp_1",
            amount="10.00",
        )
        PaymentFactory.payment(
            business=self.business,
            payee=self.payee,
            processor_payment_id="pp_2",
            amount="5.50",
            status=PaymentStatus.PROCESSING,
        )
        PaymentFactory.payment(
            business=self.business,
            payee=self.payee,
            processor_payment_id="pp_3",
            amount="99.00",
            status=PaymentStatus.SETTLED,
        )
        response = self.client.get("/api/businesses/ECL-9001/payments/summary/")
        self.assertEqual(response.json()["outstanding"], "15.50")
        self.assertEqual(response.json()["settled_this_month"], "99.00")

    def test_list_returns_payee_name(self):
        PaymentFactory.payment(business=self.business, payee=self.payee)
        response = self.client.get("/api/businesses/ECL-9001/payments/")
        self.assertEqual(response.json()[0]["payee_name"], "Vendor")

    def test_non_member_is_forbidden(self):
        CoreFactory.business(business_id="ECL-9002", name="Other")
        response = self.client.get("/api/businesses/ECL-9002/payments/")
        self.assertEqual(response.status_code, 403)
