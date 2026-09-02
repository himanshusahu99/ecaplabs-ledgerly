"""Exceptions raised while extracting invoices."""


class ExtractionError(Exception):
    """The agent could not produce a usable extraction."""


class LLMRecordingMissingError(ExtractionError):
    """No recorded LLM response exists for this document."""
