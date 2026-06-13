import pytest

from crypto_bot.arbitrage import scan_all, scan_pair
from crypto_bot.config import ArbitrageConfig


class FakeExchangeManager:
    """Minimal stand-in for ExchangeManager: prices[exchange_id][symbol] -> last price."""

    def __init__(self, prices):
        self._prices = prices

    def exchange_ids(self):
        return list(self._prices.keys())

    def fetch_ticker(self, exchange_id, symbol):
        price = self._prices.get(exchange_id, {}).get(symbol)
        if price is None:
            return None
        return {"last": price}


def test_scan_pair_finds_opportunity_above_threshold():
    manager = FakeExchangeManager({
        "kraken": {"BTC/USDT": 100.0},
        "kucoin": {"BTC/USDT": 102.0},
    })
    config = ArbitrageConfig(min_spread_pct=0.5, taker_fee_pct=0.1)

    opp = scan_pair(manager, "BTC/USDT", config)

    assert opp is not None
    assert opp.buy_exchange == "kraken"
    assert opp.sell_exchange == "kucoin"
    assert opp.gross_spread_pct == pytest.approx(2.0)
    assert opp.net_spread_pct == pytest.approx(1.8)


def test_scan_pair_returns_none_below_threshold():
    manager = FakeExchangeManager({
        "kraken": {"BTC/USDT": 100.0},
        "kucoin": {"BTC/USDT": 100.05},
    })
    config = ArbitrageConfig(min_spread_pct=0.5, taker_fee_pct=0.1)

    assert scan_pair(manager, "BTC/USDT", config) is None


def test_scan_pair_requires_at_least_two_exchanges():
    manager = FakeExchangeManager({"kraken": {"BTC/USDT": 100.0}})
    config = ArbitrageConfig(min_spread_pct=0.5, taker_fee_pct=0.1)

    assert scan_pair(manager, "BTC/USDT", config) is None


def test_scan_all_sorts_by_net_spread_descending():
    manager = FakeExchangeManager({
        "kraken": {"BTC/USDT": 100.0, "ETH/USDT": 100.0},
        "kucoin": {"BTC/USDT": 101.0, "ETH/USDT": 105.0},
    })
    config = ArbitrageConfig(min_spread_pct=0.1, taker_fee_pct=0.1)

    opps = scan_all(manager, ["BTC/USDT", "ETH/USDT"], config)

    assert [o.symbol for o in opps] == ["ETH/USDT", "BTC/USDT"]
