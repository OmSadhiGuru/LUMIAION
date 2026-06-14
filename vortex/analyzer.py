"""Analyse des prix et génération des signaux d'achat."""

import datetime

from . import indicators
from .data_sources import fetch_ohlc

ASSETS = [
    {
        "id": "btc",
        "label": "BTC/USDT",
        "name": "Bitcoin",
        "kraken_pair": "BTCUSDT",
        "note": "Données Kraken (BTC/USDT, bougies horaires).",
    },
    {
        "id": "gold",
        "label": "OR (XAU/USD)",
        "name": "Or",
        "kraken_pair": "PAXGUSD",
        "note": (
            "Données Kraken pour PAX Gold (PAXG/USD), jeton adossé 1:1 à "
            "une once d'or fin — utilisé comme proxy temps réel du cours "
            "spot XAU/USD."
        ),
    },
]

DAY_NAMES_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

HISTORY_HOURS = 24 * 7  # 7 jours de bougies horaires pour le graphique
ZSCORE_WINDOW = 24      # fenêtre glissante de 24h pour l'analyse de saisonnalité


def _signal(price, rsi14, bb, sma20):
    if rsi14 is None or bb is None or sma20 is None:
        return {
            "label": "Données insuffisantes",
            "level": "neutral",
            "reason": "Historique trop court pour calculer les indicateurs.",
        }

    near_lower_band = price <= bb["lower"] * 1.01
    near_upper_band = price >= bb["upper"] * 0.99

    if rsi14 <= 30 and near_lower_band:
        return {
            "label": "Achat fort",
            "level": "strong-buy",
            "reason": (
                f"RSI à {rsi14:.0f} (survente) et prix proche de la bande "
                "basse de Bollinger : zone de repli marquée."
            ),
        }
    if rsi14 <= 40 or price < sma20:
        return {
            "label": "Achat",
            "level": "buy",
            "reason": (
                f"RSI à {rsi14:.0f} et/ou prix sous sa moyenne mobile 20h : "
                "repli potentiellement intéressant."
            ),
        }
    if rsi14 >= 70 and near_upper_band:
        return {
            "label": "Surachat — Prudence",
            "level": "avoid",
            "reason": (
                f"RSI à {rsi14:.0f} (surachat) et prix proche de la bande "
                "haute de Bollinger : mieux vaut attendre un repli."
            ),
        }
    if rsi14 >= 60:
        return {
            "label": "Attendre",
            "level": "wait",
            "reason": f"RSI à {rsi14:.0f} : pas de signal de repli marqué pour l'instant.",
        }
    return {
        "label": "Neutre",
        "level": "neutral",
        "reason": f"RSI à {rsi14:.0f} : prix proche de sa zone médiane.",
    }


def _best_buy_windows(ohlc):
    closes = [row["close"] for row in ohlc]
    scores = indicators.rolling_zscore(closes, ZSCORE_WINDOW)

    hour_buckets = {h: [] for h in range(24)}
    day_buckets = {d: [] for d in range(7)}

    for row, score in zip(ohlc, scores):
        if score is None:
            continue
        moment = datetime.datetime.utcfromtimestamp(row["time"])
        hour_buckets[moment.hour].append(score)
        day_buckets[moment.weekday()].append(score)

    hour_avg = {h: sum(v) / len(v) for h, v in hour_buckets.items() if v}
    day_avg = {d: sum(v) / len(v) for d, v in day_buckets.items() if v}

    best_hours = sorted(hour_avg, key=hour_avg.get)[:3]
    best_days = sorted(day_avg, key=day_avg.get)[:2]

    return {
        "best_hours_utc": best_hours,
        "best_days": [DAY_NAMES_FR[d] for d in best_days],
    }


def analyze_asset(config):
    ohlc = fetch_ohlc(config["kraken_pair"])
    closes = [row["close"] for row in ohlc]

    price = closes[-1]
    rsi14 = indicators.rsi(closes, 14)
    sma20 = indicators.sma(closes, 20)
    sma50 = indicators.sma(closes, 50)
    bb = indicators.bollinger_bands(closes, 20, 2)
    change_24h = (
        (closes[-1] - closes[-25]) / closes[-25] * 100 if len(closes) > 25 else None
    )

    windows = _best_buy_windows(ohlc)

    return {
        "id": config["id"],
        "label": config["label"],
        "name": config["name"],
        "note": config["note"],
        "price": price,
        "change_24h_pct": change_24h,
        "rsi14": rsi14,
        "sma20": sma20,
        "sma50": sma50,
        "bollinger": bb,
        "signal": _signal(price, rsi14, bb, sma20),
        "best_hours_utc": windows["best_hours_utc"],
        "best_days": windows["best_days"],
        "history": [
            {"time": row["time"], "close": row["close"]} for row in ohlc[-HISTORY_HOURS:]
        ],
    }


def get_dashboard_data():
    """Retourne les données d'analyse pour tous les actifs suivis.

    Chaque actif est analysé indépendamment : si la récupération des prix
    échoue pour l'un d'eux, son entrée contient une clé "error" plutôt que
    de faire échouer l'ensemble du tableau de bord.
    """
    assets = []
    for config in ASSETS:
        try:
            assets.append(analyze_asset(config))
        except Exception as exc:
            assets.append({
                "id": config["id"],
                "label": config["label"],
                "name": config["name"],
                "note": config["note"],
                "error": str(exc),
            })

    return {
        "generated_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "assets": assets,
    }
