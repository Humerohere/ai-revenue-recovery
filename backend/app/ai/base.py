"""Provider-agnostic LLM interface. No vendor SDK may be imported outside app/ai/."""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Message:
    role: str  # "user" | "assistant"
    content: str


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class LLMResponse:
    text: str | None
    tool_calls: list[ToolCall]
    model: str


class LLMProvider(Protocol):
    async def complete(
        self,
        *,
        system: str,
        messages: list[Message],
        tools: list[dict[str, Any]],
    ) -> LLMResponse: ...
