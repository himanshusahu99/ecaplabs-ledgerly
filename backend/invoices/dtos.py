"""Data transfer objects for invoice extraction."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class LLMTurnDTO:
    """One model response, as plain content-block dicts."""

    stop_reason: str
    content: list


@dataclass(frozen=True)
class ExtractedLineItemDTO:
    """One line on an invoice."""

    description: str
    amount: Decimal

    def to_json(self):
        """Serialises for the line_items JSON column."""
        return {"description": self.description, "amount": str(self.amount)}


@dataclass(frozen=True)
class InvoiceExtractionDTO:
    """The normalised fields the agent submitted."""

    vendor_name: str
    invoice_number: str
    currency: str
    total_amount: Decimal
    due_date: date | None
    line_items: list = field(default_factory=list)


@dataclass
class AgentRunDTO:
    """What one agent run produced."""

    submission: dict | None = None
    payee: object | None = None
    transcript: list = field(default_factory=list)
