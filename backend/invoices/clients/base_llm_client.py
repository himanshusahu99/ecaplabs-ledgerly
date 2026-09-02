"""Contract for LLM clients used by agents."""

from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Sends one Messages API request and returns an LLMTurnDTO."""

    @abstractmethod
    def create_message(self, *, system, messages, tools):
        """Returns the next assistant turn."""
