"""Constants for payments."""

from payments.choices import PaymentStatus, PaystreamEventType

OUTSTANDING_STATUSES = [PaymentStatus.PENDING, PaymentStatus.PROCESSING]
PAYSTREAM_SIGNATURE_HEADER = "X-Paystream-Signature"
PAYSTREAM_PROVIDER = "paystream"
NOTIFY_TEMPLATE_PAYMENT_ON_THE_WAY = "payment_on_the_way"
DEFAULT_CURRENCY = "USD"

STATUS_BY_EVENT_TYPE = {
    PaystreamEventType.PAYMENT_PROCESSING: PaymentStatus.PROCESSING,
    PaystreamEventType.PAYMENT_SETTLED: PaymentStatus.SETTLED,
    PaystreamEventType.PAYMENT_FAILED: PaymentStatus.FAILED,
    PaystreamEventType.PAYMENT_CANCELLED: PaymentStatus.CANCELLED,
}
