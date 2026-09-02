"""Tests for MoneyUtilities."""

from decimal import Decimal

from core.utils.money_utilities import MoneyUtilities
from django.test import SimpleTestCase


class ParseAmountTests(SimpleTestCase):
    """parse_amount handles the formats our sources send."""

    def test_thousands_separator(self):
        self.assertEqual(
            MoneyUtilities.parse_amount(value="1,250.00"), Decimal("1250.00")
        )

    def test_dollar_sign(self):
        self.assertEqual(MoneyUtilities.parse_amount(value="$89.5"), Decimal("89.50"))

    def test_number(self):
        self.assertEqual(MoneyUtilities.parse_amount(value=42), Decimal("42.00"))

    def test_none(self):
        self.assertIsNone(MoneyUtilities.parse_amount(value=None))

    def test_garbage(self):
        with self.assertRaises(ValueError):
            MoneyUtilities.parse_amount(value="twelve")
