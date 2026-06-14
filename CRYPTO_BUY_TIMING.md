# 💰 Crypto Buy Timing

Crypto Buy Timing est le mini tableau de bord de LUMIAION qui indique, pour
**BTC/USDT** et **l'Or (XAU/USD)**, s'il s'agit actuellement d'un bon moment
pour acheter, et quels sont historiquement les meilleurs horaires.

## Accès

- **Dashboard web** : route `/crypto` (page HTML avec graphiques).
- **Données brutes (JSON)** : route `/api/crypto-timing`.

## Sources de données

Toutes les données viennent de l'**API publique Kraken** (sans clé API,
bougies horaires sur ~30 jours) :

- **BTC/USDT** : paire `BTCUSDT`.
- **Or (XAU/USD)** : paire `PAXGUSD` — [PAX Gold (PAXG)](https://paxos.com/paxgold/)
  est un jeton adossé 1:1 à une once d'or fin et trade en quasi temps réel
  au cours du spot XAU/USD. Il sert de proxy fiable et sans clé API pour le
  prix de l'or.

## Ce que le dashboard affiche, pour chaque actif

- **Prix actuel** et **variation sur 24h**.
- **RSI (14)** — indicateur de survente/surachat.
- **Moyennes mobiles SMA 20 / SMA 50**.
- **Bandes de Bollinger** (20 périodes, 2 écarts-types).
- **Signal d'achat actuel** :
  - 🟢 **Achat fort** — RSI ≤ 30 et prix proche de la bande basse de Bollinger.
  - 🟢 **Achat** — RSI ≤ 40 ou prix sous sa SMA 20.
  - 🟡 **Attendre** — RSI ≥ 60 sans signal de repli marqué.
  - 🔴 **Surachat — Prudence** — RSI ≥ 70 et prix proche de la bande haute.
  - ⚪ **Neutre** — aucun signal fort.
- **Meilleures heures historiques (UTC)** et **meilleurs jours** pour
  acheter, calculés sur les 30 derniers jours : pour chaque bougie horaire,
  on calcule son z-score par rapport aux 24 heures précédentes, puis on
  regroupe par heure de la journée et par jour de la semaine. Les heures /
  jours avec le z-score moyen le plus bas sont ceux où le prix tend
  historiquement à être en retrait par rapport à sa moyenne récente.
- **Graphique** des 7 derniers jours de prix (Chart.js).

## Personnaliser

- `crypto_buy_timing/analyzer.py` — liste des actifs suivis (`ASSETS`),
  logique du signal d'achat (`_signal`) et de l'analyse de saisonnalité
  (`_best_buy_windows`).
- `crypto_buy_timing/indicators.py` — RSI, SMA, bandes de Bollinger, z-score
  glissant (implémentations sans dépendance externe).
- `crypto_buy_timing/data_sources.py` — appel à l'API Kraken.
- `templates/crypto_dashboard.html` — mise en forme du dashboard.

## Avertissement

⚠️ Ceci n'est **pas un conseil financier**. Les signaux sont basés sur des
indicateurs techniques simples et une analyse statistique des 30 derniers
jours — ils ne garantissent aucune performance future.
