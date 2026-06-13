"""Météo spatiale & résonance de Schumann pour Soma V1 Virtual.

Récupère les données publiques NOAA SWPC (activité solaire, indice Kp
géomagnétique, prévision de tempêtes) et calcule une lecture symbolique
de la résonance de Schumann (aucun flux public en direct n'existant pour
celle-ci).
"""

import hashlib
from datetime import datetime, timedelta, timezone

import requests

REQUEST_TIMEOUT = 10

NOAA_KP_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
NOAA_FLARES_URL = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"
NOAA_SCALES_URL = "https://services.swpc.noaa.gov/products/noaa-scales.json"

# --- Activité géomagnétique (indice Kp) -----------------------------------

KP_LEVELS = [
    (0, "Calme", "Champ géomagnétique calme — favorable à la concentration et à une énergie stable."),
    (3, "Instable", "Légères fluctuations — restez ancré(e), une sensibilité mineure est possible."),
    (5, "Actif / Tempête mineure", "Activité géomagnétique accrue — les émotions et le sommeil peuvent être stimulés."),
    (6, "Tempête modérée", "Perturbation géomagnétique notable — ancrage, hydratation et repos recommandés."),
    (8, "Tempête forte à sévère", "Forte perturbation géomagnétique — un ancrage profond et du repos sont fortement conseillés."),
]

G_SCALE_FR = {
    "none": "Aucune",
    "minor": "Mineure",
    "moderate": "Modérée",
    "strong": "Forte",
    "severe": "Sévère",
    "extreme": "Extrême",
}


def _kp_description(kp: float):
    label, note = KP_LEVELS[0][1], KP_LEVELS[0][2]
    for threshold, lvl, n in KP_LEVELS:
        if kp >= threshold:
            label, note = lvl, n
    return label, note


