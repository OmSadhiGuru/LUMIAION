"""Le système Chakra de Soma V1 — 7 chakras, 12 centres énergétiques
étendus et 24 portes de chakra.

Ce module est la carte énergétique propriétaire de Soma V1 Virtual. Les
noms sanskrits/anglais traditionnels sont conservés (usage courant en
spiritualité), tandis que les thèmes, mots-clés et affirmations sont en
français. Les fréquences (Hz) et couleurs (hex) forment le "spectre" combiné
avec la lecture Schumann pour chaque rapport.

Tout est conçu pour être facilement modifiable : ajuste simplement les
dictionnaires ci-dessous pour adapter les noms ou significations à ta
propre charte.
"""

from .numerology import reduce_number

# ---------------------------------------------------------------------------
# 7 Chakras classiques
# ---------------------------------------------------------------------------

CHAKRAS_7 = [
    {
        "number": 1,
        "name": "Racine",
        "sanskrit": "Muladhara",
        "color_name": "Rouge Rubis",
        "color_hex": "#C0392B",
        "frequency_hz": 396,
        "keyword": "Stabilité & Survie",
        "theme": "Ancrage, sécurité, lien à la Terre.",
        "affirmation": "Je suis enraciné(e), en sécurité, et soutenu(e) par la Terre.",
    },
    {
        "number": 2,
        "name": "Sacré",
        "sanskrit": "Svadhisthana",
        "color_name": "Orange Ambré",
        "color_hex": "#E67E22",
        "frequency_hz": 417,
        "keyword": "Créativité & Flux",
        "theme": "Émotions, plaisir, créativité, mouvement.",
        "affirmation": "Je laisse mes émotions et ma créativité circuler librement.",
    },
    {
        "number": 3,
        "name": "Plexus Solaire",
        "sanskrit": "Manipura",
        "color_name": "Jaune Doré",
        "color_hex": "#F1C40F",
        "frequency_hz": 528,
        "keyword": "Volonté & Transformation",
        "theme": "Pouvoir personnel, confiance, transformation.",
        "affirmation": "Ma volonté intérieure est claire, puissante et alignée.",
    },
    {
        "number": 4,
        "name": "Cœur",
        "sanskrit": "Anahata",
        "color_name": "Vert Émeraude",
        "color_hex": "#27AE60",
        "frequency_hz": 639,
        "keyword": "Amour & Connexion",
        "theme": "Compassion, relations, équilibre du cœur.",
        "affirmation": "J'ouvre mon cœur à l'amour, donné et reçu.",
    },
    {
        "number": 5,
        "name": "Gorge",
        "sanskrit": "Vishuddha",
        "color_name": "Bleu Saphir",
        "color_hex": "#2980B9",
        "frequency_hz": 741,
        "keyword": "Expression & Vérité",
        "theme": "Communication, vérité, expression authentique.",
        "affirmation": "Je m'exprime avec clarté et vérité.",
    },
    {
        "number": 6,
        "name": "Troisième Œil",
        "sanskrit": "Ajna",
        "color_name": "Indigo",
        "color_hex": "#6C3483",
        "frequency_hz": 852,
        "keyword": "Intuition & Vision",
        "theme": "Perception intérieure, intuition, clarté mentale.",
        "affirmation": "Je fais confiance à ma vision intérieure et à mon intuition.",
    },
    {
        "number": 7,
        "name": "Couronne",
        "sanskrit": "Sahasrara",
        "color_name": "Violet",
        "color_hex": "#8E44AD",
        "frequency_hz": 963,
        "keyword": "Unité & Transcendance",
        "theme": "Connexion spirituelle, conscience supérieure, unité.",
        "affirmation": "Je suis connecté(e) à la Source et à la conscience universelle.",
    },
]

# ---------------------------------------------------------------------------
# 12 Centres énergétiques étendus (de l'Étoile de la Terre au Portail Universel)
# ---------------------------------------------------------------------------

