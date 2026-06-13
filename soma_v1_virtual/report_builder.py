"""Construction et mise en forme des rapports Soma V1 Virtual.

Combine la résonance de Schumann, l'activité solaire et géomagnétique,
le mouvement lunaire, la numérologie et le système des chakras (7 / 12 /
24 portes) en un seul rapport "spectre complet", puis le met en forme en
plusieurs formats prêts à publier (Facebook, Instagram, rapport complet).
"""

from datetime import date, datetime, timedelta, timezone

from . import chakra_system, lunar, numerology, space_weather

AGENT_NAME = "Soma V1 Virtual"

MONTH_NAMES_FR = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]

DISCLAIMER_FR = (
    "✨ Soma V1 Virtual — Prévision Cosmique à but de divertissement et de "
    "réflexion personnelle. Les données scientifiques (activité solaire et "
    "géomagnétique) proviennent de NOAA SWPC. Les éléments numérologiques, "
    "lunaires symboliques, chakras et fréquences relèvent d'une lecture "
    "énergétique/spirituelle et ne remplacent aucun avis médical, "
    "scientifique ou professionnel."
)

BASE_HASHTAGS = [
    "#SomaV1Virtual", "#CosmicForecast", "#PrevisionCosmique", "#Spiritualite",
    "#Chakras", "#Numerologie", "#FrequencesSacrees", "#EnergieDuJour",
]

EXTRA_HASHTAGS = [
    "#SchumannResonance", "#ActiviteSolaire", "#Lune", "#Eveil",
    "#ConscienceCosmique", "#Lumiaion",
]

PERIOD_HASHTAGS = {
    "daily": "#PrevisionDuJour",
    "weekly": "#PrevisionDeLaSemaine",
    "monthly": "#PrevisionDuMois",
}


# ---------------------------------------------------------------------------
# Construction des rapports
# ---------------------------------------------------------------------------

def _gather_space_weather(reference_date):
    geo = space_weather.fetch_geomagnetic_activity()
    solar = space_weather.fetch_solar_activity()
    storm = space_weather.fetch_storm_outlook()
    schumann = space_weather.estimate_schumann_resonance(
        reference_date, kp_index=geo.get("kp_index")
    )
    return solar, geo, storm, schumann


def _build_spectrum(chakras, schumann):
    frequencies = list(schumann["harmonics_hz"]) + [schumann["estimated_reading_hz"]]
    colors = []
    for chakra in chakras:
        if chakra["frequency_hz"] not in frequencies:
            frequencies.append(chakra["frequency_hz"])
        colors.append({
            "name": chakra["color_name"],
            "hex": chakra["color_hex"],
            "source": chakra["name"],
        })
    return {
        "frequencies_hz": sorted(set(frequencies)),
        "colors": colors,
    }


def build_daily_report(reference_date: date = None) -> dict:
    reference_date = reference_date or date.today()
    now = datetime.now(timezone.utc)

    solar, geo, storm, schumann = _gather_space_weather(reference_date)
    lunar_snapshot = lunar.get_lunar_snapshot(now)

    universal_day = numerology.universal_day_number(reference_date)
    num_profile = numerology.number_profile(universal_day)

    ordinal = reference_date.toordinal()
    chakra7 = chakra_system.select_chakra_7(universal_day)
    chakra12 = chakra_system.select_chakra_12(ordinal)
    gate24 = chakra_system.select_gate_24(ordinal)

    spectrum = _build_spectrum([chakra7, chakra12], schumann)

    synthesis = (
        f"Aujourd'hui, l'énergie du nombre {num_profile['number']} "
        f"({num_profile['keyword']}) s'aligne avec le chakra {chakra7['name']} "
        f"({chakra7['sanskrit']}) et la {gate24['name']}. "
        f"{num_profile['affirmation']} {chakra7['affirmation']}"
    )

    return {
        "agent": AGENT_NAME,
        "period": "daily",
        "period_label": "Prévision Cosmique du Jour",
        "date": reference_date.isoformat(),
        "generated_at": now.isoformat(),
        "numerology": {"label": "Nombre Universel du Jour", **num_profile},
        "lunar": lunar_snapshot,
        "solar": solar,
        "geomagnetic": geo,
        "storm_outlook": storm,
        "schumann": schumann,
        "chakra_7": chakra7,
        "chakra_12": chakra12,
        "gate_24": gate24,
        "spectrum": spectrum,
        "synthesis": synthesis,
    }


