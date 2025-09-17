"""Minimal structlog stub for offline environments."""

from __future__ import annotations

import logging
from typing import Any, Callable


class _LoggerAdapter:
    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)

    def info(self, event: str, **kwargs: Any) -> None:
        self._logger.info("%s %s", event, kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self._logger.warning("%s %s", event, kwargs)

    def debug(self, event: str, **kwargs: Any) -> None:
        self._logger.debug("%s %s", event, kwargs)


def get_logger(name: str) -> _LoggerAdapter:
    return _LoggerAdapter(name)


def configure(**kwargs: Any) -> None:  # pragma: no cover - compatibility stub
    logging.basicConfig(level=logging.INFO)


class processors:  # pragma: no cover - compatibility stub
    @staticmethod
    def TimeStamper(fmt: str = "iso") -> Callable[..., Any]:
        def _processor(*args: Any, **kwargs: Any) -> Any:
            return args, kwargs

        return _processor

    @staticmethod
    def add_log_level(*args: Any, **kwargs: Any) -> Any:
        return args, kwargs

    @staticmethod
    def StackInfoRenderer(*args: Any, **kwargs: Any) -> Any:
        return args, kwargs

    @staticmethod
    def format_exc_info(*args: Any, **kwargs: Any) -> Any:
        return args, kwargs


class dev:  # pragma: no cover
    class ConsoleRenderer:
        def __call__(self, *args: Any, **kwargs: Any) -> str:
            return ""


def make_filtering_bound_logger(level: int) -> Callable[[str], _LoggerAdapter]:  # pragma: no cover
    def factory(name: str) -> _LoggerAdapter:
        logging.getLogger(name).setLevel(level)
        return _LoggerAdapter(name)

    return factory
