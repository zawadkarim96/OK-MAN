# MT5 Bridge Setup

1. Install MetaTrader 5 and enable algorithmic trading.
2. Copy `src/execution/mt5_bridge/MQL5/ScalperEA.mq5` into the MT5 experts directory and compile it.
3. Configure the Expert Advisor inputs to point at the bridge host/port defined in `configs/mt5.yaml`.
4. Launch the Python side via `make bridge` which starts the ZeroMQ/socket server.
5. Attach the EA to each required symbol chart. The EA streams ticks and depth-of-market data to Python and listens for order instructions.
6. Ensure firewall rules allow traffic on the configured port.

The bridge measures latency and automatically attempts reconnection on failure. All messages conform to the JSON schema in `src/execution/mt5_bridge/protocol.py`.
