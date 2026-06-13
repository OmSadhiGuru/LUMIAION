#!/usr/bin/env python3
"""Génère la prévision cosmique Soma V1 Virtual et l'envoie sur Telegram.

Utilisé par le workflow GitHub Actions planifié
(`.github/workflows/cosmic-forecast.yml`).

Usage :
    python send_telegram_forecast.py <daily|weekly|monthly>

Variables d'environnement :
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID — si l'une des deux est absente,
    la génération a tout de même lieu (et est commitée dans
    cosmic_reports/), mais l'envoi Telegram est simplement ignoré.
"""

import os
import sys

import requests

from soma_v1_virtual import generate_cosmic_forecast

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def main():
    period = sys.argv[1] if len(sys.argv) > 1 else "daily"

    result = generate_cosmic_forecast(period=period)
    print(f"✅ {period} -> {result['output_dir']}")

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("ℹ️ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID non configurés — envoi Telegram ignoré.")
        return

    response = requests.post(
        TELEGRAM_API.format(token=token),
        json={"chat_id": chat_id, "text": result["facebook_post"]},
        timeout=15,
    )
    response.raise_for_status()
    print("📬 Prévision envoyée sur Telegram.")


if __name__ == "__main__":
    main()
