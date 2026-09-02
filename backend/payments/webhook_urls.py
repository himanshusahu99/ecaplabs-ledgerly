"""Inbound webhook routes."""

from django.urls import path
from payments.views.paystream_webhook_view import PaystreamWebhookView

urlpatterns = [
    path("paystream/", PaystreamWebhookView.as_view(), name="paystream-webhook"),
]
