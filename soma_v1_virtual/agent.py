"""Soma V1 Virtual — point d'entrée de l'agent Cosmic Forecast.

Génère le rapport (quotidien, hebdomadaire ou mensuel), l'écrit dans un
dossier de sortie prêt à publier (Facebook, Instagram, rapport complet,
données brutes JSON), et retourne le tout pour une intégration (Telegram,
script planifié, etc.).
"""

import argparse
import json
import os
from datetime import date

from . import report_builder

DEFAULT_OUTPUT_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cosmic_reports"
)


def _output_folder_name(report: dict) -> str:
    if report["period"] == "weekly":
        return f"{report['iso_year']}-W{report['iso_week']:02d}"
    if report["period"] == "monthly":
        return report["date"][:7]
    return report["date"]


def generate_cosmic_forecast(period: str = "daily", reference_date: date = None,
                              output_root: str = None) -> dict:
    """Génère la prévision cosmique Soma V1 Virtual pour la période donnée
    ("daily", "weekly" ou "monthly").

    Écrit les fichiers prêts à publier dans
    `output_root/<period>/<dossier>/` (rapport_complet.md, facebook_post.md,
    instagram_post.md, data.json) et retourne un dictionnaire contenant les
    chemins et les textes générés.
    """
    report = report_builder.build_report(period, reference_date)

    full_text = report_builder.render_full_report(report)
    facebook_text = report_builder.render_facebook_post(report)
    instagram_text = report_builder.render_instagram_post(report)

    output_root = output_root or DEFAULT_OUTPUT_ROOT
    folder = os.path.join(output_root, period, _output_folder_name(report))
    os.makedirs(folder, exist_ok=True)

    paths = {
        "report": os.path.join(folder, "rapport_complet.md"),
        "facebook": os.path.join(folder, "facebook_post.md"),
        "instagram": os.path.join(folder, "instagram_post.md"),
        "data": os.path.join(folder, "data.json"),
    }

    with open(paths["report"], "w", encoding="utf-8") as f:
        f.write(full_text)
    with open(paths["facebook"], "w", encoding="utf-8") as f:
        f.write(facebook_text)
    with open(paths["instagram"], "w", encoding="utf-8") as f:
        f.write(instagram_text)
    with open(paths["data"], "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return {
        "report_data": report,
        "output_dir": folder,
        "paths": paths,
        "full_report": full_text,
        "facebook_post": facebook_text,
        "instagram_post": instagram_text,
    }


def _parse_args():
    parser = argparse.ArgumentParser(description="Soma V1 Virtual — Cosmic Forecast")
    parser.add_argument(
        "--period", choices=["daily", "weekly", "monthly", "all"], default="daily",
        help="Période à générer (par défaut : daily)",
    )
    parser.add_argument(
        "--output", default=None,
        help="Dossier de sortie racine (par défaut : ./cosmic_reports)",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    periods = ["daily", "weekly", "monthly"] if args.period == "all" else [args.period]
    for period in periods:
        result = generate_cosmic_forecast(period=period, output_root=args.output)
        print(f"✅ {period} -> {result['output_dir']}")


if __name__ == "__main__":
    main()
