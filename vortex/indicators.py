"""Indicateurs techniques simples (sans dépendance externe)."""


def sma(values, period):
    """Moyenne mobile simple sur les `period` dernières valeurs."""
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def rsi(values, period=14):
    """RSI (Relative Strength Index) de Wilder."""
    if len(values) < period + 1:
        return None

    gains, losses = [], []
    for prev, curr in zip(values, values[1:]):
        change = curr - prev
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for gain, loss in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def bollinger_bands(values, period=20, num_std=2):
    """Bandes de Bollinger (moyenne, bande haute, bande basse) sur les
    `period` dernières valeurs."""
    if len(values) < period:
        return None

    window = values[-period:]
    mean = sum(window) / period
    variance = sum((x - mean) ** 2 for x in window) / period
    std = variance ** 0.5

    return {
        "mid": mean,
        "upper": mean + num_std * std,
        "lower": mean - num_std * std,
        "std": std,
    }


def rolling_zscore(values, window=24):
    """Z-score de chaque valeur par rapport aux `window` valeurs précédentes.

    `None` pour les indices sans historique suffisant.
    """
    scores = [None] * len(values)
    for i in range(window, len(values)):
        segment = values[i - window:i]
        mean = sum(segment) / window
        variance = sum((x - mean) ** 2 for x in segment) / window
        std = variance ** 0.5
        scores[i] = (values[i] - mean) / std if std > 0 else 0.0
    return scores
