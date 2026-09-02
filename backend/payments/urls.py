"""Dashboard payment routes."""

from django.urls import path
from payments.views.payment_list_view import PaymentListView
from payments.views.payment_summary_view import PaymentSummaryView

urlpatterns = [
    path(
        "businesses/<str:business_id>/payments/",
        PaymentListView.as_view(),
        name="payment-list",
    ),
    path(
        "businesses/<str:business_id>/payments/summary/",
        PaymentSummaryView.as_view(),
        name="payment-summary",
    ),
]
