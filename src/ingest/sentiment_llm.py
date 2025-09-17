"""Local LLM wrapper for sentiment scoring."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Protocol

from structlog import get_logger

LOGGER = get_logger(__name__)

try:
    from llama_cpp import Llama
except Exception:  # pragma: no cover - optional dependency guard
    Llama = None  # type: ignore[assignment]


class _LlamaProtocol(Protocol):
    def __call__(self, *, prompt: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        ...


@dataclass(slots=True)
class SentimentResult:
    """Structured sentiment response."""

    sentiment: float
    volatility_flag: bool
    tokens_used: int


class SentimentModel:
    """Thin wrapper around llama-cpp for deterministic scoring."""

    def __init__(self, model_path: Path, max_tokens: int = 256, temperature: float = 0.2) -> None:
        self._max_tokens = max_tokens
        self._temperature = temperature
        if Llama is None:
            LOGGER.warning("llama_cpp_missing", msg="Sentiment model running in mock mode")
            self._llm: _LlamaProtocol | None = None
        else:
            if not model_path.exists():
                raise FileNotFoundError(model_path)
            self._llm = Llama(model_path=str(model_path), n_ctx=max_tokens * 2, n_threads=4)

    def score(self, text: str, prompt: str | None = None) -> SentimentResult:
        """Return sentiment score for *text* using optional *prompt*."""

        template = prompt or "Score sentiment between -1 and 1 and flag volatility risk."""
        if self._llm is None:
            # Fallback heuristic when model is unavailable.
            sentiment = float(len(text) % 10) / 5 - 1
            return SentimentResult(sentiment=sentiment, volatility_flag=abs(sentiment) > 0.6, tokens_used=0)
        output: Dict[str, Any] = self._llm(
            prompt=f"{template}\n\n{text}",
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )
        LOGGER.debug("llm_sentiment_output", output=output)
        sentiment_str = output.get("choices", [{}])[0].get("text", "0")
        try:
            sentiment = float(sentiment_str)
        except ValueError:
            sentiment = 0.0
        volatility_flag = abs(sentiment) > 0.6
        tokens_used = int(output.get("usage", {}).get("total_tokens", 0))
        return SentimentResult(sentiment=sentiment, volatility_flag=volatility_flag, tokens_used=tokens_used)


__all__ = ["SentimentModel", "SentimentResult"]
