"""API shapes for payments."""

from payments.models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    """A payment as the dashboard shows it."""

    payee_name = serializers.CharField(source="payee.name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "processor_payment_id",
            "payee_name",
            "amount",
            "currency",
            "status",
            "memo",
            "scheduled_for",
            "created_at",
            "updated_at",
        ]
