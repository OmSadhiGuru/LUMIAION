"""LUMIAION crypto trading bot.

Modules:
  config         - environment-driven configuration (exchanges, risk, strategy params)
  exchange_manager - ccxt-based multi-exchange connectivity
  indicators     - EMA / RSI / ATR / trend helpers
  fvg            - Fair Value Gap (ICT / Smart Money Concepts) detection
  arbitrage      - cross-exchange price-spread scanner
  signal_engine  - confluence-based probability scoring of trade setups
  risk_manager   - position sizing and portfolio-level risk limits
  executor       - order execution (live or dry-run)
  storage        - SQLite trade journal and equity history
  notifier       - Telegram alerts
  bot            - main orchestration loop
"""
