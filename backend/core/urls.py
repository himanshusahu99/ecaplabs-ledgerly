"""Core routes."""

from core.views.me_view import MeView
from django.urls import path

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
]
