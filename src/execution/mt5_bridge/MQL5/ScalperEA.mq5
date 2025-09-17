//+------------------------------------------------------------------+
//|  Scalper EA placeholder                                          |
//|  TODO: Implement streaming of ticks and DOM via ZeroMQ.          |
//+------------------------------------------------------------------+
#property strict

int OnInit()
  {
   return(INIT_SUCCEEDED);
  }

void OnTick()
  {
   // TODO: Serialize tick data and send to Python bridge.
  }

void OnDeinit(const int reason)
  {
   // TODO: Close sockets gracefully.
  }
