"""Telegram notifications for the trading bot.

Reuses the same TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID environment
variables as the rest of LUMIAION. If they aren't configured,
notifications are simply logged instead of sent.
"""
from __future__ import annotations

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: Optional[str], chat_id: Optional[str]):
        self.token = token
        self.chat_id = chat_id
        self.enabled = bool(token and chat_id)

    def send(self, text: str) -> None:
        if not self.enabled:
            logger.info("[notify] %s", text)
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            response = requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=10)
            if response.status_code != 200:
                logger.warning("Telegram notification failed: %s %s", response.status_code, response.text)
        except requests.RequestException:
            logger.exception("Failed to send Telegram notification")