def build_weekly_report(reference_date: date = None) -> dict:
    reference_date = reference_date or date.today()
    now = datetime.now(timezone.utc)

    iso_year, iso_week, _ = reference_date.isocalendar()
    monday = date.fromisocalendar(iso_year, iso_week, 1)
    sunday = monday + timedelta(days=6)

    solar, geo, storm, schumann = _gather_space_weather(reference_date)
    lunar_snapshot = lunar.get_lunar_snapshot(now)
    moon_progression = [
        lunar.get_phase_for_date(monday + timedelta(days=i)) for i in range(7)
    ]

    universal_week = numerology.universal_week_number(reference_date)
    num_profile = numerology.number_profile(universal_week)

    chakra7 = chakra_system.select_chakra_7(universal_week)
    chakra12 = chakra_system.select_chakra_12(iso_year * 100 + iso_week)
    gate_open = chakra_system.select_gate_24(monday.toordinal())
    gate_close = chakra_system.select_gate_24(sunday.toordinal())

    spectrum = _build_spectrum([chakra7, chakra12], schumann)

    synthesis = (
        f"Cette semaine (semaine ISO {iso_week}, du {monday.isoformat()} au "
        f"{sunday.isoformat()}), l'énergie du nombre {num_profile['number']} "
        f"({num_profile['keyword']}) met en lumière le centre {chakra12['name']} "
        f"({chakra12['sanskrit']}), avec un arc énergétique allant de la "
        f"{gate_open['name']} à la {gate_close['name']}. "
        f"{num_profile['affirmation']} {chakra7['affirmation']}"
    )

    return {
        "agent": AGENT_NAME,
        "period": "weekly",
        "period_label": "Prévision Cosmique de la Semaine",
        "date": reference_date.isoformat(),
        "week_start": monday.isoformat(),
        "week_end": sunday.isoformat(),
        "iso_year": iso_year,
        "iso_week": iso_week,
        "generated_at": now.isoformat(),
        "numerology": {"label": "Nombre Universel de la Semaine", **num_profile},
        "lunar": lunar_snapshot,
        "moon_progression": moon_progression,
        "solar": solar,
        "geomagnetic": geo,
        "storm_outlook": storm,
        "schumann": schumann,
        "chakra_7": chakra7,
        "chakra_12": chakra12,
        "gate_open": gate_open,
        "gate_close": gate_close,
        "spectrum": spectrum,
        "synthesis": synthesis,
    }


