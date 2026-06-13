"""Multi-exchange connectivity layer built on top of ccxt."""
from __future__ import annotations

import logging
from typing import Optional

import ccxt

from .config import ExchangeConfig

logger = logging.getLogger(__name__)


class ExchangeManager:
    """Holds initialized ccxt exchange clients and provides safe wrappers.

    Exchanges without API credentials are still initialized for public
    market-data access (tickers, OHLCV) so the arbitrage scanner and
    signal engine work even before keys are configured; only order
    placement requires credentials.
    """

    def __init__(self, exchange_configs: list[ExchangeConfig]):
        self.clients: dict[str, ccxt.Exchange] = {}
        self.tradable: dict[str, bool] = {}

        for cfg in exchange_configs:
            try:
                exchange_class = getattr(ccxt, cfg.id)
            except AttributeError:
                logger.error("Unknown ccxt exchange id: %s", cfg.id)
                continue

            params: dict = {"enableRateLimit": True}
            if cfg.can_trade:
                params["apiKey"] = cfg.api_key
                params["secret"] = cfg.api_secret
                if cfg.password:
                    params["password"] = cfg.password

            self.clients[cfg.id] = exchange_class(params)
            self.tradable[cfg.id] = cfg.can_trade
            logger.info(
                "Initialized %s (%s)",
                cfg.id,
                "trading enabled" if cfg.can_trade else "market data only",
            )

    def exchange_ids(self) -> list[str]:
        return list(self.clients.keys())

    def can_trade(self, exchange_id: str) -> bool:
        return self.tradable.get(exchange_id, False)

    def fetch_ticker(self, exchange_id: str, symbol: str) -> Optional[dict]:
        client = self.clients[exchange_id]
        try:
            return client.fetch_ticker(symbol)
        except Exception:
            logger.exception("Failed to fetch ticker %s on %s", symbol, exchange_id)
            return None

    def fetch_ohlcv(self, exchange_id: str, symbol: str, timeframe: str,
                     limit: int = 200) -> Optional[list]:
        client = self.clients[exchange_id]
        try:
            return client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception:
            logger.exception("Failed to fetch OHLCV %s %s on %s", symbol, timeframe, exchange_id)
            return None

    def fetch_balance(self, exchange_id: str) -> Optional[dict]:
        if not self.can_trade(exchange_id):
            return None
        client = self.clients[exchange_id]
        try:
            return client.fetch_balance()
        except Exception:
            logger.exception("Failed to fetch balance on %s", exchange_id)
            return None

    def create_order(self, exchange_id: str, symbol: str, side: str, amount: float,
                      order_type: str = "market", price: Optional[float] = None,
                      params: Optional[dict] = None) -> dict:
        if not self.can_trade(exchange_id):
            raise RuntimeError(f"Exchange '{exchange_id}' has no API credentials configured")
        client = self.clients[exchange_id]
        return client.create_order(symbol, order_type, side, amount, price, params or {})

    def symbol_supported(self, exchange_id: str, symbol: str) -> bool:
        client = self.clients[exchange_id]
        try:
            markets = client.load_markets()
            return symbol in markets
        except Exception:
            logger.exception("Failed to load markets for %s", exchange_id)
            return False
