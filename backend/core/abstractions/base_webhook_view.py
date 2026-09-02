"""Base class for inbound webhook endpoints."""

import json
import logging
from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class BaseWebhookView(APIView, ABC):
    """Verifies, decodes and hands a webhook payload to its processor."""

    authentication_classes = []
    permission_classes = [AllowAny]
    provider = None

    @abstractmethod
    def verify_signature(self, *, request):
        """Returns True when the request is signed by the provider."""

    @abstractmethod
    def build_processor(self):
        """Returns the WebhookProcessorInterface for this provider."""

    def post(self, request):
        if not self.verify_signature(request=request):
            logger.warning("%s webhook rejected: bad signature", self.provider)
            return Response(
                {"detail": "Invalid signature."}, status=status.HTTP_401_UNAUTHORIZED
            )
        payload = json.loads(request.body)
        logger.info(
            "webhook received provider=%s id=%s type=%s",
            self.provider,
            payload.get("id"),
            payload.get("type"),
        )
        self.build_processor().run(payload=payload)
        return Response({"received": True})
