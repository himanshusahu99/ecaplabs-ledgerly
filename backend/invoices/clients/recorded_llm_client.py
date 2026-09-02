"""Replays recorded Claude responses so the app runs without an API key."""

import json

from django.conf import settings
from invoices.clients.base_llm_client import BaseLLMClient
from invoices.dtos import LLMTurnDTO
from invoices.exceptions import LLMRecordingMissingError


class RecordedLLMClient(BaseLLMClient):
    """Returns the recorded turns for one document, in order."""

    def __init__(self, *, document_sha256):
        path = settings.LLM_RECORDINGS_DIR / f"{document_sha256}.json"
        if not path.exists():
            raise LLMRecordingMissingError(
                f"no recording for document {document_sha256[:12]}; "
                "set ANTHROPIC_API_KEY to run the agent live"
            )
        self.turns = json.loads(path.read_text())["turns"]
        self.position = 0

    def create_message(self, *, system, messages, tools):
        if self.position >= len(self.turns):
            raise LLMRecordingMissingError("recording ran out of turns")
        turn = self.turns[self.position]
        self.position += 1
        return LLMTurnDTO(stop_reason=turn["stop_reason"], content=turn["content"])
