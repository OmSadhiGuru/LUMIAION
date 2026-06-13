import pandas as pd

from crypto_bot.fvg import detect_fvgs, latest_unfilled_fvg


def _make_df(highs, lows):
    return pd.DataFrame({"high": highs, "low": lows})


def test_bullish_fvg_detected_and_unfilled():
    df = _make_df(
        highs=[10, 15, 20, 21, 22],
        lows=[9, 14, 18, 19, 20],
    )
    gaps = detect_fvgs(df)
    bullish_gaps = [g for g in gaps if g.direction == "bullish"]
    assert bullish_gaps

    first = bullish_gaps[0]
    assert first.bottom == 10
    assert first.top == 18
    assert first.filled is False

    latest = latest_unfilled_fvg(df, direction="bullish")
    assert latest is not None
    assert latest.direction == "bullish"


def test_bullish_fvg_marked_filled_when_price_returns():
    df = _make_df(
        highs=[10, 15, 20, 16],
        lows=[9, 14, 18, 11],
    )
    gaps = detect_fvgs(df)
    matching = [g for g in gaps if g.direction == "bullish" and g.bottom == 10 and g.top == 18]
    assert len(matching) == 1
    assert matching[0].filled is True

    assert latest_unfilled_fvg(df, direction="bullish") is None


def test_bearish_fvg_detected():
    df = _make_df(
        highs=[100, 95, 90, 88, 86],
        lows=[98, 93, 88, 86, 84],
    )
    gaps = detect_fvgs(df)
    bearish_gaps = [g for g in gaps if g.direction == "bearish"]
    assert bearish_gaps

    first = bearish_gaps[0]
    assert first.top == 98
    assert first.bottom == 90


def test_min_gap_pct_filters_small_gaps():
    df = _make_df(
        highs=[10, 15, 20, 21, 22],
        lows=[9, 14, 18, 19, 20],
    )
    gaps_all = detect_fvgs(df, min_gap_pct=0.0)
    gaps_strict = detect_fvgs(df, min_gap_pct=1000.0)

    assert gaps_all
    assert gaps_strict == []
