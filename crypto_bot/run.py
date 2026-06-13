"""Entry point for the LUMIAION crypto trading bot.

Usage:
    python -m crypto_bot.run            # run continuously
    python -m crypto_bot.run --once     # run a single cycle (useful for testing)
"""
from __future__ import annotations

import argparse
import logging

from .bot import CryptoBot
from .config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description="LUMIAION crypto trading bot")
    parser.add_argument("--once", action="store_true", help="run a single cycle and exit")
    parser.add_argument("--log-level", default="INFO", help="logging level (default: INFO)")
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = load_config()
    bot = CryptoBot(config)

    if args.once:
        bot.run_cycle()
    else:
        bot.run_forever()


if __name__ == "__main__":
    main()
