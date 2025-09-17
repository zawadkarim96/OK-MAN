"""MT5 bridge connectivity layer."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import AsyncIterator

import zmq
import zmq.asyncio
from structlog import get_logger

from .protocol import BridgeMessage

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class BridgeConfig:
    host: str = "127.0.0.1"
    port: int = 5555


class MT5Bridge:
    """Simple ZeroMQ bridge prototype."""

    def __init__(self, config: BridgeConfig) -> None:
        self._config = config
        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect(f"tcp://{config.host}:{config.port}")

    async def send(self, message: BridgeMessage) -> None:
        LOGGER.debug("bridge_send", message=message)
        await self._socket.send_string(json.dumps(message.to_dict()))

    async def recv(self) -> BridgeMessage:
        raw = await self._socket.recv_string()
        payload = json.loads(raw)
        return BridgeMessage.from_dict(payload)

    async def stream(self) -> AsyncIterator[BridgeMessage]:
        while True:
            yield await self.recv()


async def main() -> None:
    bridge = MT5Bridge(BridgeConfig())
    async for message in bridge.stream():
        LOGGER.info("bridge_message", message=message)


if __name__ == "__main__":
    asyncio.run(main())
