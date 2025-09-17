"""Reinforcement learning agent prototype."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from stable_baselines3 import PPO


@dataclass(slots=True)
class RLConfig:
    policy: str = "MlpPolicy"
    timesteps: int = 1000


class RLAgent:
    """Thin wrapper around PPO for experimentation."""

    def __init__(self, env: Any, config: RLConfig | None = None) -> None:
        self._config = config or RLConfig()
        self._model = PPO(self._config.policy, env, verbose=0)

    def train(self) -> None:
        self._model.learn(total_timesteps=self._config.timesteps)

    def predict(self, observation: Any) -> Any:
        action, _ = self._model.predict(observation, deterministic=True)
        return action


__all__ = ["RLAgent", "RLConfig"]
