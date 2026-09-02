"""Businesses and the users who can act for them."""

from django.conf import settings
from django.db import models


class Business(models.Model):
    """A customer business on the platform."""

    business_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Grants a user access to a business."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="memberships"
    )

    class Meta:
        unique_together = [("user", "business")]
