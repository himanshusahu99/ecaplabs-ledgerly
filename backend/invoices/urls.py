"""Invoice routes."""

from django.urls import path
from invoices.views.invoice_list_view import InvoiceListView
from invoices.views.invoice_review_views import InvoiceApproveView, InvoiceRejectView

urlpatterns = [
    path(
        "businesses/<str:business_id>/invoices/",
        InvoiceListView.as_view(),
        name="invoice-list",
    ),
    path(
        "businesses/<str:business_id>/invoices/<int:invoice_id>/approve/",
        InvoiceApproveView.as_view(),
        name="invoice-approve",
    ),
    path(
        "businesses/<str:business_id>/invoices/<int:invoice_id>/reject/",
        InvoiceRejectView.as_view(),
        name="invoice-reject",
    ),
]
