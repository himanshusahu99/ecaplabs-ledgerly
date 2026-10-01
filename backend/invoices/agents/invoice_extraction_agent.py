"""Tool-using agent that reads one invoice."""

import json
import logging

from core.abstractions.base_service import BaseService
from invoices.constants import AGENT_MAX_TURNS, INVOICE_AGENT_ACTOR, SUBMIT_TOOL_NAME
from invoices.dtos import AgentRunDTO
from invoices.exceptions import ExtractionError
from invoices.prompts.invoice_extraction_prompt import (
    SYSTEM_PROMPT,
    TOOLS,
    build_user_message,
)
from payments.repositories.payee_repository import PayeeRepository

logger = logging.getLogger(__name__)


class InvoiceExtractionAgent(BaseService):
    """Runs the Claude tool loop until the model submits an extraction."""

    def __init__(self, *, business, llm_client, **kwargs):
        super().__init__(**kwargs)
        self.business = business
        self.llm_client = llm_client
        self.payee_repository = PayeeRepository()
        self.run_state = AgentRunDTO()
        self.tool_handlers = {
            "find_payee": self._find_payee,
            "create_payee": self._create_payee,
            "update_payee_remittance": self._update_payee_remittance,
        }

    def run(self, *, document_text):
        """Returns an AgentRunDTO with the submission, resolved payee and transcript."""
        messages = [
            {
                "role": "user",
                "content": build_user_message(
                    business_name=self.business.name, document_text=document_text
                ),
            }
        ]
        for _ in range(AGENT_MAX_TURNS):
            turn = self.llm_client.create_message(
                system=SYSTEM_PROMPT, messages=messages, tools=TOOLS
            )
            messages.append({"role": "assistant", "content": turn.content})
            self.run_state.transcript.append(
                {
                    "role": "assistant",
                    "stop_reason": turn.stop_reason,
                    "content": turn.content,
                }
            )
            if turn.stop_reason == "refusal":
                raise ExtractionError("model declined to process this document")
            tool_uses = [
                block for block in turn.content if block.get("type") == "tool_use"
            ]
            submission = next(
                (block for block in tool_uses if block["name"] == SUBMIT_TOOL_NAME),
                None,
            )
            if submission is not None:
                self.run_state.submission = submission["input"]
                return self.run_state
            if turn.stop_reason != "tool_use":
                raise ExtractionError(
                    f"agent stopped without submitting ({turn.stop_reason})"
                )
            tool_results = [self._run_tool(block=block) for block in tool_uses]
            messages.append({"role": "user", "content": tool_results})
            self.run_state.transcript.append(
                {"role": "tool_results", "content": tool_results}
            )
        raise ExtractionError(f"agent did not submit within {AGENT_MAX_TURNS} turns")

    def _run_tool(self, *, block):
        """Executes one tool_use block and returns its tool_result."""
        handler = self.tool_handlers.get(block["name"])
        if handler is None:
            return self._tool_result(
                block=block, payload={"error": "unknown tool"}, is_error=True
            )
        logger.info("invoice agent tool=%s input=%s", block["name"], block["input"])
        return self._tool_result(block=block, payload=handler(**block["input"]))

    @staticmethod
    def _tool_result(*, block, payload, is_error=False):
        """Formats a tool_result content block."""
        return {
            "type": "tool_result",
            "tool_use_id": block["id"],
            "content": json.dumps(payload),
            "is_error": is_error,
        }

    def _find_payee(self, *, name):
        """Tool: returns payees whose name matches."""
        matches = self.payee_repository.find_by_name(business=self.business, name=name)
        if matches:
            self.run_state.payee = matches[0]
        return {
            "matches": [{"payee_id": payee.pk, "name": payee.name} for payee in matches]
        }

    def _create_payee(self, *, name, email):
        """Tool: creates a payee and makes it the invoice's payee."""
        payee = self.payee_repository.create(
            business=self.business, name=name, email=email or ""
        )
        self.run_state.payee = payee
        return {"payee_id": payee.pk, "name": payee.name}

    def _update_payee_remittance(
        self, *, payee_id, routing_number, account_number, reason
    ):
        """Tool: points a payee's payments at new bank details."""
        payee = self.payee_repository.get_for_business(
            business=self.business, payee_id=payee_id
        )
        if payee is None:
            return {"error": f"no payee {payee_id} for this business"}
        self.payee_repository.update_remittance(
            payee=payee,
            routing_number=routing_number,
            account_number=account_number,
            updated_by=INVOICE_AGENT_ACTOR,
        )
        logger.info(
            "invoice agent updated remittance payee=%s reason=%s", payee.pk, reason
        )
        return {"updated": True, "payee_id": payee.pk}
