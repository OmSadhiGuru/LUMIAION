"""Récupération des données de prix (API publique Kraken, sans clé)."""

import requests

KRAKEN_OHLC_URL = "https://api.kraken.com/0/public/OHLC"


def fetch_ohlc(pair: str, interval: int = 60, timeout: int = 10) -> list:
    """Récupère l'historique OHLC pour une paire Kraken (ex: "BTCUSDT",
    "PAXGUSD") avec un intervalle en minutes.

    Retourne une liste de dicts triés du plus ancien au plus récent :
    {"time": <epoch>, "open", "high", "low", "close", "volume"}.
    """
    response = requests.get(
        KRAKEN_OHLC_URL, params={"pair": pair, "interval": interval}, timeout=timeout
    )
    response.raise_for_status()
    payload = response.json()

    errors = payload.get("error") or []
    if errors:
        raise RuntimeError(f"Kraken API error for {pair}: {', '.join(errors)}")

    result = dict(payload.get("result", {}))
    result.pop("last", None)
    if not result:
        raise RuntimeError(f"No OHLC data returned by Kraken for {pair}")

    rows = next(iter(result.values()))
    return [
        {
            "time": int(row[0]),
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "volume": float(row[6]),
        }
        for row in rows
    ]
