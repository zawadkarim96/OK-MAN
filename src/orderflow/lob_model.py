"""PyTorch Siamese/attention model stub for LOB prediction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import torch
import torch.nn as nn


class _StreamEncoder(nn.Module):
    """Encode bid/ask streams via 1D convolutions."""

    def __init__(self, channels: int = 16) -> None:
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(1, channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(channels, channels, kernel_size=3, padding=1),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return self.conv(x)


class LobSiameseModel(nn.Module):
    """Siamese encoder with attention pooling."""

    def __init__(self) -> None:
        super().__init__()
        self.encoder = _StreamEncoder()
        self.attention = nn.MultiheadAttention(embed_dim=16, num_heads=4, batch_first=True)
        self.classifier = nn.Sequential(nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, 1), nn.Sigmoid())

    def forward(self, bids: torch.Tensor, asks: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        bid_encoded = self.encoder(bids)
        ask_encoded = self.encoder(asks)
        combined = torch.cat([bid_encoded, ask_encoded], dim=2)
        attn_output, _ = self.attention(combined, combined, combined)
        pooled = attn_output.mean(dim=1)
        return self.classifier(pooled)

    def predict(self, bids: torch.Tensor, asks: torch.Tensor) -> float:
        """Return a scalar probability."""

        with torch.no_grad():
            return float(self.forward(bids, asks).item())


@dataclass(slots=True)
class LobModelConfig:
    """Configuration placeholder for future hyper-parameters."""

    learning_rate: float = 1e-3
    dropout: float = 0.1


__all__ = ["LobSiameseModel", "LobModelConfig"]
