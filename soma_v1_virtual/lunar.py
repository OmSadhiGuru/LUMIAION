"""Mouvement lunaire pour Soma V1 Virtual.

Calcule la phase lunaire (âge, illumination, nom de phase) ainsi que le
signe zodiacal approximatif de la Lune, à partir de formules
astronomiques simplifiées (Meeus) — sans dépendance externe.
"""

import math
from datetime import datetime, timedelta, timezone

SYNODIC_MONTH = 29.530588853
REFERENCE_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

ZODIAC_SIGNS_FR = [
    "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
    "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
]

PHASE_NAMES_FR = [
    (0.02, "Nouvelle Lune"),
    (0.24, "Premier Croissant"),
    (0.26, "Premier Quartier"),
    (0.49, "Lune Gibbeuse Croissante"),
    (0.51, "Pleine Lune"),
    (0.74, "Lune Gibbeuse Décroissante"),
    (0.76, "Dernier Quartier"),
    (0.98, "Dernier Croissant"),
    (1.01, "Nouvelle Lune"),
]


def _phase_name(fraction: float) -> str:
    for upper_bound, name in PHASE_NAMES_FR:
        if fraction <= upper_bound:
            return name
    return "Nouvelle Lune"


def _to_julian_day(dt: datetime) -> float:
    dt = dt.astimezone(timezone.utc)
    year, month = dt.year, dt.month
    day = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day
        + b
        - 1524.5
    )


def moon_ecliptic_longitude(dt: datetime) -> float:
    """Longitude écliptique géocentrique approximative de la Lune (degrés),
    via les termes périodiques dominants de la théorie lunaire de Meeus
    (précision approximative de quelques dixièmes de degré)."""
    jd = _to_julian_day(dt)
    t = (jd - 2451545.0) / 36525.0

    l_prime = 218.3164477 + 481267.88123421 * t
    d = 297.8501921 + 445267.1114034 * t
    m = 357.5291092 + 35999.0502909 * t
    m_prime = 134.9633964 + 477198.8675055 * t
    f = 93.2720950 + 483202.0175233 * t

    def rad(deg: float) -> float:
        return math.radians(deg % 360)

    longitude = l_prime
    longitude += 6.288774 * math.sin(rad(m_prime))
    longitude += 1.274027 * math.sin(rad(2 * d - m_prime))
    longitude += 0.658314 * math.sin(rad(2 * d))
    longitude += 0.213618 * math.sin(rad(2 * m_prime))
    longitude -= 0.185116 * math.sin(rad(m))
    longitude -= 0.114332 * math.sin(rad(2 * f))
    longitude += 0.058793 * math.sin(rad(2 * d - 2 * m_prime))
    longitude += 0.057066 * math.sin(rad(2 * d - m - m_prime))
    longitude += 0.053322 * math.sin(rad(2 * d + m_prime))
    longitude += 0.045758 * math.sin(rad(2 * d - m))
    longitude -= 0.040923 * math.sin(rad(m - m_prime))
    longitude -= 0.034720 * math.sin(rad(d))
    longitude -= 0.030383 * math.sin(rad(m + m_prime))

    return longitude % 360


def moon_phase(dt: datetime):
    """Retourne (age_en_jours, fraction_du_cycle, illumination_0_a_1)."""
    days_since = (dt - REFERENCE_NEW_MOON).total_seconds() / 86400
    age = days_since % SYNODIC_MONTH
    fraction = age / SYNODIC_MONTH
    illumination = (1 - math.cos(2 * math.pi * fraction)) / 2
    return age, fraction, illumination


def next_phase_date(dt: datetime, target_fraction: float) -> datetime:
    """Date du prochain passage par une fraction de cycle donnée
    (0.0 = Nouvelle Lune, 0.5 = Pleine Lune)."""
    _, fraction, _ = moon_phase(dt)
    days_ahead = (target_fraction - fraction) % 1.0 * SYNODIC_MONTH
    if days_ahead < 0.05:
        days_ahead += SYNODIC_MONTH
    return dt + timedelta(days=days_ahead)


def get_lunar_snapshot(dt: datetime = None) -> dict:
    """Photo instantanée du mouvement lunaire pour une date/heure donnée
    (UTC par défaut = maintenant)."""
    dt = dt or datetime.now(timezone.utc)
    age, fraction, illumination = moon_phase(dt)
    longitude = moon_ecliptic_longitude(dt)
    sign_index = int(longitude // 30)

    return {
        "datetime_utc": dt.isoformat(),
        "age_days": round(age, 2),
        "cycle_fraction": round(fraction, 4),
        "illumination_pct": round(illumination * 100, 1),
        "phase_name": _phase_name(fraction),
        "zodiac_sign": ZODIAC_SIGNS_FR[sign_index],
        "zodiac_degree": round(longitude % 30, 2),
        "next_new_moon": next_phase_date(dt, 0.0).date().isoformat(),
        "next_full_moon": next_phase_date(dt, 0.5).date().isoformat(),
    }


def get_phase_for_date(d) -> dict:
    """Phase lunaire simplifiée (nom + illumination) pour une date donnée
    (utile pour les progressions hebdomadaires/mensuelles)."""
    dt = datetime(d.year, d.month, d.day, 12, 0, tzinfo=timezone.utc)
    _, fraction, illumination = moon_phase(dt)
    return {
        "date": d.isoformat(),
        "phase_name": _phase_name(fraction),
        "illumination_pct": round(illumination * 100, 1),
    }
