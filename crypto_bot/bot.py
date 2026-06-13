"""Main orchestration loop for the LUMIAION crypto trading bot.

Each cycle:
  1. Scan all configured trading pairs across exchanges for
     cross-exchange arbitrage opportunities (high vs. low market-value
     venues) and notify on anything actionable.
  2. For every pair/exchange/timeframe, fetch OHLCV data and run the
     Fair Value Gap + confluence signal engine to rank short-term
     (15m/1h) and long-term (4h/1d) setups by probability score.
  3. Manage open positions: close anything that has hit its stop-loss
     or take-profit.
  4. Open new positions for the highest-probability setups, subject to
     the risk manager's position-sizing and exposure limits.
  5. Persist equity history and send notifications.
"""
from __future__ import annotations

import datetime as dt
import logging
import time

from . import arbitrage, indicators, signal_engine
from .config import BotConfig
from .exchange_manager import ExchangeManager
from .executor import OrderExecutor
from .notifier import TelegramNotifier
from .risk_manager import RiskManager
from .storage import TradeStore

logger = logging.getLogger(__name__)

MIN_SETUP_SCORE = 50.0


class CryptoBot:
    def __init__(self, config: BotConfig):
        self.config = config
        self.exchange_manager = ExchangeManager(config.exchanges)
        self.executor = OrderExecutor(self.exchange_manager, config.live_trading)
        self.notifier = TelegramNotifier(config.telegram_token, config.telegram_chat_id)
        self.store = TradeStore(config.db_path)
        self.risk = RiskManager(config.risk, config.starting_equity)
        self._last_day = dt.date.today()

    def _maybe_reset_day(self) -> None:
        today = dt.date.today()
        if today != self._last_day:
            self.risk.reset_day()
            self._last_day = today

    def run_cycle(self) -> None:
        self._maybe_reset_day()

        if self.risk.trading_halted():
            logger.warning(
                "Daily loss limit reached (%.2f%% >= %.2f%%) - trading halted for today",
                self.risk.daily_loss_pct(), self.config.risk.max_daily_loss_pct,
            )
            self._manage_open_positions()
            return

        self._scan_arbitrage()
        setups = self._scan_signals()
        self._manage_open_positions()
        self._act_on_setups(setups)
        self.store.record_equity(dt.datetime.utcnow().isoformat(), self.risk.equity)

    def run_forever(self) -> None:
        logger.info(
            "Starting crypto bot - live_trading=%s, exchanges=%s, pairs=%s",
            self.config.live_trading, self.exchange_manager.exchange_ids(), self.config.pairs,
        )
        while True:
            try:
                self.run_cycle()
            except Exception:
                logger.exception("Error during bot cycle")
            time.sleep(self.config.poll_interval_seconds)

    # -- Strategy: cross-exchange arbitrage ---------------------------------
    def _scan_arbitrage(self) -> None:
        opportunities = arbitrage.scan_all(self.exchange_manager, self.config.pairs, self.config.arbitrage)
        for opp in opportunities:
            logger.info("Arbitrage opportunity: %s", opp)
            self.notifier.send(f"\U0001F4B1 Arbitrage: {opp}")

    # -- Strategy: Fair Value Gap + confluence signal engine -----------------
    def _scan_signals(self) -> list[signal_engine.TradeSetup]:
        all_setups: list[signal_engine.TradeSetup] = []
        timeframes = self.config.fvg.timeframes_short + self.config.fvg.timeframes_long

        for exchange_id in self.exchange_manager.exchange_ids():
            for symbol in self.config.pairs:
                for timeframe in timeframes:
                    ohlcv = self.exchange_manager.fetch_ohlcv(
                        exchange_id, symbol, timeframe, limit=self.config.fvg.lookback_candles,
                    )
                    if not ohlcv:
                        continue
                    df = indicators.ohlcv_to_dataframe(ohlcv)
                    setup = signal_engine.evaluate(
                        df, symbol, exchange_id, timeframe, min_gap_pct=self.config.fvg.min_gap_pct,
                    )
                    if setup:
                        all_setups.append(setup)

        ranked = signal_engine.rank_setups(all_setups, min_score=MIN_SETUP_SCORE)
        for setup in ranked[:10]:
            logger.info("Setup: %s", setup)
        return ranked

    # -- Position management --------------------------------------------------
    def _manage_open_positions(self) -> None:
        for plan in list(self.risk.open_positions.values()):
            ticker = self.exchange_manager.fetch_ticker(plan.exchange, plan.symbol)
            if not ticker:
                continue
            current_price = ticker.get("last") or ticker.get("close")
            if not current_price:
                continue

            exit_reason = self.risk.check_exit(plan, float(current_price))
            if not exit_reason:
                continue

            self.executor.close_position(plan)
            pnl = self.risk.register_close(plan, float(current_price))

            if plan.trade_id is not None:
                self.store.record_close(
                    plan.trade_id, dt.datetime.utcnow().isoformat(), float(current_price), exit_reason, pnl,
                )

            logger.info(
                "Closed %s %s on %s (%s) @ %.6f, pnl=%.2f",
                plan.direction, plan.symbol, plan.exchange, exit_reason, current_price, pnl,
            )
            self.notifier.send(
                f"✅ Closed {plan.direction.upper()} {plan.symbol} on {plan.exchange} "
                f"({exit_reason}) @ {current_price:.6f} | PnL: {pnl:.2f}"
            )

    def _act_on_setups(self, setups: list[signal_engine.TradeSetup]) -> None:
        for setup in setups:
            plan = self.risk.build_position_plan(
                exchange=setup.exchange,
                symbol=setup.symbol,
                direction=setup.direction,
                entry_price=setup.current_price,
            )
            if not plan:
                continue

            self.executor.open_position(plan)
            plan.trade_id = self.store.record_open(
                opened_at=dt.datetime.utcnow().isoformat(),
                exchange=plan.exchange,
                symbol=plan.symbol,
                strategy=f"fvg_{setup.timeframe}",
                direction=plan.direction,
                entry_price=plan.entry_price,
                size_base=plan.size_base,
                size_quote=plan.size_quote,
                stop_loss=plan.stop_loss,
                take_profit=plan.take_profit,
            )
            self.risk.register_open(plan)

            logger.info("Opened position: %s", setup)
            self.notifier.send(
                f"\U0001F680 New {plan.direction.upper()} {plan.symbol} on {plan.exchange} "
                f"@ {plan.entry_price:.6f} (score {setup.score:.1f}%, SL {plan.stop_loss:.6f}, "
                f"TP {plan.take_profit:.6f}, R:R {plan.risk_reward_ratio:.2f})"
            )
