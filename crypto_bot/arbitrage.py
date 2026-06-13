"""Cross-exchange arbitrage scanner.

Compares the current price of each configured trading pair across all
connected exchanges (e.g. higher-liquidity venues like Kraken/Coinbase
vs. smaller venues like KuCoin/Bybit, where altcoin spreads tend to be
wider) and flags opportunities where the spread between the highest and
lowest price exceeds the configured threshold, net of estimated taker
fees on both legs.

Note: this strategy assumes the bot already holds balances of both the
base and quote asset on each exchange involved (buy on the cheap
exchange, sell on the expensive one in the same cycle). Moving funds
between exchanges is not instantaneous and is intentionally not handled
here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import ArbitrageConfig
from .exchange_manager import ExchangeManager


@dataclass
class ArbitrageOpportunity:
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    gross_spread_pct: float
    net_spread_pct: float

    def __str__(self) -> str:
        return (
            f"{self.symbol}: buy on {self.buy_exchange} @ {self.buy_price:.6f}, "
            f"sell on {self.sell_exchange} @ {self.sell_price:.6f} "
            f"(net spread {self.net_spread_pct:.3f}%)"
        )


def scan_pair(exchange_manager: ExchangeManager, symbol: str,
               config: ArbitrageConfig) -> Optional[ArbitrageOpportunity]:
    """Return the best arbitrage opportunity for `symbol` across all exchanges, if any."""
    prices: dict[str, float] = {}
    for exchange_id in exchange_manager.exchange_ids():
        ticker = exchange_manager.fetch_ticker(exchange_id, symbol)
        if not ticker:
            continue
        price = ticker.get("last") or ticker.get("close")
        if price:
            prices[exchange_id] = float(price)

    if len(prices) < 2:
        return None

    buy_exchange = min(prices, key=prices.get)
    sell_exchange = max(prices, key=prices.get)
    buy_price = prices[buy_exchange]
    sell_price = prices[sell_exchange]

    if buy_exchange == sell_exchange or buy_price <= 0:
        return None

    gross_spread_pct = (sell_price - buy_price) / buy_price * 100
    fees_pct = config.taker_fee_pct * 2  # one taker fee per leg
    net_spread_pct = gross_spread_pct - fees_pct

    if net_spread_pct < config.min_spread_pct:
        return None

    return ArbitrageOpportunity(
        symbol=symbol,
        buy_exchange=buy_exchange,
        sell_exchange=sell_exchange,
        buy_price=buy_price,
        sell_price=sell_price,
        gross_spread_pct=gross_spread_pct,
        net_spread_pct=net_spread_pct,
    )


def scan_all(exchange_manager: ExchangeManager, symbols: list[str],
              config: ArbitrageConfig) -> list[ArbitrageOpportunity]:
    """Scan all `symbols` and return opportunities sorted by net spread, best first."""
    opportunities = []
    for symbol in symbols:
        opp = scan_pair(exchange_manager, symbol, config)
        if opp:
            opportunities.append(opp)
    return sorted(opportunities, key=lambda o: o.net_spread_pct, reverse=True)
