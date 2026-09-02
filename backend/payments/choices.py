"""Enumerations for payments."""

from django.db import models


class PaymentStatus(models.TextChoices):
    """Lifecycle of a payment as Paystream reports it."""

    PENDING = "pending"
    PROCESSING = "processing"
    SETTLED = "settled"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaystreamEventType(models.TextChoices):
    """Webhook event types Paystream sends."""

    PAYMENT_CREATED = "payment.created"
    PAYMENT_PROCESSING = "payment.processing"
    PAYMENT_SETTLED = "payment.settled"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_CANCELLED = "payment.cancelled"
