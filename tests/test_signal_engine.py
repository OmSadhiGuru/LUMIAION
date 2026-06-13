import pandas as pd

from crypto_bot.signal_engine import evaluate


def _build_uptrend_df(n=60):
    """A steady uptrend whose final candles form a naturally unfilled bullish FVG."""
    closes = [100.0 + i for i in range(n)]
    highs = [c + 0.5 for c in closes]
    lows = [c - 0.5 for c in closes]
    return pd.DataFrame({
        "open": closes,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": [1.0] * n,
    })


def test_evaluate_scores_full_confluence_long_setup():
    df = _build_uptrend_df()

    setup = evaluate(df, symbol="BTC/USDT", exchange="kraken", timeframe="1h")

    assert setup is not None
    assert setup.direction == "long"
    assert setup.score == 100.0
    assert setup.entry_zone is not None
    assert setup.entry_zone[0] < setup.entry_zone[1]


def test_evaluate_returns_none_for_flat_market():
    n = 60
    flat = pd.DataFrame({
        "open": [100.0] * n,
        "high": [100.5] * n,
        "low": [99.5] * n,
        "close": [100.0] * n,
        "volume": [1.0] * n,
    })

    assert evaluate(flat, symbol="BTC/USDT", exchange="kraken", timeframe="1h") is None


def test_evaluate_returns_none_with_too_few_candles():
    df = _build_uptrend_df(n=10)

    assert evaluate(df, symbol="BTC/USDT", exchange="kraken", timeframe="1h") is None
