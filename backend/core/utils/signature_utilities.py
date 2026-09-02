"""HMAC signing helpers for webhooks."""

import hashlib
import hmac

from core.abstractions.base_utility import BaseUtility


class SignatureUtilities(BaseUtility):
    """SHA-256 HMAC over a raw request body."""

    @staticmethod
    def sign(*, secret, body):
        """Returns the hex signature for body."""
        return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    @staticmethod
    def is_valid(*, secret, body, signature):
        """Constant-time check of a provided signature."""
        expected = SignatureUtilities.sign(secret=secret, body=body)
        return hmac.compare_digest(expected, signature or "")
