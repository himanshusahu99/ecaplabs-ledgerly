"""Contract every webhook processor implements."""

from abc import ABC, abstractmethod


class WebhookProcessorInterface(ABC):
    """Applies one provider event to local state."""

    def run(self, *, payload):
        """Validates then processes a payload."""
        self.validate_payload(payload=payload)
        self.process(payload=payload)

    @abstractmethod
    def validate_payload(self, *, payload):
        """Raises ValueError when the payload is malformed."""

    @abstractmethod
    def process(self, *, payload):
        """Applies the event."""
