"""Payee model."""

from core.models import Business
from django.db import models


class Payee(models.Model):
    """A vendor a business pays, with where to send the money."""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="payees"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    remittance_routing_number = models.CharField(max_length=9, blank=True)
    remittance_account_number = models.CharField(max_length=34, blank=True)
    remittance_updated_at = models.DateTimeField(null=True, blank=True)
    remittance_updated_by = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
