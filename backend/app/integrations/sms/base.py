"""SMSProvider protocol -- keeps Twilio swappable."""

from typing import Protocol


class SMSProvider(Protocol):
    async def send(self, *, from_number: str, to_number: str, body: str) -> str:
        """Send a message; returns the provider message id."""
        ...
