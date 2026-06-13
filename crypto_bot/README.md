# LUMIAION Crypto Trading Bot

An automated market-scanning and trading bot covering three strategies:

1. **Cross-exchange arbitrage** - compares prices for the same pair across
   high-liquidity venues (Kraken, Coinbase) and smaller venues (KuCoin,
   Bybit) where altcoins often trade at wider spreads, and flags
   opportunities net of estimated fees.
2. **Fair Value Gap (FVG) trading** - detects ICT/Smart-Money-Concepts style
   3-candle imbalances and uses unfilled gaps in the direction of the trend
   as high-probability entry zones.
3. **Confluence-based probability scoring** - ranks every symbol/exchange/
   timeframe combination (short-term: 15m/1h, long-term: 4h/1d) by how many
   factors (trend, momentum, FVG presence, price proximity to the FVG zone)
   currently line up, so the bot always trades the highest-probability
   setups available.

A risk manager sizes every position from the configured
`MAX_RISK_PER_TRADE_PCT`, enforces a max number of concurrent positions and a
daily-loss circuit breaker, and every trade (real or simulated) is journaled
to SQLite so monthly P&L can be reviewed.

## Setup

```bash
pip install -r crypto_bot/requirements.txt
cp crypto_bot/.env.example crypto_bot/.env
# edit crypto_bot/.env with your exchange API keys and risk settings
```

## Running

```bash
# single cycle, useful for testing your config
python -m crypto_bot.run --once

# run continuously
python -m crypto_bot.run
```

## Live trading vs. dry-run

By default (`ENABLE_LIVE_TRADING=false`, or no API keys for an exchange),
every order is **simulated and logged** - the bot still scans the market,
scores setups, manages a simulated portfolio and sends notifications, but
nothing is sent to any exchange.

To place real orders on an exchange:

1. Set `ENABLE_LIVE_TRADING=true` in `crypto_bot/.env`.
2. Provide API key/secret (and passphrase for Coinbase/KuCoin) for that
   exchange.
3. Make sure the API key has **trading permissions only** (no withdrawal
   permission) and is restricted to your server's IP if the exchange
   supports it.

An exchange without configured API credentials always stays in market-data
/ dry-run mode for trading, even if `ENABLE_LIVE_TRADING=true` - it is still
used for arbitrage price comparisons and signal scanning.

## Important risk notes

- **No bot can guarantee a profit, monthly or otherwise.** This bot
  automates a strategy and enforces risk limits; it does not eliminate
  market risk. Start with `ENABLE_LIVE_TRADING=false` and small position
  sizes, and validate behaviour over time before increasing exposure.
- The arbitrage scanner assumes the bot **already holds balances of the
  relevant assets on each exchange** - it does not transfer funds between
  exchanges (that is slow and itself risky).
- Tune `MAX_RISK_PER_TRADE_PCT`, `MAX_DAILY_LOSS_PCT` and
  `MAX_OPEN_POSITIONS` to your own risk tolerance before going live.

## Module overview

| Module | Purpose |
| --- | --- |
| `config.py` | Loads all settings from environment variables / `.env` |
| `exchange_manager.py` | ccxt wrapper for tickers, OHLCV, balances, orders |
| `indicators.py` | EMA, RSI, ATR, trend direction helpers |
| `fvg.py` | Fair Value Gap detection |
| `signal_engine.py` | Confluence scoring & ranking of trade setups |
| `arbitrage.py` | Cross-exchange spread scanner |
| `risk_manager.py` | Position sizing, exposure & daily-loss limits |
| `executor.py` | Order execution (live or dry-run) |
| `storage.py` | SQLite trade journal & equity history |
| `notifier.py` | Telegram alerts |
| `bot.py` | Main loop tying everything together |
| `run.py` | CLI entry point |

## Tests

```bash
pip install pytest
pytest tests/
```
