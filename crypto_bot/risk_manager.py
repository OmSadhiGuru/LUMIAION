"""Position sizing and portfolio-level risk controls.

Every position is sized so that, if its stop-loss is hit, the loss is
capped at `max_risk_per_trade_pct` of current equity. A daily loss
circuit breaker halts new entries once `max_daily_loss_pct` of equity
has been lost on the day, and `max_open_positions` caps concurrent
exposure.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import RiskConfig


@dataclass
class PositionPlan:
    exchange: str
    symbol: str
    direction: str  # "long" or "short"
    entry_price: float
    stop_loss: float
    take_profit: float
    size_quote: float   # position size in quote currency (e.g. USDT)
    size_base: float    # position size in base currency
    trade_id: Optional[int] = None  # set once persisted to the trade store

    @property
    def key(self) -> str:
        return f"{self.exchange}:{self.symbol}"

    @property
    def risk_reward_ratio(self) -> float:
        risk = abs(self.entry_price - self.stop_loss)
        reward = abs(self.take_profit - self.entry_price)
        return reward / risk if risk else 0.0


class RiskManager:
    """Tracks equity and enforces position-sizing / loss-limit rules."""

    def __init__(self, config: RiskConfig, starting_equity: float):
        self.config = config
        self.equity = starting_equity
        self.day_start_equity = starting_equity
        self.open_positions: dict[str, PositionPlan] = {}

    def reset_day(self) -> None:
        self.day_start_equity = self.equity

    def daily_loss_pct(self) -> float:
        if self.day_start_equity == 0:
            return 0.0
        return (self.day_start_equity - self.equity) / self.day_start_equity * 100

    def trading_halted(self) -> bool:
        return self.daily_loss_pct() >= self.config.max_daily_loss_pct

    def can_open_position(self, exchange: str, symbol: str) -> bool:
        if self.trading_halted():
            return False
        if f"{exchange}:{symbol}" in self.open_positions:
            return False
        return len(self.open_positions) < self.config.max_open_positions

    def build_position_plan(self, exchange: str, symbol: str, direction: str, entry_price: float,
                              stop_loss: Optional[float] = None,
                              take_profit: Optional[float] = None) -> Optional[PositionPlan]:
        """Build a risk-sized position plan, or None if the trade fails risk checks."""
        if not self.can_open_position(exchange, symbol):
            return None

        if entry_price <= 0:
            return None

        if stop_loss is None:
            sl_pct = self.config.default_stop_loss_pct / 100
            stop_loss = entry_price * (1 - sl_pct) if direction == "long" else entry_price * (1 + sl_pct)

        if take_profit is None:
            tp_pct = self.config.default_take_profit_pct / 100
            take_profit = entry_price * (1 + tp_pct) if direction == "long" else entry_price * (1 - tp_pct)

        risk_per_unit = abs(entry_price - stop_loss)
        if risk_per_unit <= 0:
            return None

        reward_per_unit = abs(take_profit - entry_price)
        if reward_per_unit / risk_per_unit < self.config.min_risk_reward_ratio:
            return None

        max_risk_amount = self.equity * (self.config.max_risk_per_trade_pct / 100)
        size_base = max_risk_amount / risk_per_unit
        size_quote = size_base * entry_price

        max_position_quote = self.equity * (self.config.max_position_pct / 100)
        if size_quote > max_position_quote:
            size_quote = max_position_quote
            size_base = size_quote / entry_price

        return PositionPlan(
            exchange=exchange,
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            size_quote=size_quote,
            size_base=size_base,
        )

    def register_open(self, plan: PositionPlan) -> None:
        self.open_positions[plan.key] = plan

    def register_close(self, plan: PositionPlan, exit_price: float) -> float:
        """Remove the position, apply its P&L to equity, and return the P&L."""
        self.open_positions.pop(plan.key, None)
        direction_mult = 1 if plan.direction == "long" else -1
        pnl = (exit_price - plan.entry_price) * plan.size_base * direction_mult
        self.equity += pnl
        return pnl

    def check_exit(self, plan: PositionPlan, current_price: float) -> Optional[str]:
        """Return "stop_loss", "take_profit" or None based on the current price."""
        if plan.direction == "long":
            if current_price <= plan.stop_loss:
                return "stop_loss"
            if current_price >= plan.take_profit:
                return "take_profit"
        else:
            if current_price >= plan.stop_loss:
                return "stop_loss"
            if current_price <= plan.take_profit:
                return "take_profit"
        return None
