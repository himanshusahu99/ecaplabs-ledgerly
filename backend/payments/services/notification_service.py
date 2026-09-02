"""Payee notifications."""

import logging

from core.abstractions.base_service import BaseService
from payments.clients.notify_client import NotifyClient
from payments.constants import NOTIFY_TEMPLATE_PAYMENT_ON_THE_WAY

logger = logging.getLogger(__name__)


class NotificationService(BaseService):
    """Tells payees about payments headed their way."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notify_client = NotifyClient()

    def send_payment_notice(self, *, payment):
        """Emails the payee that a payment is on the way."""
        if not self.notify_client.is_configured:
            logger.info(
                "notify disabled, skipping payment=%s", payment.processor_payment_id
            )
            return
        self.notify_client.send(
            template=NOTIFY_TEMPLATE_PAYMENT_ON_THE_WAY,
            to=payment.payee.email,
            context={
                "business": payment.business.name,
                "amount": str(payment.amount),
                "currency": payment.currency,
                "scheduled_for": (
                    payment.scheduled_for.isoformat() if payment.scheduled_for else None
                ),
            },
        )
