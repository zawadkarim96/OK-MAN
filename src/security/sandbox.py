"""Sandbox executor for generated code."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from structlog import get_logger

LOGGER = get_logger(__name__)


def run_in_sandbox(command: List[str], cwd: Path | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    LOGGER.info("sandbox_execute", command=command)
    return subprocess.run(command, cwd=cwd, timeout=timeout, capture_output=True, text=True, check=False)


__all__ = ["run_in_sandbox"]
