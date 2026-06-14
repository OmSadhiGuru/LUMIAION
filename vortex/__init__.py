"""VORTEX — signaux de timing d'achat pour BTC/USDT et l'Or (XAU/USD).

VORTEX est un tableau de bord de trading indépendant, isolé du reste de
LUMIAION. Il analyse les prix récents de BTC/USDT et de l'or (XAU/USD, via
le jeton PAX Gold/PAXG comme proxy temps réel) pour proposer un signal
d'achat actuel (RSI, moyennes mobiles, bandes de Bollinger) ainsi que les
heures et jours historiquement les plus favorables pour acheter.
"""

from .analyzer import get_dashboard_data

__all__ = ["get_dashboard_data"]
