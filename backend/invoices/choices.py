"""Enumerations for invoices."""

from django.db import models


class InvoiceStatus(models.TextChoices):
    """Lifecycle of an uploaded invoice."""

    UPLOADED = "uploaded"
    EXTRACTING = "extracting"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"
