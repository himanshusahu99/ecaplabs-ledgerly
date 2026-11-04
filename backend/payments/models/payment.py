"""Payment model."""

from core.models import Business
from django.db import models
from payments.choices import PaymentStatus
from payments.constants import DEFAULT_CURRENCY
from payments.models.payee import Payee


class Payment(models.Model):
    """A payment mirrored from Paystream."""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="payments"
    )
    payee = models.ForeignKey(Payee, on_delete=models.PROTECT, related_name="payments")
    processor_payment_id = models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = models.CharField(
        max_length=16, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    memo = models.CharField(max_length=255, blank=True)
    scheduled_for = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.processor_payment_id} {self.amount} {self.status}"
