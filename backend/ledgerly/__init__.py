"""Ledgerly project package."""

from ledgerly.celery import app as celery_app

__all__ = ["celery_app"]
