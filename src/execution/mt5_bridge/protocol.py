"""Bridge protocol definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class BridgeMessage:
    type: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "payload": self.payload}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BridgeMessage":
        return cls(type=str(data.get("type", "unknown")), payload=dict(data.get("payload", {})))


__all__ = ["BridgeMessage"]
