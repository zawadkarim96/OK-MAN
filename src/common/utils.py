"""Utility helpers shared across the project."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Sequence, Tuple

import numpy as np
import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load a YAML file and return a dictionary.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML content as a dictionary.
    """

    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def percentile_rank(values: Sequence[float], value: float) -> float:
    """Compute the percentile rank of a value within a sample."""

    if not values:
        return 0.0
    arr = np.asarray(values, dtype=float)
    rank = float(np.mean(arr <= value) * 100.0)
    return rank


def chunked(iterable: Iterable[Any], size: int) -> Iterator[Tuple[Any, ...]]:
    """Yield fixed-size chunks from *iterable*."""

    if size <= 0:
        raise ValueError("size must be positive")
    chunk: List[Any] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield tuple(chunk)
            chunk.clear()
    if chunk:
        yield tuple(chunk)
