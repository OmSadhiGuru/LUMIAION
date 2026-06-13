"""Confluence-based probability scoring for trade setups.

Combines several independent signals into a 0-100 score representing
how many factors line up in favour of a long or short position on a
given symbol/exchange/timeframe:

  - Trend alignment (fast EMA vs slow EMA)
  - Momentum (RSI not overextended in the trade direction)
  - An unfilled Fair Value Gap in the direction of the trend, which acts
    as a high-probability re-entry zone
  - Price currently sitting inside/near that FVG zone (ready to trigger)

Each factor contributes a fixed weight; the final score is the
percentage of available weight the current setup satisfies. Running the
same evaluation across short timeframes (15m/1h) and long timeframes
(4h/1d) surfaces both short-term and long-term opportunities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from . import indicators
from .fvg import FairValueGap, latest_unfilled_fvg

_WEIGHTS = {
    "trend": 35,
    "momentum": 25,
    "fvg_present": 25,
    "price_near_fvg": 15,
}
TOTAL_WEIGHT = sum(_WEIGHTS.values())


@dataclass
class TradeSetup:
    symbol: str
    exchange: str
    timeframe: str
    direction: str  # "long" or "short"
    score: float    # 0-100, higher = more confluence factors satisfied
    current_price: float
    entry_zone: Optional[tuple[float, float]]
    reasons: list[str]

    def __str__(self) -> str:
        zone = f"{self.entry_zone[0]:.6f}-{self.entry_zone[1]:.6f}" if self.entry_zone else "n/a"
        return (
            f"[{self.score:5.1f}%] {self.symbol} {self.timeframe} {self.direction.upper()} "
            f"on {self.exchange} (price {self.current_price:.6f}, entry zone {zone}) "
            f"- {', '.join(self.reasons)}"
        )


def evaluate(df: pd.DataFrame, symbol: str, exchange: str, timeframe: str,
              min_gap_pct: float = 0.0) -> Optional[TradeSetup]:
    """Score the latest candle of `df` for the best long/short setup.

    Returns None if there isn't enough data or the trend is flat.
    """
    if len(df) < 60:
        return None

    close = df["close"]
    current_price = float(close.iloc[-1])
    trend = indicators.trend_direction(df)
    rsi_value = float(indicators.rsi(close).iloc[-1])

    if trend == "bullish":
        direction = "long"
    elif trend == "bearish":
        direction = "short"
    else:
        return None

    score = 0.0
    reasons: list[str] = [f"trend {trend}"]
    score += _WEIGHTS["trend"]

    if direction == "long" and rsi_value < 70:
        score += _WEIGHTS["momentum"]
        reasons.append(f"RSI {rsi_value:.1f} not overbought")
    elif direction == "short" and rsi_value > 30:
        score += _WEIGHTS["momentum"]
        reasons.append(f"RSI {rsi_value:.1f} not oversold")

    fvg_direction = "bullish" if direction == "long" else "bearish"
    gap: Optional[FairValueGap] = latest_unfilled_fvg(df, direction=fvg_direction, min_gap_pct=min_gap_pct)
    entry_zone = None
    if gap:
        score += _WEIGHTS["fvg_present"]
        reasons.append(f"unfilled {gap.direction} FVG ({gap.bottom:.6f}-{gap.top:.6f})")
        entry_zone = (gap.bottom, gap.top)

        gap_mid = (gap.top + gap.bottom) / 2
        distance_pct = abs(current_price - gap_mid) / gap_mid * 100 if gap_mid else 0.0
        if distance_pct <= max(gap.size_pct, 0.5):
            score += _WEIGHTS["price_near_fvg"]
            reasons.append("price near FVG entry zone")

    score_pct = score / TOTAL_WEIGHT * 100

    return TradeSetup(
        symbol=symbol,
        exchange=exchange,
        timeframe=timeframe,
        direction=direction,
        score=score_pct,
        current_price=current_price,
        entry_zone=entry_zone,
        reasons=reasons,
    )


def rank_setups(setups: list[TradeSetup], min_score: float = 0.0) -> list[TradeSetup]:
    """Return setups with score >= min_score, best first."""
    filtered = [s for s in setups if s.score >= min_score]
    return sorted(filtered, key=lambda s: s.score, reverse=True)
