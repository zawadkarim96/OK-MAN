"""Sandbox runner orchestrating research evaluations."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class SandboxConfig:
    interval_seconds: int = 60


class SandboxRunner:
    def __init__(self, config: SandboxConfig | None = None) -> None:
        self._config = config or SandboxConfig()
        self._running = False

    async def run(self) -> None:
        self._running = True
        while self._running:
            LOGGER.info("sandbox_cycle")
            await asyncio.sleep(self._config.interval_seconds)

    def stop(self) -> None:
        self._running = False


async def main() -> None:
    runner = SandboxRunner()
    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())
