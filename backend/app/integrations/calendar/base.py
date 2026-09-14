"""CalendarProvider protocol -- free/busy lookup and event creation."""

from datetime import datetime
from typing import Protocol


class CalendarProvider(Protocol):
    async def busy_blocks(
        self, *, calendar_id: str, start: datetime, end: datetime
    ) -> list[tuple[datetime, datetime]]: ...

    async def create_event(
        self, *, calendar_id: str, start: datetime, end: datetime, summary: str, description: str
    ) -> str: ...
