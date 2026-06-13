"""Order execution layer with a dry-run safety mode.

Live orders are only sent when BOTH:
  - `live_trading` is True (set ENABLE_LIVE_TRADING=true), AND
  - the target exchange has API credentials configured.

Otherwise every order is simulated and logged - nothing is sent to the
exchange. This means a misconfigured exchange (missing keys) never
silently fails a live trade; it just stays in simulation for that venue.
"""
from __future__ import annotations

import logging

from .exchange_manager import ExchangeManager
from .risk_manager import PositionPlan

logger = logging.getLogger(__name__)


class OrderExecutor:
    def __init__(self, exchange_manager: ExchangeManager, live_trading: bool):
        self.exchange_manager = exchange_manager
        self.live_trading = live_trading

    def _is_live(self, exchange_id: str) -> bool:
        return self.live_trading and self.exchange_manager.can_trade(exchange_id)

    def open_position(self, plan: PositionPlan) -> dict:
        side = "buy" if plan.direction == "long" else "sell"

        if self._is_live(plan.exchange):
            order = self.exchange_manager.create_order(
                plan.exchange, plan.symbol, side, plan.size_base, order_type="market",
            )
            logger.info("LIVE order placed: %s", order)
            return order

        logger.info(
            "[DRY-RUN] would %s %.8f %s on %s at ~%.6f (SL %.6f / TP %.6f)",
            side, plan.size_base, plan.symbol, plan.exchange,
            plan.entry_price, plan.stop_loss, plan.take_profit,
        )
        return {"status": "simulated", "side": side, "symbol": plan.symbol,
                "amount": plan.size_base, "price": plan.entry_price}

    def close_position(self, plan: PositionPlan) -> dict:
        side = "sell" if plan.direction == "long" else "buy"

        if self._is_live(plan.exchange):
            order = self.exchange_manager.create_order(
                plan.exchange, plan.symbol, side, plan.size_base, order_type="market",
            )
            logger.info("LIVE close order placed: %s", order)
            return order

        logger.info(
            "[DRY-RUN] would %s %.8f %s on %s to close position",
            side, plan.size_base, plan.symbol, plan.exchange,
        )
        return {"status": "simulated", "side": side, "symbol": plan.symbol, "amount": plan.size_base}
