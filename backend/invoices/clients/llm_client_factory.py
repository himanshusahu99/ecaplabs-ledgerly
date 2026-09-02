"""Chooses a live or recorded LLM client."""

from django.conf import settings
from invoices.clients.anthropic_llm_client import AnthropicLLMClient
from invoices.clients.recorded_llm_client import RecordedLLMClient


class LLMClientFactory:
    """Live Claude when a key is set, recordings otherwise."""

    @staticmethod
    def build(*, document_sha256):
        """Returns the client for one document."""
        if settings.INVOICE_AGENT_LIVE:
            return AnthropicLLMClient()
        return RecordedLLMClient(document_sha256=document_sha256)
