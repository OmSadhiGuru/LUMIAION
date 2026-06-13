"""Lightweight technical indicators built on pandas (no TA-Lib dependency)."""
from __future__ import annotations

import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    rsi_values = 100 - (100 / (1 + rs))
    return rsi_values.fillna(50)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    true_range = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return true_range.ewm(alpha=1 / period, adjust=False).mean()


def trend_direction(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> str:
    """Return "bullish", "bearish" or "neutral" based on EMA crossover."""
    if len(df) < slow:
        return "neutral"
    fast_ema = ema(df["close"], fast).iloc[-1]
    slow_ema = ema(df["close"], slow).iloc[-1]
    if fast_ema > slow_ema:
        return "bullish"
    if fast_ema < slow_ema:
        return "bearish"
    return "neutral"


def ohlcv_to_dataframe(ohlcv: list) -> pd.DataFrame:
    """Convert a ccxt OHLCV list (timestamp, open, high, low, close, volume) to a DataFrame."""
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
