"""Data transfer objects for payments."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PaystreamEventDTO:
    """One Paystream webhook event."""

    event_id: str
    event_type: str
    created: str
    data: dict

    @classmethod
    def from_payload(cls, *, payload):
        """Builds the DTO from a decoded webhook body."""
        return cls(
            event_id=payload["id"],
            event_type=payload["type"],
            created=payload.get("created", ""),
            data=payload["data"],
        )


@dataclass(frozen=True)
class PaymentSummaryDTO:
    """Totals shown on the dashboard cards."""

    outstanding: Decimal
    settled_this_month: Decimal
    currency: str

    def to_response(self):
        """Serialises amounts as strings to keep precision."""
        return {
            "outstanding": str(self.outstanding),
            "settled_this_month": str(self.settled_this_month),
            "currency": self.currency,
        }
