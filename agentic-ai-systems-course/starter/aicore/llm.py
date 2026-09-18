"""Provider-agnostic LLM access.

Two rules this module exists to enforce:

1. Nothing outside this file imports a provider SDK. Swapping vendors, adding a
   fallback pool, routing by tier, or counting cost must all be one-file changes.
2. Every exercise in the course runs offline. `FakeLLM` is scripted and
   deterministic, so tests assert on behaviour rather than on model output.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


# --------------------------------------------------------------------------
# Wire types
# --------------------------------------------------------------------------
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass
class Message:
    role: str                       # system | user | assistant | tool
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str = ""

    def to_dict(self) -> dict:
        out: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.tool_calls:
            out["tool_calls"] = [
                {"id": c.id, "name": c.name, "arguments": c.arguments} for c in self.tool_calls
            ]
        if self.tool_call_id:
            out["tool_call_id"] = self.tool_call_id
        return out


@dataclass
class LLMResponse:
    text: str
    model: str = "fake"
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"

    @property
    def cost_usd(self) -> float:
        price = PRICES.get(self.model, PRICES["fake"])
        billable_in = max(self.input_tokens - self.cached_tokens, 0)
        return (
            billable_in * price["in"]
            + self.cached_tokens * price["cached"]
            + self.output_tokens * price["out"]
        ) / 1_000_000


# USD per 1M tokens. Keep prices in config, never scattered through the code -
# they change, and a hard-coded price makes every historical cost report wrong.
PRICES: dict[str, dict[str, float]] = {
    "fake": {"in": 0.0, "out": 0.0, "cached": 0.0},
    "small": {"in": 0.25, "out": 1.25, "cached": 0.03},
    "default": {"in": 3.00, "out": 15.00, "cached": 0.30},
    "strong": {"in": 15.00, "out": 75.00, "cached": 1.50},
}


class LLM(Protocol):
    name: str

    def complete(
        self,
        messages: list[Message],
        *,
        tools: list[dict] | None = None,
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> LLMResponse: ...


# --------------------------------------------------------------------------
# Token estimation
# --------------------------------------------------------------------------
_CODE_CHARS = set("{}()[];=_<>")


def estimate_tokens(text: str) -> int:
    """Calibrated character heuristic.

    Dense code tokenises at roughly 3.1 chars/token and English prose at 4.2.
    The usual advice of 4.0 underestimates a C header by 20-30%, always in the
    direction that flatters your cost model. Replace with `tiktoken` when you
    have it; keep this as the offline fallback.
    """
    if not text:
        return 0
    density = sum(text.count(ch) for ch in _CODE_CHARS) / len(text)
    chars_per_token = 3.1 if density > 0.02 else 4.2
    return max(1, int(len(text) / chars_per_token))


# --------------------------------------------------------------------------
# Offline scripted model
# --------------------------------------------------------------------------
@dataclass
class ScriptRule:
    """Fires when `pattern` matches the last user/tool message."""

    pattern: re.Pattern
    respond: Callable[[re.Match, list[Message]], LLMResponse]


class FakeLLM:
    """Deterministic, offline, and inspectable.

    It records every call, so tests can assert on *how* a component used the
    model (call count, prompt prefix stability, tool arguments) rather than only
    on what came back. That is usually the more valuable assertion.
    """

    name = "fake"

    def __init__(self, rules: list[ScriptRule] | None = None, default: str = "NOT_IN_CONTEXT: no scripted response") -> None:
        self.rules = rules or []
        self.default = default
        self.calls: list[dict] = []

    def complete(
        self,
        messages: list[Message],
        *,
        tools: list[dict] | None = None,
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        probe = next((m.content for m in reversed(messages) if m.role in ("user", "tool")), "")
        response = LLMResponse(text=self.default, model=self.name)
        for rule in self.rules:
            match = rule.pattern.search(probe)
            if match:
                response = rule.respond(match, messages)
                break

        response.input_tokens = sum(estimate_tokens(m.content) for m in messages)
        response.output_tokens = estimate_tokens(response.text)
        self.calls.append(
            {
                "messages": len(messages),
                "tools": len(tools or []),
                "temperature": temperature,
                "probe": probe[:200],
                "response": response.text[:200],
                "input_tokens": response.input_tokens,
            }
        )
        return response

    # Convenience for building scripts in tests.
    def on(self, pattern: str, text: str = "", tool: tuple[str, dict] | None = None) -> "FakeLLM":
        def respond(_match: re.Match, _messages: list[Message]) -> LLMResponse:
            calls = [ToolCall(id=f"call_{len(self.calls)}", name=tool[0], arguments=tool[1])] if tool else []
            return LLMResponse(text=text, model=self.name, tool_calls=calls)

        self.rules.append(ScriptRule(re.compile(pattern, re.IGNORECASE), respond))
        return self


# --------------------------------------------------------------------------
# Provider adapters (thin; add the SDK import inside the adapter only)
# --------------------------------------------------------------------------
class OpenAIChat:
    def __init__(self, model: str = "gpt-4.1-mini", tier: str = "default") -> None:
        from openai import OpenAI  # imported lazily so the offline path needs no SDK

        self._client = OpenAI()
        self._model = model
        self.name = tier

    def complete(self, messages, *, tools=None, temperature=0.0, max_tokens=2048) -> LLMResponse:
        raw = self._client.chat.completions.create(
            model=self._model,
            messages=[m.to_dict() for m in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            **({"tools": tools} if tools else {}),
        )
        choice = raw.choices[0]
        usage = raw.usage
        return LLMResponse(
            text=choice.message.content or "",
            model=self.name,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            cached_tokens=getattr(getattr(usage, "prompt_tokens_details", None), "cached_tokens", 0) or 0,
            finish_reason=choice.finish_reason,
        )


_DEFAULT: LLM | None = None


def get_llm() -> LLM:
    """Factory. Offline unless BENCH_AI_PROVIDER says otherwise."""
    global _DEFAULT
    if _DEFAULT is not None:
        return _DEFAULT
    provider = os.environ.get("BENCH_AI_PROVIDER", "fake")
    if provider == "openai":
        _DEFAULT = OpenAIChat(model=os.environ.get("BENCH_AI_MODEL", "gpt-4.1-mini"))
    else:
        _DEFAULT = FakeLLM()
    return _DEFAULT


def set_llm(llm: LLM) -> None:
    """Used by tests and by the model-routing table (Module 35)."""
    global _DEFAULT
    _DEFAULT = llm
