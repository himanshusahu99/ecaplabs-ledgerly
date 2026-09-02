"""Root URL configuration."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("core.urls")),
    path("api/", include("payments.urls")),
    path("api/", include("invoices.urls")),
    path("webhooks/", include("payments.webhook_urls")),
]
