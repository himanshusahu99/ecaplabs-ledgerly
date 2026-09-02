"""Live Claude client."""

import anthropic
from django.conf import settings
from invoices.clients.base_llm_client import BaseLLMClient
from invoices.constants import AGENT_MAX_TOKENS
from invoices.dtos import LLMTurnDTO
from invoices.exceptions import ExtractionError

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class AnthropicLLMClient(BaseLLMClient):
    """Calls the Claude Messages API with refusal fallbacks enabled."""

    def __init__(self):
        self.client = anthropic.Anthropic()

    def create_message(self, *, system, messages, tools):
        try:
            response = self.client.beta.messages.create(
                model=settings.INVOICE_AGENT_MODEL,
                max_tokens=AGENT_MAX_TOKENS,
                system=system,
                messages=messages,
                tools=tools,
                betas=[FALLBACK_BETA],
                fallbacks="default",
            )
        except anthropic.APIError as error:
            raise ExtractionError(f"claude request failed: {error}") from error
        return LLMTurnDTO(
            stop_reason=response.stop_reason,
            content=[block.to_dict() for block in response.content],
        )
