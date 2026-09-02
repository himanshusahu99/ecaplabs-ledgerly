"""Test helpers for invoices."""

from invoices.clients.base_llm_client import BaseLLMClient
from invoices.dtos import LLMTurnDTO


class ScriptedLLMClient(BaseLLMClient):
    """Returns pre-written turns and records what it was sent."""

    def __init__(self, *, turns):
        self.turns = list(turns)
        self.requests = []

    def create_message(self, *, system, messages, tools):
        self.requests.append(list(messages))
        return self.turns.pop(0)


class TurnFactory:
    """Builds assistant turns in Messages API shape."""

    @staticmethod
    def tool_call(*, name, tool_input, tool_use_id="toolu_1"):
        """A turn that calls one tool."""
        return LLMTurnDTO(
            stop_reason="tool_use",
            content=[
                {
                    "type": "tool_use",
                    "id": tool_use_id,
                    "name": name,
                    "input": tool_input,
                }
            ],
        )

    @staticmethod
    def submission(*, total="1,250.00", line_items=None, currency="USD"):
        """A turn that submits an extraction."""
        return TurnFactory.tool_call(
            name="submit_extraction",
            tool_use_id="toolu_submit",
            tool_input={
                "vendor_name": "Vendor",
                "invoice_number": "INV-1",
                "currency": currency,
                "total": total,
                "due_date": "2026-11-01",
                "line_items": (
                    line_items
                    if line_items is not None
                    else [{"description": "Widgets", "amount": total}]
                ),
            },
        )