def fetch_geomagnetic_activity() -> dict:
    try:
        resp = requests.get(NOAA_KP_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        latest = data[-1]
        kp = float(latest.get("estimated_kp") or latest.get("kp_index") or 0)
        level, note = _kp_description(kp)
        return {
            "kp_index": round(kp, 2),
            "level": level,
            "interpretation": note,
            "observed_at": latest.get("time_tag"),
            "source": "NOAA SWPC — Indice Kp planétaire (estimation 1 minute)",
        }
    except Exception as exc:
        return {
            "kp_index": None,
            "level": "Indisponible",
            "interpretation": "Les données géomagnétiques en direct sont temporairement inaccessibles.",
            "observed_at": None,
            "source": f"NOAA SWPC (erreur : {exc})",
        }


def fetch_storm_outlook() -> dict:
    try:
        resp = requests.get(NOAA_SCALES_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        today = data.get("0", {})
        g = today.get("G", {}) or {}
        scale = g.get("Scale")
        text = (g.get("Text") or "none").lower()
        return {
            "g_scale": scale,
            "g_level_fr": G_SCALE_FR.get(text, text.capitalize()),
            "date": today.get("DateStamp"),
            "source": "NOAA SWPC — Prévision sur 3 jours (échelles G/S/R)",
        }
    except Exception as exc:
        return {
            "g_scale": None,
            "g_level_fr": "Indisponible",
            "date": None,
            "source": f"NOAA SWPC (erreur : {exc})",
        }


# --- Activité solaire (éruptions à rayons X) -------------------------------

FLARE_CLASS_ORDER = "ABCMX"

FLARE_SUMMARIES_FR = {
    "X": "Forte activité solaire — attendez-vous à une énergie amplifiée, un afflux intense d'inspiration et une possible sensibilité technologique.",
    "M": "Activité solaire modérée — une vague perceptible d'énergie stimulante et de haute fréquence.",
    "C": "Activité solaire légère — une énergie solaire douce qui favorise la clarté et la motivation.",
    "B": "Activité solaire mineure — une légère sous-tonalité solaire en arrière-plan.",
    "A": "Activité solaire très faible — champ solaire calme.",
}

NO_FLARE_SUMMARY_FR = (
    "Aucune éruption solaire significative (classe M ou plus) au cours des "
    "dernières 24 heures. Le champ solaire est stable."
)


def _flare_strength(flare_class: str) -> float:
    if not flare_class:
        return 0.0
    letter = flare_class[0].upper()
    try:
        magnitude = float(flare_class[1:])
    except (ValueError, IndexError):
        magnitude = 0.0
    if letter not in FLARE_CLASS_ORDER:
        return 0.0
    return FLARE_CLASS_ORDER.index(letter) * 10 + magnitude


def _solar_summary(flare_class: str, count: int) -> str:
    letter = (flare_class or "?")[0].upper()
    base = FLARE_SUMMARIES_FR.get(letter, "Activité solaire détectée.")
    return f"{base} ({count} éruption(s) détectée(s), la plus forte : {flare_class})"


def fetch_solar_activity(window_hours: int = 24) -> dict:
    try:
        resp = requests.get(NOAA_FLARES_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        flares = resp.json()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
        recent = []
        for flare in flares:
            try:
                t = datetime.fromisoformat(flare["max_time"].replace("Z", "+00:00"))
            except (KeyError, ValueError, TypeError):
                continue
            if t >= cutoff:
                recent.append(flare)

        if not recent:
            return {
                "flare_count": 0,
                "strongest_class": None,
                "strongest_time": None,
                "summary": NO_FLARE_SUMMARY_FR,
                "source": "NOAA SWPC — Éruptions GOES à rayons X (7 jours)",
            }

        strongest = max(recent, key=lambda f: _flare_strength(f.get("max_class")))
        return {
            "flare_count": len(recent),
            "strongest_class": strongest.get("max_class"),
            "strongest_time": strongest.get("max_time"),
            "summary": _solar_summary(strongest.get("max_class"), len(recent)),
            "source": "NOAA SWPC — Éruptions GOES à rayons X (7 jours)",
        }
    except Exception as exc:
        return {
            "flare_count": None,
            "strongest_class": None,
            "strongest_time": None,
            "summary": "Les données d'activité solaire en direct sont temporairement inaccessibles.",
            "source": f"NOAA SWPC (erreur : {exc})",
        }


# --- Résonance de Schumann (estimation symbolique) -------------------------

SCHUMANN_BASE_HZ = 7.83
SCHUMANN_HARMONICS_HZ = [7.83, 14.3, 20.8, 27.3, 33.8]

SCHUMANN_LEVELS_FR = [
    (0, "Champ Calme", "Le battement de cœur planétaire est stable — favorable à la méditation, au sommeil et à la régénération du système nerveux."),
    (2, "Champ Actif", "Légère activité ionosphérique — l'énergie est alerte et légèrement stimulée."),
    (4, "Champ Élevé", "Activité de résonance accrue — de nombreuses personnes sensibles peuvent se sentir survoltées, émotives, ou avoir des rêves intenses."),
    (6, "Champ Hautement Chargé", "Pics de résonance puissants — attendez-vous à des changements énergétiques intenses, de l'agitation, ou des percées."),
]

SCHUMANN_METHOD_NOTE_FR = (
    "Aucun flux public en direct de la résonance de Schumann n'existe. Soma V1 "
    "calcule donc une lecture symbolique quotidienne basée sur la fréquence "
    "fondamentale de 7.83 Hz et sa série harmonique, modulée par l'indice "
    "géomagnétique Kp du jour (un Kp plus élevé = davantage de perturbation "
    "ionosphérique = une variance de résonance plus large). La lecture est "
    "déterministe pour une date donnée (stable si régénérée) et destinée à un "
    "usage réflexif et de divertissement, non comme un flux scientifique en direct."
)


def estimate_schumann_resonance(reference_date, kp_index: float = None) -> dict:
    seed = int(hashlib.sha256(reference_date.isoformat().encode()).hexdigest(), 16)
    jitter = ((seed % 200) / 100.0) - 1.0  # entre -1.00 et +0.99

    kp = kp_index if kp_index is not None else 2.0
    swing = 0.05 + (kp / 9.0) * 0.6
    estimated_reading = round(SCHUMANN_BASE_HZ + jitter * swing, 2)

    intensity_score = kp + abs(jitter) * 2
    level, note = SCHUMANN_LEVELS_FR[0][1], SCHUMANN_LEVELS_FR[0][2]
    for threshold, lvl, n in SCHUMANN_LEVELS_FR:
        if intensity_score >= threshold:
            level, note = lvl, n

    return {
        "base_frequency_hz": SCHUMANN_BASE_HZ,
        "estimated_reading_hz": estimated_reading,
        "harmonics_hz": SCHUMANN_HARMONICS_HZ,
        "field_intensity": level,
        "interpretation": note,
        "method": SCHUMANN_METHOD_NOTE_FR,
    }
