"""Base class for outbound HTTP clients."""

import logging
import time

import requests
from core.abstractions.base_service import BaseService
from core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class BaseAPIClient(BaseService):
    """Wraps requests with timing logs and a single error type."""

    service_name = "external"

    def __init__(self, *, base_url, timeout_seconds, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @property
    def is_configured(self):
        """True when a base URL is set for this environment."""
        return bool(self.base_url)

    def post(self, *, path, payload):
        """Sends a JSON POST and returns the decoded body."""
        url = f"{self.base_url}{path}"
        started = time.perf_counter()
        try:
            response = requests.post(url, json=payload, timeout=self.timeout_seconds)
        except requests.RequestException as error:
            raise ExternalServiceError(
                service=self.service_name, message=str(error)
            ) from error
        finally:
            logger.info(
                "%s POST %s took %.2fs",
                self.service_name,
                path,
                time.perf_counter() - started,
            )
        if response.status_code >= 400:
            raise ExternalServiceError(
                service=self.service_name,
                message=response.text[:500],
                status_code=response.status_code,
            )
        return response.json() if response.content else {}
