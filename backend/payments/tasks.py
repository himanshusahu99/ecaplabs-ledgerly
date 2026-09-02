"""Background tasks for payments."""

from celery import shared_task
from payments.models import Payment
from payments.services.notification_service import NotificationService


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_payment_notice_task(payment_id):
    """Sends the payee notice outside the request cycle."""
    payment = Payment.objects.select_related("payee", "business").get(pk=payment_id)
    NotificationService().send_payment_notice(payment=payment)
