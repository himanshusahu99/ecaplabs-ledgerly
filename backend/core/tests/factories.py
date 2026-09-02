"""Test data builders shared by every app."""

from core.models import Business, Membership
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class CoreFactory:
    """Creates businesses, members and authenticated clients."""

    @staticmethod
    def business(*, business_id="ECL-9001", name="Testco"):
        """Creates a business."""
        return Business.objects.create(business_id=business_id, name=name)

    @staticmethod
    def member(*, business, email="member@testco.test"):
        """Creates a user who belongs to business."""
        user = get_user_model().objects.create_user(username=email, email=email)
        Membership.objects.create(user=user, business=business)
        return user

    @staticmethod
    def api_client(*, user):
        """Returns an APIClient authenticated as user."""
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=user).key}"
        )
        return client