def build_monthly_report(reference_date: date = None) -> dict:
    reference_date = reference_date or date.today()
    now = datetime.now(timezone.utc)

    month_start = reference_date.replace(day=1)
    if reference_date.month == 12:
        next_month_start = reference_date.replace(year=reference_date.year + 1, month=1, day=1)
    else:
        next_month_start = reference_date.replace(month=reference_date.month + 1, day=1)
    month_end = next_month_start - timedelta(days=1)

    solar, geo, storm, schumann = _gather_space_weather(reference_date)
    lunar_snapshot = lunar.get_lunar_snapshot(now)

    universal_month = numerology.universal_month_number(reference_date)
    num_profile = numerology.number_profile(universal_month)

    chakra7 = chakra_system.select_chakra_7(universal_month)
    chakra12 = chakra_system.get_chakra_12_by_number(reference_date.month)
    gate_receiving = chakra_system.get_gate_24_by_number((chakra12["number"] - 1) * 2 + 1)
    gate_radiating = chakra_system.get_gate_24_by_number((chakra12["number"] - 1) * 2 + 2)

    spectrum = _build_spectrum([chakra7, chakra12], schumann)
    month_name = MONTH_NAMES_FR[reference_date.month - 1]

    synthesis = (
        f"Le mois de {month_name} {reference_date.year} est porté par le "
        f"nombre universel {num_profile['number']} ({num_profile['keyword']}), "
        f"avec le centre {chakra12['name']} ({chakra12['sanskrit']}) comme "
        f"thème directeur — entre la {gate_receiving['name']} (recevoir) et "
        f"la {gate_radiating['name']} (rayonner). "
        f"{num_profile['affirmation']} {chakra7['affirmation']}"
    )

    return {
        "agent": AGENT_NAME,
        "period": "monthly",
        "period_label": "Prévision Cosmique du Mois",
        "date": reference_date.isoformat(),
        "month_start": month_start.isoformat(),
        "month_end": month_end.isoformat(),
        "month_name": month_name,
        "generated_at": now.isoformat(),
        "numerology": {"label": "Nombre Universel du Mois", **num_profile},
        "lunar": lunar_snapshot,
        "solar": solar,
        "geomagnetic": geo,
        "storm_outlook": storm,
        "schumann": schumann,
        "chakra_7": chakra7,
        "chakra_12": chakra12,
        "gate_receiving": gate_receiving,
        "gate_radiating": gate_radiating,
        "spectrum": spectrum,
        "synthesis": synthesis,
    }


BUILDERS = {
    "daily": build_daily_report,
    "weekly": build_weekly_report,
    "monthly": build_monthly_report,
}


def build_report(period: str, reference_date: date = None) -> dict:
    builder = BUILDERS.get(period)
    if builder is None:
        raise ValueError(f"Période inconnue : {period!r} (attendu : daily, weekly, monthly)")
    return builder(reference_date)


# ---------------------------------------------------------------------------
# Rendu — rapport complet, Facebook, Instagram, hashtags
# ---------------------------------------------------------------------------

def _hashtags(report: dict, extra: bool = False) -> str:
    tags = list(BASE_HASHTAGS)
    if extra:
        tags += EXTRA_HASHTAGS
    period_tag = PERIOD_HASHTAGS.get(report["period"])
    if period_tag:
        tags.append(period_tag)
    return " ".join(tags)


def _render_gate_section(report: dict) -> list:
    lines = []
    if "gate_24" in report:
        g = report["gate_24"]
        lines.append(f"### Porte du Jour (système des 24) : #{g['number']} — {g['name']} ({g['polarity']})")
        lines.append(f"- {g['theme']}")
        lines.append(f"- Centre associé : {g['chakra_12']}")
    elif "gate_open" in report:
        go, gc = report["gate_open"], report["gate_close"]
        lines.append("### Arc des Portes de la Semaine (système des 24)")
        lines.append(f"- Ouverture (lundi) : #{go['number']} — {go['name']} ({go['polarity']}) — {go['theme']}")
        lines.append(f"- Clôture (dimanche) : #{gc['number']} — {gc['name']} ({gc['polarity']}) — {gc['theme']}")
    elif "gate_receiving" in report:
        gr, gd = report["gate_receiving"], report["gate_radiating"]
        lines.append("### Portes Recevoir / Rayonner du Mois (système des 24)")
        lines.append(f"- Recevoir : #{gr['number']} — {gr['name']} — {gr['theme']}")
        lines.append(f"- Rayonner : #{gd['number']} — {gd['name']} — {gd['theme']}")
    return lines