CHAKRAS_12 = [
    {
        "number": 1,
        "name": "Étoile de la Terre",
        "sanskrit": "Earth Star",
        "color_name": "Brun Obsidienne",
        "color_hex": "#3E2723",
        "frequency_hz": 174,
        "keyword": "Ancrage & Mémoire Ancestrale",
        "theme": "Racines profondes dans la Terre, héritage et lignée.",
    },
    {
        "number": 2,
        "name": "Racine",
        "sanskrit": "Muladhara",
        "color_name": "Rouge Rubis",
        "color_hex": "#C0392B",
        "frequency_hz": 396,
        "keyword": "Stabilité & Survie",
        "theme": "Ancrage, sécurité, lien à la Terre.",
    },
    {
        "number": 3,
        "name": "Sacré",
        "sanskrit": "Svadhisthana",
        "color_name": "Orange Ambré",
        "color_hex": "#E67E22",
        "frequency_hz": 417,
        "keyword": "Créativité & Flux",
        "theme": "Émotions, plaisir, créativité, mouvement.",
    },
    {
        "number": 4,
        "name": "Plexus Solaire",
        "sanskrit": "Manipura",
        "color_name": "Jaune Doré",
        "color_hex": "#F1C40F",
        "frequency_hz": 528,
        "keyword": "Volonté & Transformation",
        "theme": "Pouvoir personnel, confiance, transformation.",
    },
    {
        "number": 5,
        "name": "Cœur",
        "sanskrit": "Anahata",
        "color_name": "Vert Émeraude",
        "color_hex": "#27AE60",
        "frequency_hz": 639,
        "keyword": "Amour & Connexion",
        "theme": "Compassion, relations, équilibre du cœur.",
    },
    {
        "number": 6,
        "name": "Cœur Supérieur (Thymus)",
        "sanskrit": "Higher Heart",
        "color_name": "Rose Quartz",
        "color_hex": "#F1948A",
        "frequency_hz": 285,
        "keyword": "Guérison du Cœur & Amour Inconditionnel",
        "theme": "Pardon, régénération, compassion sans limites.",
    },
    {
        "number": 7,
        "name": "Gorge",
        "sanskrit": "Vishuddha",
        "color_name": "Bleu Saphir",
        "color_hex": "#2980B9",
        "frequency_hz": 741,
        "keyword": "Expression & Vérité",
        "theme": "Communication, vérité, expression authentique.",
    },
    {
        "number": 8,
        "name": "Troisième Œil",
        "sanskrit": "Ajna",
        "color_name": "Indigo",
        "color_hex": "#6C3483",
        "frequency_hz": 852,
        "keyword": "Intuition & Vision",
        "theme": "Perception intérieure, intuition, clarté mentale.",
    },
    {
        "number": 9,
        "name": "Couronne",
        "sanskrit": "Sahasrara",
        "color_name": "Violet",
        "color_hex": "#8E44AD",
        "frequency_hz": 963,
        "keyword": "Unité & Transcendance",
        "theme": "Connexion spirituelle, conscience supérieure, unité.",
    },
    {
        "number": 10,
        "name": "Étoile de l'Âme",
        "sanskrit": "Soul Star",
        "color_name": "Magenta-Blanc",
        "color_hex": "#E8DAEF",
        "frequency_hz": 1074,
        "keyword": "Mémoire de l'Âme & Plan Divin",
        "theme": "Sagesse akashique, mémoire des vies, plan d'âme.",
    },
    {
        "number": 11,
        "name": "Portail Stellaire",
        "sanskrit": "Stellar Gateway",
        "color_name": "Or Platine",
        "color_hex": "#D4AC0D",
        "frequency_hz": 1185,
        "keyword": "Lignée Cosmique & Sagesse Stellaire",
        "theme": "Connexion aux origines stellaires et à la sagesse galactique.",
    },
    {
        "number": 12,
        "name": "Portail Universel",
        "sanskrit": "Universal Gateway",
        "color_name": "Iridescent / Arc-en-ciel",
        "color_hex": "#ECECEC",
        "frequency_hz": 1296,
        "keyword": "Unité Source & Champ Infini",
        "theme": "Fusion avec la Source, unité, champ de conscience infini.",
    },
]

# ---------------------------------------------------------------------------
# 24 Portes de Chakra — chaque centre des 12 chakras porte une Porte
# Réceptrice (impair) et une Porte Rayonnante (pair)
# ---------------------------------------------------------------------------

