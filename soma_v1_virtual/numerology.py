"""Numérologie universelle pour Soma V1 Virtual.

Calcule les nombres universels (jour, semaine, mois) à partir du
calendrier — sans nécessiter de date de naissance — et fournit leur
profil énergétique (mot-clé, thème, affirmation).
"""

from datetime import date

MASTER_NUMBERS = (11, 22, 33)

NUMBER_PROFILES = {
    1: {
        "keyword": "Initiation",
        "theme": "Nouveaux départs, leadership, étincelle créatrice brute.",
        "affirmation": "Je plante les graines d'un nouveau départ avec courage.",
    },
    2: {
        "keyword": "Union",
        "theme": "Partenariat, équilibre, intuition, patience.",
        "affirmation": "J'avance en harmonie avec les autres et avec moi-même.",
    },
    3: {
        "keyword": "Expression",
        "theme": "Créativité, communication, joie.",
        "affirmation": "J'exprime ma vérité avec joie et créativité.",
    },
    4: {
        "keyword": "Fondation",
        "theme": "Structure, stabilité, effort ancré.",
        "affirmation": "Je construis ma vie sur une base solide et sacrée.",
    },
    5: {
        "keyword": "Mouvement",
        "theme": "Changement, liberté, aventure.",
        "affirmation": "Je m'adapte au changement et je fais confiance à l'inconnu.",
    },
    6: {
        "keyword": "Harmonie",
        "theme": "Amour, responsabilité, guérison, foyer.",
        "affirmation": "Je prends soin de moi-même et de ceux que j'aime.",
    },
    7: {
        "keyword": "Réflexion",
        "theme": "Introspection, spiritualité, sagesse.",
        "affirmation": "Je fais confiance à la sagesse qui émerge du silence.",
    },
    8: {
        "keyword": "Pouvoir",
        "theme": "Abondance, maîtrise, karma.",
        "affirmation": "J'aligne mon pouvoir avec l'intégrité et l'abondance.",
    },
    9: {
        "keyword": "Achèvement",
        "theme": "Clôture, compassion, amour universel.",
        "affirmation": "Je relâche ce qui est complet, avec gratitude.",
    },
    11: {
        "keyword": "Illumination",
        "theme": "Intuition, vision spirituelle, maître enseignant.",
        "affirmation": "Je suis un canal clair pour la lumière supérieure.",
    },
    22: {
        "keyword": "Bâtisseur Maître",
        "theme": "Manifestation de grandes visions en structures concrètes.",
        "affirmation": "Je transforme la vision en structure durable.",
    },
    33: {
        "keyword": "Guérisseur Maître",
        "theme": "Service par compassion, enseignement, guérison à grande échelle.",
        "affirmation": "Je suis un vecteur de guérison et de lumière.",
    },
}


def reduce_number(n: int, keep_master: bool = True) -> int:
    """Réduit un nombre à un chiffre unique (1-9), en conservant
    optionnellement les nombres maîtres 11, 22 et 33."""
    while n > 9:
        if keep_master and n in MASTER_NUMBERS:
            return n
        n = sum(int(d) for d in str(n))
    return n


def universal_day_number(d: date) -> int:
    digits = f"{d.year}{d.month:02d}{d.day:02d}"
    total = sum(int(c) for c in digits)
    return reduce_number(total)


def universal_week_number(d: date) -> int:
    iso_year, iso_week, _ = d.isocalendar()
    digits = f"{iso_year}{iso_week:02d}"
    total = sum(int(c) for c in digits)
    return reduce_number(total)


def universal_month_number(d: date) -> int:
    digits = f"{d.year}{d.month:02d}"
    total = sum(int(c) for c in digits)
    return reduce_number(total)


def number_profile(n: int) -> dict:
    """Retourne le profil énergétique d'un nombre universel."""
    profile = NUMBER_PROFILES.get(n)
    if profile is None:
        profile = NUMBER_PROFILES[reduce_number(n, keep_master=False)]
    return {"number": n, **profile}
