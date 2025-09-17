# Order-Flow & LOB Analytics

The order-flow subsystem extracts low-latency features from depth-of-market and time-and-sales streams.

## Feature Overview

- **Imbalance** – Difference between aggregated bid and ask volumes at top *n* levels.
- **Cumulative Volume Delta (CVD)** – Running delta of aggressive buyer vs seller volume.
- **Queue Dynamics** – Position, churn rate, and survival probability of resting orders.
- **Depth Slope** – Regression of volume across price levels capturing convexity/concavity.
- **Microprice** – Weighted price to capture hidden order pressure.
- **Cancellation Rate** – Order cancels per second normalised by resting size.
- **Tape Metrics** – Trades per second, average trade size, aggressor ratio, sweep detection.

## Model Stub

`src/orderflow/lob_model.py` defines a Siamese-style PyTorch module that processes bid and ask tensors via shared encoders and attention layers. The forward method returns a short-horizon move probability used as a veto or confidence boost inside the ensemble.

## Latency Considerations

- Vectorised Numba kernels for indicator calculations.
- Shared-memory queues to pass data between ingest and feature modules.
- Batching windows no longer than 50 ms to remain responsive.
