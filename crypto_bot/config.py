"""Configuration for the crypto trading bot.

Everything is driven by environment variables (loaded from a local
`.env` file via python-dotenv if present). API keys/secrets are never
hardcoded - an exchange runs in market-data-only mode if no
credentials are configured for it.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - python-dotenv is optional at import time
    pass


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _env_float(name: str, default: float) -> float:
    val = os.getenv(name)
    return float(val) if val else default


def _env_int(name: str, default: int) -> int:
    val = os.getenv(name)
    return int(val) if val else default


def _env_list(name: str, default: list[str]) -> list[str]:
    val = os.getenv(name)
    if not val:
        return list(default)
    return [item.strip() for item in val.split(",") if item.strip()]


@dataclass
class ExchangeConfig:
    """Credentials and toggle for a single ccxt exchange."""

    id: str  # ccxt exchange id, e.g. "kraken", "coinbase", "kucoin", "bybit"
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    password: Optional[str] = None  # passphrase, required by kucoin/coinbase
    enabled: bool = True

    @property
    def can_trade(self) -> bool:
        return bool(self.api_key and self.api_secret)


def _load_exchange(exchange_id: str, env_prefix: str) -> ExchangeConfig:
    return ExchangeConfig(
        id=exchange_id,
        api_key=os.getenv(f"{env_prefix}_API_KEY"),
        api_secret=os.getenv(f"{env_prefix}_API_SECRET"),
        password=os.getenv(f"{env_prefix}_PASSWORD"),
        enabled=_env_bool(f"{env_prefix}_ENABLED", True),
    )


@dataclass
class RiskConfig:
    """Portfolio-level risk limits. All values are percentages."""

    max_risk_per_trade_pct: float = 1.0   # equity risked (stop-loss distance) per trade
    max_position_pct: float = 20.0        # max equity allocated to a single position
    max_open_positions: int = 5
    max_daily_loss_pct: float = 5.0       # circuit breaker: halt new trades for the day
    default_stop_loss_pct: float = 2.0
    default_take_profit_pct: float = 4.0
    min_risk_reward_ratio: float = 1.5


@dataclass
class ArbitrageConfig:
    """Cross-exchange arbitrage scanner thresholds."""

    min_spread_pct: float = 0.5    # minimum *net* spread (after both taker fees) to flag
    taker_fee_pct: float = 0.1     # estimated taker fee per leg, used to net out the spread
    max_position_usd: float = 500.0


@dataclass
class FVGConfig:
    """Fair Value Gap / signal-engine parameters."""

    timeframes_short: list[str] = field(default_factory=lambda: ["15m", "1h"])
    timeframes_long: list[str] = field(default_factory=lambda: ["4h", "1d"])
    min_gap_pct: float = 0.05      # minimum gap size (% of price) to be considered an FVG
    lookback_candles: int = 200


@dataclass
class BotConfig:
    exchanges: list[ExchangeConfig]
    pairs: list[str]
    risk: RiskConfig
    arbitrage: ArbitrageConfig
    fvg: FVGConfig
    poll_interval_seconds: int
    live_trading: bool
    starting_equity: float
    telegram_token: Optional[str]
    telegram_chat_id: Optional[str]
    db_path: str


# Exchanges chosen for arbitrage between "high market value" venues
# (Coinbase, Kraken) and "low market value" venues (KuCoin, Bybit) where
# spreads on altcoins tend to be wider.
SUPPORTED_EXCHANGES = [
    ("kraken", "KRAKEN"),
    ("coinbase", "COINBASE"),
    ("kucoin", "KUCOIN"),
    ("bybit", "BYBIT"),
]

DEFAULT_PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ARB/USDT", "INJ/USDT"]


def load_config() -> BotConfig:
    exchanges = [_load_exchange(ex_id, prefix) for ex_id, prefix in SUPPORTED_EXCHANGES]
    exchanges = [ex for ex in exchanges if ex.enabled]

    live_trading = _env_bool("ENABLE_LIVE_TRADING", False)

    return BotConfig(
        exchanges=exchanges,
        pairs=_env_list("TRADING_PAIRS", DEFAULT_PAIRS),
        risk=RiskConfig(
            max_risk_per_trade_pct=_env_float("MAX_RISK_PER_TRADE_PCT", 1.0),
            max_position_pct=_env_float("MAX_POSITION_PCT", 20.0),
            max_open_positions=_env_int("MAX_OPEN_POSITIONS", 5),
            max_daily_loss_pct=_env_float("MAX_DAILY_LOSS_PCT", 5.0),
            default_stop_loss_pct=_env_float("DEFAULT_STOP_LOSS_PCT", 2.0),
            default_take_profit_pct=_env_float("DEFAULT_TAKE_PROFIT_PCT", 4.0),
            min_risk_reward_ratio=_env_float("MIN_RISK_REWARD_RATIO", 1.5),
        ),
        arbitrage=ArbitrageConfig(
            min_spread_pct=_env_float("ARBITRAGE_MIN_SPREAD_PCT", 0.5),
            taker_fee_pct=_env_float("TAKER_FEE_PCT", 0.1),
            max_position_usd=_env_float("ARBITRAGE_MAX_POSITION_USD", 500.0),
        ),
        fvg=FVGConfig(
            timeframes_short=_env_list("FVG_TIMEFRAMES_SHORT", ["15m", "1h"]),
            timeframes_long=_env_list("FVG_TIMEFRAMES_LONG", ["4h", "1d"]),
            min_gap_pct=_env_float("FVG_MIN_GAP_PCT", 0.05),
            lookback_candles=_env_int("FVG_LOOKBACK_CANDLES", 200),
        ),
        poll_interval_seconds=_env_int("POLL_INTERVAL_SECONDS", 60),
        live_trading=live_trading,
        starting_equity=_env_float("STARTING_EQUITY", 10_000.0),
        telegram_token=os.getenv("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        db_path=os.getenv("CRYPTO_BOT_DB_PATH", "crypto_bot/data/trades.db"),
    )
