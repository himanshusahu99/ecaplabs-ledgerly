"""Applies Paystream events to local payments."""

import logging
from decimal import Decimal

from core.abstractions.webhook_processor_interface import WebhookProcessorInterface
from core.repositories.business_repository import BusinessRepository
from payments.choices import PaystreamEventType
from payments.constants import STATUS_BY_EVENT_TYPE
from payments.dtos import PaystreamEventDTO
from payments.repositories.payee_repository import PayeeRepository
from payments.repositories.payment_repository import PaymentRepository
from payments.tasks import send_payment_notice_task

logger = logging.getLogger(__name__)

REQUIRED_KEYS = ("id", "type", "data")


class PaystreamWebhookProcessor(WebhookProcessorInterface):
    """Mirrors Paystream payment events into Payment rows."""

    def __init__(self):
        self.business_repository = BusinessRepository()
        self.payee_repository = PayeeRepository()
        self.payment_repository = PaymentRepository()

    def validate_payload(self, *, payload):
        missing = [key for key in REQUIRED_KEYS if key not in payload]
        if missing:
            raise ValueError(f"paystream payload missing {missing}")

    def process(self, *, payload):
        event = PaystreamEventDTO.from_payload(payload=payload)
        if event.event_type == PaystreamEventType.PAYMENT_CREATED:
            self._on_payment_created(event=event)
        elif event.event_type in STATUS_BY_EVENT_TYPE:
            self._on_payment_status_changed(event=event)
        else:
            logger.info("ignoring event type=%s", event.event_type)

    def _on_payment_created(self, *, event):
        """Records a payment the business scheduled in Paystream."""
        data = event.data
        business = self.business_repository.get_by_business_id(
            business_id=data["business_id"]
        )
        payee = self.payee_repository.get_for_business(
            business=business, payee_id=data["payee_id"]
        )
        payment = self.payment_repository.create(
            business=business,
            payee=payee,
            processor_payment_id=data["id"],
            amount=Decimal(data["amount"]),
            currency=data["currency"],
            memo=data.get("memo", ""),
            scheduled_for=data.get("scheduled_for"),
        )
        logger.info(
            "payment created pk=%s processor_payment_id=%s",
            payment.pk,
            payment.processor_payment_id,
        )
        send_payment_notice_task.delay(payment_id=payment.pk)

    def _on_payment_status_changed(self, *, event):
        """Moves a payment to the status Paystream reports."""
        payment = self.payment_repository.get_by_processor_payment_id(
            processor_payment_id=event.data["id"]
        )
        if payment is None:
            logger.warning("status event for unknown payment=%s", event.data["id"])
            return
        status = STATUS_BY_EVENT_TYPE[event.event_type]
        self.payment_repository.update_status(payment=payment, status=status)
        logger.info("payment pk=%s now %s", payment.pk, status)
