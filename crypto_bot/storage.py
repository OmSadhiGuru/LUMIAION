"""SQLite-backed trade journal and equity history.

Used to reconstruct monthly P&L, audit every trade the bot opened
(real or simulated), and track the equity curve over time.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opened_at TEXT NOT NULL,
    closed_at TEXT,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    strategy TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry_price REAL NOT NULL,
    exit_price REAL,
    size_base REAL NOT NULL,
    size_quote REAL NOT NULL,
    stop_loss REAL,
    take_profit REAL,
    exit_reason TEXT,
    pnl_quote REAL,
    status TEXT NOT NULL DEFAULT 'open'
);

CREATE TABLE IF NOT EXISTS equity_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    equity REAL NOT NULL
);
"""


class TradeStore:
    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def record_open(self, opened_at: str, exchange: str, symbol: str, strategy: str,
                     direction: str, entry_price: float, size_base: float, size_quote: float,
                     stop_loss: Optional[float], take_profit: Optional[float]) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO trades
                   (opened_at, exchange, symbol, strategy, direction, entry_price,
                    size_base, size_quote, stop_loss, take_profit, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')""",
                (opened_at, exchange, symbol, strategy, direction, entry_price,
                 size_base, size_quote, stop_loss, take_profit),
            )
            return cur.lastrowid

    def record_close(self, trade_id: int, closed_at: str, exit_price: float,
                      exit_reason: str, pnl_quote: float) -> None:
        with self._connect() as conn:
            conn.execute(
                """UPDATE trades
                   SET closed_at = ?, exit_price = ?, exit_reason = ?, pnl_quote = ?, status = 'closed'
                   WHERE id = ?""",
                (closed_at, exit_price, exit_reason, pnl_quote, trade_id),
            )

    def record_equity(self, recorded_at: str, equity: float) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO equity_history (recorded_at, equity) VALUES (?, ?)",
                (recorded_at, equity),
            )

    def monthly_pnl(self) -> list[tuple[str, float]]:
        """Return (YYYY-MM, total pnl) for every month with closed trades."""
        with self._connect() as conn:
            rows = conn.execute(
                """SELECT strftime('%Y-%m', closed_at) AS month, SUM(pnl_quote)
                   FROM trades WHERE status = 'closed'
                   GROUP BY month ORDER BY month"""
            ).fetchall()
        return rows

    def open_trades(self) -> list[sqlite3.Row]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM trades WHERE status = 'open'").fetchall()