def render_full_report(report: dict) -> str:
    lines = []
    lines.append(f"# 🌌 {report['agent']} — {report['period_label']}")
    lines.append(f"**Date :** {report['date']}")
    if report["period"] == "weekly":
        lines.append(
            f"**Semaine :** {report['week_start']} → {report['week_end']} "
            f"(ISO {report['iso_week']}/{report['iso_year']})"
        )
    elif report["period"] == "monthly":
        lines.append(
            f"**Mois :** {report['month_name'].capitalize()} {report['date'][:4]} "
            f"({report['month_start']} → {report['month_end']})"
        )
    lines.append(f"**Généré le :** {report['generated_at']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    s = report["schumann"]
    lines.append("## 🌍 Résonance de Schumann")
    lines.append(f"- Fréquence fondamentale : **{s['base_frequency_hz']} Hz**")
    lines.append(f"- Lecture estimée du jour : **{s['estimated_reading_hz']} Hz**")
    lines.append(f"- Harmoniques : {', '.join(str(h) for h in s['harmonics_hz'])} Hz")
    lines.append(f"- Intensité du champ : **{s['field_intensity']}**")
    lines.append(f"- Interprétation : {s['interpretation']}")
    lines.append(f"- _Méthode : {s['method']}_")
    lines.append("")

    sol = report["solar"]
    lines.append("## ☀️ Activité Solaire")
    if sol.get("flare_count") is not None:
        lines.append(f"- Éruptions détectées (24h) : **{sol['flare_count']}**")
        if sol.get("strongest_class"):
            lines.append(f"- Éruption la plus forte : **{sol['strongest_class']}** ({sol.get('strongest_time')})")
    lines.append(f"- {sol['summary']}")
    lines.append(f"- _Source : {sol['source']}_")
    lines.append("")

    geo = report["geomagnetic"]
    storm = report["storm_outlook"]
    lines.append("## 🧭 Activité Géomagnétique")
    lines.append(f"- Indice Kp : **{geo['kp_index']}** — {geo['level']}")
    lines.append(f"- {geo['interpretation']}")
    if storm.get("g_scale") is not None:
        lines.append(f"- Prévision de tempête géomagnétique (échelle G) : **G{storm['g_scale']} — {storm['g_level_fr']}**")
    lines.append(f"- _Source : {geo['source']}_")
    lines.append("")

    moon = report["lunar"]
    lines.append("## 🌙 Mouvement Lunaire")
    lines.append(f"- Phase actuelle : **{moon['phase_name']}** ({moon['illumination_pct']}% illuminée)")
    lines.append(f"- Signe zodiacal : **{moon['zodiac_sign']}** ({moon['zodiac_degree']}°)")
    lines.append(f"- Âge de la Lune : {moon['age_days']} jours")
    lines.append(f"- Prochaine Nouvelle Lune : {moon['next_new_moon']}")
    lines.append(f"- Prochaine Pleine Lune : {moon['next_full_moon']}")
    if "moon_progression" in report:
        lines.append("- Progression lunaire de la semaine :")
        for day in report["moon_progression"]:
            lines.append(f"  - {day['date']} : {day['phase_name']} ({day['illumination_pct']}%)")
    lines.append("")

    num = report["numerology"]
    lines.append("## 🔢 Numérologie")
    lines.append(f"- {num['label']} : **{num['number']} — {num['keyword']}**")
    lines.append(f"- Thème : {num['theme']}")
    lines.append(f"- Affirmation : _{num['affirmation']}_")
    lines.append("")

    c7 = report["chakra_7"]
    c12 = report["chakra_12"]
    lines.append("## 🌈 Alignement Chakras & Portes")
    lines.append(f"### Chakra Focus (système des 7) : {c7['name']} ({c7['sanskrit']})")
    lines.append(f"- Mot-clé : {c7['keyword']}")
    lines.append(f"- Thème : {c7['theme']}")
    lines.append(f"- Fréquence : {c7['frequency_hz']} Hz — Couleur : {c7['color_name']} ({c7['color_hex']})")
    lines.append(f"- Affirmation : _{c7['affirmation']}_")
    lines.append("")
    lines.append(f"### Centre Énergétique (système des 12) : {c12['name']} ({c12['sanskrit']})")
    lines.append(f"- Mot-clé : {c12['keyword']}")
    lines.append(f"- Thème : {c12['theme']}")
    lines.append(f"- Fréquence : {c12['frequency_hz']} Hz — Couleur : {c12['color_name']} ({c12['color_hex']})")
    lines.append("")
    lines.extend(_render_gate_section(report))
    lines.append("")

    spec = report["spectrum"]
    lines.append("## 🎼 Spectre Fréquences & Couleurs")
    lines.append(f"- Fréquences (Hz) : {', '.join(str(f) for f in spec['frequencies_hz'])}")
    lines.append("- Couleurs :")
    for c in spec["colors"]:
        lines.append(f"  - {c['name']} ({c['hex']}) — {c['source']}")
    lines.append("")

    lines.append("## ✨ Synthèse Soma V1")
    lines.append(report["synthesis"])
    lines.append("")
    lines.append("---")
    lines.append(DISCLAIMER_FR)

    return "\n".join(lines)


def render_facebook_post(report: dict) -> str:
    s = report["schumann"]
    sol = report["solar"]
    geo = report["geomagnetic"]
    moon = report["lunar"]
    num = report["numerology"]
    c7 = report["chakra_7"]
    c12 = report["chakra_12"]

    lines = []
    lines.append(f"🌌✨ {report['agent']} — {report['period_label']} ✨🌌")
    lines.append(f"📅 {report['date']}")
    lines.append("")
    lines.append(f"🌍 Schumann : {s['estimated_reading_hz']} Hz — {s['field_intensity']}")
    lines.append(f"☀️ Soleil : {sol['summary']}")
    lines.append(f"🧭 Géomagnétisme : Kp {geo['kp_index']} — {geo['level']}")
    lines.append(f"🌙 Lune : {moon['phase_name']} en {moon['zodiac_sign']} ({moon['illumination_pct']}% illuminée)")
    lines.append(f"🔢 Numérologie : {num['number']} — {num['keyword']}")
    lines.append(f"🌈 Chakra du moment : {c7['name']} ({c7['sanskrit']}) — {c7['frequency_hz']} Hz — {c7['color_name']}")
    lines.append(f"🔮 Centre des 12 : {c12['name']} — {c12['frequency_hz']} Hz")

    if "gate_24" in report:
        g = report["gate_24"]
        lines.append(f"🚪 Porte #{g['number']} : {g['name']} ({g['polarity']})")
    elif "gate_open" in report:
        go, gc = report["gate_open"], report["gate_close"]
        lines.append(f"🚪 Portes de la semaine : #{go['number']} {go['name']} → #{gc['number']} {gc['name']}")
    elif "gate_receiving" in report:
        gr, gd = report["gate_receiving"], report["gate_radiating"]
        lines.append(f"🚪 Portes du mois : Recevoir #{gr['number']} {gr['name']} / Rayonner #{gd['number']} {gd['name']}")

    lines.append("")
    lines.append(f"💫 {report['synthesis']}")
    lines.append("")
    lines.append(_hashtags(report))
    lines.append("")
    lines.append(DISCLAIMER_FR)

    return "\n".join(lines)


def render_instagram_post(report: dict) -> str:
    s = report["schumann"]
    geo = report["geomagnetic"]
    moon = report["lunar"]
    num = report["numerology"]
    c7 = report["chakra_7"]

    lines = []
    lines.append(f"🌌 {report['agent']} · {report['period_label']}")
    lines.append(f"📅 {report['date']}")
    lines.append("")
    lines.append(f"🌍 Schumann {s['estimated_reading_hz']}Hz · {s['field_intensity']}")
    lines.append(f"🧭 Kp {geo['kp_index']} · {geo['level']}")
    lines.append(f"🌙 {moon['phase_name']} en {moon['zodiac_sign']}")
    lines.append(f"🔢 Nombre {num['number']} · {num['keyword']}")
    lines.append(f"🌈 {c7['name']} · {c7['frequency_hz']}Hz · {c7['color_name']}")
    lines.append("")
    lines.append(report["synthesis"])
    lines.append("")
    lines.append(_hashtags(report, extra=True))

    return "\n".join(lines)
