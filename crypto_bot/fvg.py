"""Fair Value Gap (FVG) detection - ICT / Smart Money Concepts.

A Fair Value Gap is a 3-candle imbalance pattern formed when price moves
so fast that it leaves an untraded gap between candles:

  - Bullish FVG: the high of candle[i-1] is below the low of candle[i+1].
    The zone [high(i-1), low(i+1)] is an area price often returns to
    ("fills"/"mitigates") before continuing higher.
  - Bearish FVG: the low of candle[i-1] is above the high of candle[i+1].
    The zone [high(i+1), low(i-1)] often gets retested before price
    continues lower.

These gaps are commonly used as high-probability re-entry zones in the
direction of the prevailing trend.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class FairValueGap:
    index: int          # index of the middle (displacement) candle
    direction: str      # "bullish" or "bearish"
    top: float
    bottom: float
    filled: bool = False

    @property
    def size_pct(self) -> float:
        midpoint = (self.top + self.bottom) / 2
        if midpoint == 0:
            return 0.0
        return (self.top - self.bottom) / midpoint * 100

    def contains(self, price: float) -> bool:
        return self.bottom <= price <= self.top


def detect_fvgs(df: pd.DataFrame, min_gap_pct: float = 0.0) -> list[FairValueGap]:
    """Scan a candlestick dataframe (columns: high, low) for fair value gaps.

    Gaps are returned in chronological order. Each gap is flagged as
    `filled` if any later candle's range overlapped the gap zone.
    """
    gaps: list[FairValueGap] = []
    highs = df["high"].to_numpy()
    lows = df["low"].to_numpy()

    for i in range(1, len(df) - 1):
        prev_high, prev_low = highs[i - 1], lows[i - 1]
        next_high, next_low = highs[i + 1], lows[i + 1]

        gap: Optional[FairValueGap] = None
        if next_low > prev_high:
            gap = FairValueGap(index=i, direction="bullish", top=next_low, bottom=prev_high)
        elif next_high < prev_low:
            gap = FairValueGap(index=i, direction="bearish", top=prev_low, bottom=next_high)

        if gap is None or gap.size_pct < min_gap_pct:
            continue

        for j in range(i + 2, len(df)):
            if lows[j] <= gap.top and highs[j] >= gap.bottom:
                gap.filled = True
                break

        gaps.append(gap)

    return gaps


def latest_unfilled_fvg(df: pd.DataFrame, direction: Optional[str] = None,
                         min_gap_pct: float = 0.0) -> Optional[FairValueGap]:
    """Return the most recent unfilled FVG, optionally filtered by direction."""
    for gap in reversed(detect_fvgs(df, min_gap_pct=min_gap_pct)):
        if gap.filled:
            continue
        if direction and gap.direction != direction:
            continue
        return gap
    return None