_GATE_NAMES = [
    ("Porte de la Mémoire Ancestrale", "Réceptrice", "Recevoir la sagesse ancrée de la Terre et de la lignée."),
    ("Porte de la Présence Ancrée", "Rayonnante", "Rayonner la stabilité dans ton environnement."),
    ("Porte de la Sécurité", "Réceptrice", "Recevoir un sentiment profond de sécurité."),
    ("Porte de l'Incarnation", "Rayonnante", "Rayonner une confiance ancrée dans le corps."),
    ("Porte de la Sensation", "Réceptrice", "Recevoir le plaisir, le ressenti, le flux."),
    ("Porte du Flux Créatif", "Rayonnante", "Rayonner l'expression créative."),
    ("Porte du Feu Intérieur", "Réceptrice", "Recevoir le pouvoir personnel."),
    ("Porte de la Volonté", "Rayonnante", "Rayonner une action confiante."),
    ("Porte de la Compassion", "Réceptrice", "Recevoir l'amour."),
    ("Porte du Cœur Ouvert", "Rayonnante", "Rayonner l'amour vers l'extérieur."),
    ("Porte du Pardon", "Réceptrice", "Recevoir la guérison du cœur."),
    ("Porte de l'Amour Inconditionnel", "Rayonnante", "Rayonner la compassion universelle."),
    ("Porte de l'Écoute", "Réceptrice", "Recevoir la vérité."),
    ("Porte de la Voix", "Rayonnante", "Rayonner l'expression authentique."),
    ("Porte de la Vision Intérieure", "Réceptrice", "Recevoir la vision intérieure."),
    ("Porte de la Clarté", "Rayonnante", "Rayonner une perception claire."),
    ("Porte de la Connexion Divine", "Réceptrice", "Recevoir la guidance supérieure."),
    ("Porte de l'Illumination", "Rayonnante", "Rayonner la lumière spirituelle."),
    ("Porte de la Mémoire de l'Âme", "Réceptrice", "Recevoir la sagesse akashique et des vies antérieures."),
    ("Porte du Plan Divin", "Rayonnante", "Rayonner le but de l'âme."),
    ("Porte de la Lignée Cosmique", "Réceptrice", "Recevoir la sagesse stellaire."),
    ("Porte de la Transmission Galactique", "Rayonnante", "Rayonner des codes de lumière cosmiques."),
    ("Porte de l'Unité Source", "Réceptrice", "Recevoir l'unité."),
    ("Porte du Champ Infini", "Rayonnante", "Rayonner la conscience d'unité."),
]


def _build_gates_24():
    gates = []
    for index, (name, polarity, theme) in enumerate(_GATE_NAMES, start=1):
        chakra12 = CHAKRAS_12[(index - 1) // 2]
        gates.append({
            "number": index,
            "name": name,
            "polarity": polarity,
            "theme": theme,
            "chakra_12": chakra12["name"],
            "chakra_12_number": chakra12["number"],
        })
    return gates


CHAKRA_GATES_24 = _build_gates_24()


# ---------------------------------------------------------------------------
# Sélecteurs — relient la numérologie du jour/semaine/mois aux 3 systèmes
# ---------------------------------------------------------------------------

def select_chakra_7(value: int) -> dict:
    """Choisit l'un des 7 chakras à partir d'un nombre (numérologie)."""
    reduced = reduce_number(value, keep_master=False)
    index = ((reduced - 1) % 7)
    return CHAKRAS_7[index]


def select_chakra_12(value: int) -> dict:
    """Choisit l'un des 12 centres énergétiques à partir d'un nombre entier."""
    index = (value - 1) % 12
    return CHAKRAS_12[index]


def select_gate_24(value: int) -> dict:
    """Choisit l'une des 24 portes de chakra à partir d'un nombre entier."""
    index = (value - 1) % 24
    return CHAKRA_GATES_24[index]


def get_chakra_12_by_number(number: int) -> dict:
    return CHAKRAS_12[(number - 1) % 12]


def get_gate_24_by_number(number: int) -> dict:
    return CHAKRA_GATES_24[(number - 1) % 24]
