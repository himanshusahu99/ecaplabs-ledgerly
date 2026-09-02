"""Tests for the me endpoint."""

from core.tests.factories import CoreFactory
from django.test import TestCase


class MeViewTests(TestCase):
    """GET /api/me/."""

    def test_lists_member_businesses_only(self):
        business = CoreFactory.business()
        CoreFactory.business(business_id="ECL-9002", name="Other")
        client = CoreFactory.api_client(user=CoreFactory.member(business=business))
        response = client.get("/api/me/")
        self.assertEqual(
            [item["business_id"] for item in response.json()["businesses"]],
            ["ECL-9001"],
        )
