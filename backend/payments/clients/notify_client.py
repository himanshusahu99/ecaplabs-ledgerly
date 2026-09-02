"""Client for the internal notification service."""

from core.abstractions.base_api_client import BaseAPIClient
from django.conf import settings


class NotifyClient(BaseAPIClient):
    """Sends templated emails through notify-svc."""

    service_name = "notify-svc"

    def __init__(self, **kwargs):
        super().__init__(
            base_url=settings.NOTIFY_URL,
            timeout_seconds=settings.NOTIFY_TIMEOUT_SECONDS,
            **kwargs,
        )

    def send(self, *, template, to, context):
        """Queues one email in notify-svc."""
        return self.post(
            path="/v1/send",
            payload={"template": template, "to": to, "context": context},
        )
