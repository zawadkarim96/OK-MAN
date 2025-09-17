"""FastAPI application exposing control plane endpoints."""

from __future__ import annotations

from typing import Any, Callable

try:  # pragma: no cover - optional dependency
    from fastapi import FastAPI, HTTPException
except Exception:  # pragma: no cover - fallback stubs
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str) -> None:
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class FastAPI:  # type: ignore[override]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.routes: dict[str, Callable[..., Any]] = {}

        def get(self, path: str, response_model: Any | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
                self.routes[path] = func
                return func

            return decorator

        def post(self, path: str, response_model: Any | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            return self.get(path, response_model=response_model)

from src.api.schemas import BridgeCommand, HealthResponse, StrategyRunRequest
from src.strategy.signal_ensemble import run_mode

app = FastAPI(title="ai-scalper-god")


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/run")
async def run_strategy(request: StrategyRunRequest) -> dict[str, str]:
    if request.mode not in {"live", "paper"}:
        raise HTTPException(status_code=400, detail="Invalid mode")
    run_mode(request.mode)
    return {"status": "started", "mode": request.mode}


@app.post("/bridge/command")
async def send_bridge_command(command: BridgeCommand) -> dict[str, str]:
    return {"status": "queued", "command": command.command}
