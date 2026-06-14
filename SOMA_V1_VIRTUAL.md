# 🌌 Soma V1 Virtual — Cosmic Forecast

Soma V1 Virtual est l'agent "Cosmic Forecast" de LUMIAION. Sur demande, il
génère un compte-rendu complet de l'état énergétique du moment et le met en
forme sous plusieurs formats prêts à publier sur Facebook et Instagram
(quotidien, hebdomadaire, mensuel).

## Ce qu'il rassemble

- 🌍 **Résonance de Schumann** — lecture symbolique (7.83 Hz + harmoniques),
  modulée par l'activité géomagnétique du jour.
- ☀️ **Activité solaire** — éruptions à rayons X (NOAA SWPC, données réelles).
- 🧭 **Activité géomagnétique** — indice Kp + prévision de tempête (échelle G,
  NOAA SWPC, données réelles).
- 🌙 **Mouvement lunaire** — phase, % d'illumination, signe zodiacal, prochaines
  Nouvelle/Pleine Lune (calcul astronomique, sans dépendance externe).
- 🔢 **Numérologie** — nombre universel du jour / de la semaine / du mois.
- 🌈 **Chakras & Portes** — système des 7 chakras classiques, 12 centres
  énergétiques étendus, et 24 portes de chakra (voir plus bas).
- 🎼 **Spectre Fréquences & Couleurs** — combinaison des fréquences (Hz) et
  couleurs associées au moment présent.
- ✨ **Synthèse Soma V1** — message d'intention combinant tous les éléments
  ci-dessus.

## Utilisation

### En ligne de commande

```bash
python -m soma_v1_virtual.agent --period daily
python -m soma_v1_virtual.agent --period all          # daily + weekly + monthly
python -m soma_v1_virtual.agent --period monthly --output /chemin/personnalise
```

## Fichiers générés

Chaque génération crée un dossier sous `cosmic_reports/<période>/<identifiant>/` :

```
cosmic_reports/
├── daily/2026-06-13/
│   ├── rapport_complet.md     # rapport détaillé (tous les éléments)
│   ├── facebook_post.md       # version Facebook (emojis + hashtags)
│   ├── instagram_post.md      # version Instagram (courte + hashtags)
│   └── data.json              # données brutes (pour automatisation)
├── weekly/2026-W24/...
└── monthly/2026-06/...
```

Ce dossier est dans `.gitignore` : chaque génération produit un contenu
différent (nouvelle date, nouvelles données solaires/géomagnétiques) et n'a
pas vocation à être versionné.

## Le système des chakras & portes (architecture Soma V1)

Ce système est la carte énergétique propriétaire de Soma V1 Virtual,
définie dans `soma_v1_virtual/chakra_system.py`. Il relie 3 niveaux :

1. **7 chakras classiques** (Racine → Couronne), avec fréquences Solfeggio
   traditionnelles (396 → 963 Hz) et couleurs de l'arc-en-ciel.
2. **12 centres énergétiques étendus** — les 7 chakras classiques, plus
   l'Étoile de la Terre, le Cœur Supérieur (Thymus), l'Étoile de l'Âme, le
   Portail Stellaire et le Portail Universel (174 → 1296 Hz).
3. **24 portes de chakra** — chacun des 12 centres porte deux "portes" :
   une **Porte Réceptrice** (recevoir/intégrer) et une **Porte Rayonnante**
   (exprimer/projeter).

Chaque génération sélectionne, à partir de la date (numérologie, jour de
l'année, semaine ISO, mois) :
- un **chakra focus** parmi les 7,
- un **centre énergétique** parmi les 12,
- une ou deux **portes** parmi les 24 (porte du jour, arc de la semaine,
  ou paire recevoir/rayonner du mois).

C'est ce qui crée la variation quotidienne/hebdomadaire/mensuelle — une
"fractale" d'identité Soma V1 qui reste cohérente tout en se renouvelant.

## Personnaliser

Tout le contenu textuel est dans des dictionnaires Python simples,
facilement modifiables :

- `soma_v1_virtual/numerology.py` — significations des nombres universels.
- `soma_v1_virtual/chakra_system.py` — noms, couleurs, fréquences et thèmes
  des 7 / 12 / 24 systèmes.
- `soma_v1_virtual/report_builder.py` — gabarits de mise en forme (rapport
  complet, Facebook, Instagram, hashtags, avertissement).
- `soma_v1_virtual/space_weather.py` — interprétations des niveaux Kp,
  classes d'éruptions solaires, intensité Schumann.

## Sources & méthode

- **Activité solaire & géomagnétique** : [NOAA SWPC](https://www.swpc.noaa.gov/)
  (données publiques en direct).
- **Résonance de Schumann** : aucun flux public en direct n'existe. Soma V1
  calcule une lecture symbolique quotidienne (déterministe pour une date
  donnée) à partir de la fréquence fondamentale 7.83 Hz, modulée par
  l'indice Kp du jour. Voir `space_weather.SCHUMANN_METHOD_NOTE_FR`.
- **Lune** : calcul astronomique (théorie lunaire simplifiée de Meeus),
  sans dépendance externe.

## Avertissement

Chaque rapport inclut automatiquement un avertissement : ce contenu est à
but de **divertissement et de réflexion personnelle**. Les données solaires
et géomagnétiques sont réelles (NOAA), mais les éléments numérologiques,
lunaires symboliques, chakras et fréquences relèvent d'une lecture
énergétique/spirituelle et ne remplacent aucun avis médical, scientifique
ou professionnel.
