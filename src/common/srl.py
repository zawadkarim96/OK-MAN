"""Serialization helpers for strategy state and features."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import msgpack


def dump_json(data: Dict[str, Any], path: Path) -> None:
    """Write *data* to *path* as JSON."""

    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def load_json(path: Path) -> Dict[str, Any]:
    """Read JSON file into a dictionary."""

    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dump_msgpack(data: Dict[str, Any], path: Path) -> None:
    """Serialize *data* using msgpack."""

    path.write_bytes(msgpack.packb(data, use_bin_type=True))


def load_msgpack(path: Path) -> Dict[str, Any]:
    """Deserialize msgpack bytes."""

    if not path.exists():
        return {}
    return msgpack.unpackb(path.read_bytes(), raw=False)


__all__ = ["dump_json", "load_json", "dump_msgpack", "load_msgpack"]
