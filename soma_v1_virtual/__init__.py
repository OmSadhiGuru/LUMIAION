"""Soma V1 Virtual — Cosmic Forecast pour LUMIAION.

Génère des rapports quotidiens, hebdomadaires et mensuels combinant la
résonance de Schumann, l'activité solaire, l'activité géomagnétique, le
mouvement lunaire, la numérologie et le système des chakras (7 / 12 /
24 portes) en un spectre prêt à publier sur Facebook et Instagram.
"""

from .agent import generate_cosmic_forecast
from .report_builder import build_report

__all__ = ["generate_cosmic_forecast", "build_report"]
