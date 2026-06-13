import pytest

from crypto_bot.config import RiskConfig
from crypto_bot.risk_manager import RiskManager


def _config(**overrides):
    base = dict(
        max_risk_per_trade_pct=1.0,
        max_position_pct=20.0,
        max_open_positions=2,
        max_daily_loss_pct=5.0,
        default_stop_loss_pct=2.0,
        default_take_profit_pct=4.0,
        min_risk_reward_ratio=1.5,
    )
    base.update(overrides)
    return RiskConfig(**base)


def test_build_position_plan_sizes_by_risk_and_caps_position():
    risk = RiskManager(_config(), starting_equity=10_000.0)

    plan = risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0)

    assert plan is not None
    assert plan.stop_loss == pytest.approx(98.0)
    assert plan.take_profit == pytest.approx(104.0)
    assert plan.risk_reward_ratio == pytest.approx(2.0)
    # 1% risk sizing would be 5,000 quote, but max_position_pct (20%) caps it at 2,000.
    assert plan.size_quote == pytest.approx(2000.0)
    assert plan.size_base == pytest.approx(20.0)


def test_build_position_plan_caps_at_max_position_pct():
    risk = RiskManager(_config(max_risk_per_trade_pct=10.0, max_position_pct=5.0), starting_equity=10_000.0)

    plan = risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0)

    assert plan is not None
    assert plan.size_quote == pytest.approx(500.0)
    assert plan.size_base == pytest.approx(5.0)


def test_build_position_plan_rejects_poor_risk_reward():
    risk = RiskManager(_config(min_risk_reward_ratio=3.0), starting_equity=10_000.0)

    # default SL=2%, TP=4% -> R:R = 2.0 < 3.0
    assert risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0) is None


def test_max_open_positions_enforced():
    risk = RiskManager(_config(max_open_positions=1), starting_equity=10_000.0)

    plan1 = risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0)
    assert plan1 is not None
    risk.register_open(plan1)

    plan2 = risk.build_position_plan("kraken", "ETH/USDT", "long", entry_price=100.0)
    assert plan2 is None


def test_register_close_applies_pnl_to_equity():
    risk = RiskManager(_config(), starting_equity=10_000.0)
    plan = risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0)
    risk.register_open(plan)

    pnl = risk.register_close(plan, exit_price=plan.stop_loss)

    assert pnl < 0
    assert risk.equity == pytest.approx(10_000.0 + pnl)
    assert plan.key not in risk.open_positions


def test_check_exit_long_and_short():
    risk = RiskManager(_config(), starting_equity=10_000.0)

    long_plan = risk.build_position_plan("kraken", "BTC/USDT", "long", entry_price=100.0)
    assert risk.check_exit(long_plan, 97.0) == "stop_loss"
    assert risk.check_exit(long_plan, 105.0) == "take_profit"
    assert risk.check_exit(long_plan, 100.0) is None

    short_plan = risk.build_position_plan("kraken", "ETH/USDT", "short", entry_price=100.0)
    assert risk.check_exit(short_plan, 103.0) == "stop_loss"
    assert risk.check_exit(short_plan, 95.0) == "take_profit"
