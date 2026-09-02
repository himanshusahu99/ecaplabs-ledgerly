"""Money parsing and arithmetic helpers."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from core.abstractions.base_utility import BaseUtility

CENT = Decimal("0.01")


class MoneyUtilities(BaseUtility):
    """Turns human-formatted amounts into Decimals."""

    @staticmethod
    def parse_amount(*, value):
        """Parses '1,250.00', '$1250', or 1250 into Decimal('1250.00')."""
        if value is None:
            return None
        cleaned = str(value).strip().replace(",", "").replace("$", "").replace(" ", "")
        try:
            return Decimal(cleaned).quantize(CENT, rounding=ROUND_HALF_UP)
        except InvalidOperation as error:
            raise ValueError(f"not an amount: {value!r}") from error

    @staticmethod
    def to_cents(*, value):
        """Rounds a Decimal or None to two places, treating None as zero."""
        return Decimal(value or 0).quantize(CENT, rounding=ROUND_HALF_UP)

    @staticmethod
    def sum_amounts(*, amounts):
        """Adds Decimals, treating an empty list as zero."""
        return sum(amounts, Decimal("0.00"))
