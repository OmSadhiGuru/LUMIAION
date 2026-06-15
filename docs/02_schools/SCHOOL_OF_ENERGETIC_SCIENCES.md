# School of Energetic Sciences — Department Build (Phase 2)

**School #2 of 9.** Per the Phase 2 scope defined in
[`../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`](../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md)
§8 ("Horizontal Expansion — Main Information + Analyst Vault layer + 1–2 flagship
studies"), this file builds the L2/L3 map and two flagship Studies for the
department dedicated to **energy, frequency, resonance, breath, and the subtle
architecture of living systems.** It follows the Universal School and Subject
Templates in [`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md) and uses
[`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`](SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md)
as its style and depth reference, scaled to Phase 2.

---

## 1. Department Overview

**Core Question:** *How does energy move through, around, and between living
systems — and how can it be consciously directed?*

**Mission:** To build a rigorous, cross-referenced map of the energetic models —
ancient and modern, subtle and measurable — that describe how living systems
generate, hold, lose, and exchange energy; to translate that map into breath,
sound, and awareness practices that produce felt, repeatable shifts in state; and
to keep that map permanently wired to **live planetary data** (solar and
geomagnetic activity, lunar cycles) so that "energy work" is never purely
abstract — it is always checked against what is actually happening in the field
around the practitioner.

**Relationship to existing content:** Per
[`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`](../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md)
§9's migration table, this school is the institutional home for the **chakra and
frequency system migrated from "OSG LIFE OS" → SOHMA**. Every chakra, frequency,
and energy-center definition that previously lived inside OSG LIFE OS becomes a
Subjects-DB row here, tagged `Domain Tags: Energy & Frequency, Chakra System` and
`Owner Agent: SOHMA`.

**Relationship to LUMIAION / runtime:** This school is the **primary content home
for SOHMA's runtime** (`/soma_v1_virtual`). Two modules map directly onto Studies
below:

- `soma_v1_virtual/chakra_system.py` — the 7-chakra system (`CHAKRAS_7`), the
  12-center extended energy-body model (`CHAKRAS_12`, Earth Star → Universal
  Gateway), and the 24 Chakra Gates (`CHAKRA_GATES_24`) — feeds **Chakra System &
  Subtle Anatomy** (L2) directly, including the Solfeggio-aligned frequency value
  (Hz) attached to each of the 7 classical chakras.
- `soma_v1_virtual/space_weather.py` — live NOAA SWPC data (planetary Kp
  geomagnetic index, GOES X-ray solar flares, G-scale storm outlook) plus a
  deterministic symbolic Schumann-resonance estimate anchored to 7.83 Hz — feeds
  **Schumann Resonance & the Biofield** (L2) directly.
- `soma_v1_virtual/lunar.py` — lunar phase/illumination/zodiac calculations — feeds
  **Subtle Body Mapping** and cross-links to
  [`SCHOOL_OF_NATURAL_INTELLIGENCE.md`](SCHOOL_OF_NATURAL_INTELLIGENCE.md)'s
  circadian/lunar rhythm Studies.

Every SOHMA cosmic report (`cosmic_reports/<period>/<date>/data.json`) is, in
effect, a dated Research Vault row (`Type = Internal Observation`,
`School = Energetic Sciences`, `Owner Agent = SOHMA`) waiting to be ingested — no
schema changes required (`LUMIAION_MASTER_ARCHITECTURE.md` §6).

---

## 2. L2 Subject Map

### L2 Subjects (Hierarchy Level = Subject, Parent Subject empty)

| Name | Subject Type | Mastery Level | Definition | Domain Tags | Owner Agent | Related Subjects |
|---|---|---|---|---|---|---|
| Chakra System & Subtle Anatomy | Core Topic | All levels | The body's energy-center model — from the classical 7-chakra system through SOHMA's extended 12-center map and 24-gate grid — as a framework for locating where energy concentrates, blocks, and flows in a person. | Chakra System, Energy & Frequency | SOHMA | Solfeggio Frequencies & Sound Healing; Subtle Body Mapping; Energy Hygiene, Boundaries & Protection |
| Solfeggio Frequencies & Sound Healing | Core Topic | All levels | The study of specific sound frequencies (396–963 Hz and beyond) said to correspond to states of consciousness and to the body's energy centers, and of sound/vibration as a direct input to the nervous system. | Energy & Frequency, Chakra System | SOHMA | Chakra System & Subtle Anatomy; Schumann Resonance & the Biofield |
| Schumann Resonance & the Biofield | Core Topic | Intermediate+ | The study of the Earth's electromagnetic resonance (~7.83 Hz fundamental) and planetary space-weather (solar/geomagnetic activity) as an ambient field that living systems are continuously entrained to and affected by. | Energy & Frequency, Cosmology & Cycles | SOHMA | Solfeggio Frequencies & Sound Healing; Subtle Body Mapping |
| Pranayama & Breath as Energy Technology | Core Topic | All levels | Breath as the most direct, voluntary lever a person has on their own energetic and nervous-system state — from simple regulation patterns to traditional pranayama techniques. | Energy & Frequency, Practice, Embodiment | Lumiaion, Human | Chakra System & Subtle Anatomy; Energy Hygiene, Boundaries & Protection |
| Energy Hygiene, Boundaries & Protection | Concept | All levels | Practices and frameworks for managing one's own energetic state in relation to other people and environments — discernment, boundary-setting, clearing, and grounding, framed without superstition as applied self-regulation. | Energy & Frequency, Shadow Work | Human, Lumiaion | Chakra System & Subtle Anatomy; Pranayama & Breath as Energy Technology |
| Subtle Body Mapping (Auras, Meridians, Nadis) | Concept | Intermediate+ | A comparative survey of subtle-anatomy models across traditions — the aura/biofield (Western esoteric), meridians (Traditional Chinese Medicine), and nadis (Yogic) — as overlapping attempts to map the same underlying phenomenon from different cultural vantage points. | Energy & Frequency, Cosmology & Cycles | SOHMA, Human | Chakra System & Subtle Anatomy; Schumann Resonance & the Biofield |

### L3 Studies (Hierarchy Level = Study, Parent Subject → L2 row above)

#### Parent Subject: Chakra System & Subtle Anatomy

| Name | Definition |
|---|---|
| ⭐ The Seven-Chakra System | The classical Muladhara→Sahasrara model of seven energy centers, each with a color, theme, and Solfeggio-aligned frequency, as implemented in SOHMA's `CHAKRAS_7`. |
| The Twelve-Center Extended Energy Body | SOHMA's `CHAKRAS_12` model — extending the 7-chakra system downward to the Earth Star and upward through the Soul Star, Stellar Gateway, and Universal Gateway. |
| The 24 Chakra Gates | SOHMA's `CHAKRA_GATES_24` — each of the 12 centers expressed as a "Receptive" (receiving) and "Radiant" (transmitting) gate, forming a 24-point map of how energy is taken in and expressed. |
| Chakra Balancing & Diagnostic Frameworks | Methods (self-assessment, body-sensation mapping, journaling) for identifying which chakra(s) are under- or over-active in a given period. |
| Chakras Across Traditions | A comparative look at how the chakra model is treated in classical Tantric/Yogic sources versus its adaptation in modern Western wellness culture — what's preserved, what's altered. |

#### Parent Subject: Solfeggio Frequencies & Sound Healing

| Name | Definition |
|---|---|
| ⭐ Solfeggio Frequencies in Practice | The nine commonly cited Solfeggio tones (174–963 Hz) — their claimed effects, their mapping onto SOHMA's chakra frequencies, and how to use them as a structured listening practice. |
| Binaural Beats & Brainwave Entrainment | The mechanism by which two slightly different tones presented to each ear can be perceived as a single pulsing beat, and the (mixed) evidence for entrainment effects on attention, relaxation, and sleep. |
| Sound as Vibration: A Physics Primer | A plain-language grounding in what sound and vibration actually are — pressure waves, frequency, resonance, harmonics — as the factual floor beneath every sound-healing claim. |
| Mantra, Toning & the Voice as Instrument | The use of the practitioner's own voice — chanting, toning, humming — as a portable, always-available frequency practice, including vagus-nerve stimulation via humming/toning. |
| Building a Personal Frequency Practice | A practical framework for choosing, sequencing, and tracking sound-based practices (Solfeggio playlists, toning, singing bowls) against a stated intention. |

#### Parent Subject: Schumann Resonance & the Biofield

| Name | Definition |
|---|---|
| ⭐ Schumann Resonance: The Planet's Pulse | The science and lore of the Earth-ionosphere cavity resonance (~7.83 Hz fundamental and its harmonic series), and SOHMA's deterministic symbolic daily reading derived from it. |
| Reading Space Weather: Kp Index & Solar Flares | How to read NOAA SWPC's planetary Kp geomagnetic index and GOES X-ray flare classifications (A–X) as SOHMA does — and what each level practically suggests for grounding, rest, and sensitivity. |
| The Biofield Hypothesis | The proposition (held with `Confidence Level = Hypothesis`) that living organisms generate and are sensitive to weak electromagnetic/energetic fields beyond the nervous system's electrical signals — surveyed neutrally, including critiques. |
| Geomagnetic Sensitivity & Self-Tracking | A practical framework for personally tracking subjective state (sleep, mood, focus) against daily Kp index and solar activity data to test — for oneself — whether correlations exist. |
| Solar Cycles & Long-Range Rhythms | The ~11-year solar cycle and its proposed (and contested) links to collective mood, innovation waves, and historical events — framed as a long-timescale companion to the daily Schumann reading. |

#### Parent Subject: Pranayama & Breath as Energy Technology

| Name | Definition |
|---|---|
| Breath Anatomy & the Autonomic Nervous System | How breath mechanics (diaphragmatic vs. shallow, inhale/exhale ratios) directly drive the sympathetic/parasympathetic balance — the physiological foundation under every pranayama claim. |
| Foundational Pranayama Techniques | A survey of core techniques — Nadi Shodhana (alternate nostril), Ujjayi (ocean breath), Kapalabhati (skull-shining), Bhramari (bee breath) — with mechanism, traditional purpose, and cautions. |
| Box Breathing & Modern Regulation Protocols | Simple ratio-based breathing patterns (e.g., 4-4-4-4) used in clinical, military, and athletic settings for rapid state-shifting — the "secular pranayama" on-ramp. |
| Breath & the Vagus Nerve | The vagus nerve as the physiological bridge between breath and the chakra/energy-center model — extended exhales and humming/toning as vagal-tone practices. |
| Breath Pacing for Energy States | A framework matching breath patterns to desired outcomes — energizing (faster, top-heavy breath) vs. calming (slower, extended exhale) — as a decision tool. |

#### Parent Subject: Energy Hygiene, Boundaries & Protection

| Name | Definition |
|---|---|
| Energetic Boundaries: A Working Model | A non-superstitious framework for "energetic boundaries" as attention- and nervous-system management in relationships and environments. |
| Grounding & Clearing Practices | Practical techniques (physical grounding, visualization, breath, movement) for returning to a centered baseline after an energetically demanding interaction or environment. |
| Discernment: Whose Energy Is This? | A reflective framework for distinguishing one's own emotional/energetic state from what's been absorbed from others or from an environment — a prerequisite for boundary-setting. |
| Digital Environments as Energy Fields | Treating screen time, social media, and notification load as an "energy hygiene" category — what depletes and what restores, in the same frame as physical environments. |
| Designing a Personal Energy Hygiene Protocol | A template for assembling daily/weekly grounding, clearing, and boundary practices into a sustainable personal protocol. |

#### Parent Subject: Subtle Body Mapping (Auras, Meridians, Nadis)

| Name | Definition |
|---|---|
| The Aura: Layers & Models | A survey of the "auric field" / biofield models from Western esoteric and modern energy-healing traditions — the layered-body model and its claimed correspondences to physical/emotional/mental states. |
| Meridians & Traditional Chinese Medicine | The TCM meridian system as a map of energy (Qi) pathways connecting organs and the body surface — and its practical expression in acupuncture, acupressure, and Qigong. |
| Nadis & the Yogic Subtle Body | The Yogic model of nadis (subtle energy channels), with Ida, Pingala, and Sushumna as the central triad — and how this model relates to the chakra system above it. |
| Comparative Subtle Anatomy | A side-by-side framework placing chakras, meridians, nadis, and the aura on shared axes (location, function, claimed mechanism) — clarifying overlap vs. genuinely distinct claims. |
| The Lunar Body: Cycles & Subtle Rhythm | How lunar phase (via `soma_v1_virtual/lunar.py`) is traditionally mapped onto subtle-body states — and a grounded framework for using lunar tracking as a rhythm cue rather than a deterministic claim. |

---

## 3. Flagship Studies

### ⭐ The Seven-Chakra System

**Flagship = ✅**

1. **Definition** — The classical model of seven energy centers running roughly
   along the spine from the base to the crown of the head — Root (Muladhara),
   Sacral (Svadhisthana), Solar Plexus (Manipura), Heart (Anahata), Throat
   (Vishuddha), Third Eye (Ajna), and Crown (Sahasrara) — each associated with a
   color, a theme, and (in SOHMA's implementation) a specific frequency in Hz. This
   Study is the canonical reference for every other chakra-related Study in this
   school.

2. **Historical Context** — The chakra system originates in Tantric and Yogic
   texts (notably the *Sat-Cakra-Nirupana*, translated and popularized in the West
   by Arthur Avalon/John Woodroffe, 1919), where chakras are described as subtle
   energy centers (*cakra* = "wheel") linked to the nadis. The 20th-century Western
   popularization — fixed color associations, a strict 7-center hierarchy, and
   pairings with specific musical/Solfeggio frequencies — is a later synthesis,
   most influentially systematized by Anodea Judith (*Wheels of Life*, 1987;
   *Eastern Body, Western Mind*, 1996), who mapped the seven chakras onto Western
   developmental psychology. SOHMA's `CHAKRAS_7` table (in
   `soma_v1_virtual/chakra_system.py`) follows this modern synthesis: 7 centers,
   each with a Sanskrit name, a color (hex), a Solfeggio-aligned frequency in Hz, a
   theme, and a daily affirmation.

3. **Core Principles**
   - The seven centers form a **vertical gradient** from survival/embodiment
     (Root) to transcendence/unity (Crown) — each center is not "better" than the
     one below it, but addresses a different layer of human experience.
   - Each chakra in SOHMA's model pairs a **color**, a **frequency (Hz)**, and a
     **theme** — three different "languages" (visual, auditory, conceptual)
     pointing at the same center, which is itself a teaching tool: the same
     underlying state can be approached through multiple sensory channels.
   - The system is best used **diagnostically and developmentally**, not as a
     literal anatomical claim — "which center feels active/blocked right now"
     is a useful self-report frame regardless of one's metaphysical commitments
     about subtle anatomy.

4. **Frameworks** — SOHMA's `CHAKRAS_7` table, reproduced here as the master
   reference grid:

   | # | Name (FR/EN) | Sanskrit | Color | Frequency (Hz) | Keyword |
   |---|---|---|---|---|---|
   | 1 | Root | Muladhara | Ruby Red (`#C0392B`) | 396 | Stability & Survival |
   | 2 | Sacral | Svadhisthana | Amber Orange (`#E67E22`) | 417 | Creativity & Flow |
   | 3 | Solar Plexus | Manipura | Golden Yellow (`#F1C40F`) | 528 | Will & Transformation |
   | 4 | Heart | Anahata | Emerald Green (`#27AE60`) | 639 | Love & Connection |
   | 5 | Throat | Vishuddha | Sapphire Blue (`#2980B9`) | 741 | Expression & Truth |
   | 6 | Third Eye | Ajna | Indigo (`#6C3483`) | 852 | Intuition & Vision |
   | 7 | Crown | Sahasrara | Violet (`#8E44AD`) | 963 | Unity & Transcendence |

   This grid is the **shared key** between this Study and **Solfeggio Frequencies
   in Practice** (each frequency above is also one of the nine commonly cited
   Solfeggio tones).

5. **Applications** — Used as the organizing frame for "where am I, energetically,
   right now" check-ins; as a structure for sequencing a practice session (e.g.,
   grounding work before Root, then moving upward); and as SOHMA's selector
   mechanism — `select_chakra_7()` deterministically maps a numerology-reduced
   number (day/week/month) onto one of the seven chakras for the day's cosmic
   report.

6. **Exercises**
   - *Chakra Body Scan* (Beginner) — 10-minute guided scan moving attention from
     Root to Crown, noting sensation, ease, or resistance at each center without
     trying to change anything.
   - *Daily Chakra Draw* (Beginner) — each morning, use SOHMA's numerology-based
     selection (or a simple random draw) to choose one of the seven chakras as the
     day's "theme," and journal at day's end on where that theme showed up.
   - *Color-Frequency Pairing* (Intermediate) — for one center per week, spend 5
     minutes visualizing its color while listening to its paired frequency (from
     the table above), then journal the felt difference vs. a neutral baseline.
   - *Chakra Affirmation Cycle* (Intermediate/Advanced) — work through SOHMA's
     seven affirmations (one per center) over a week, one per day, noticing which
     affirmations land easily and which create resistance — resistance is data,
     not failure.

7. **Reflection Questions**
   - Which of the seven centers, described in plain language (stability,
     creativity, will, love, expression, intuition, unity), feels most "online"
     for me this week — and which feels least available?
   - If I had to address only one of these seven themes this month, which would
     have the biggest downstream effect on the others?
   - Where in my body do I actually *feel* something when I read each center's
     theme — and where do I feel nothing?

8. **Client Applications** — Beginner: Chakra Body Scan + glossary of the seven
   centers · Intermediate: Daily Chakra Draw + Color-Frequency Pairing as a 7-week
   rotation · Advanced: Chakra Affirmation Cycle integrated with journaling ·
   Mastery: using the seven-center frame as a diagnostic lens in coaching sessions
   (Professional Development → Client Applications, `Type = Coaching Protocol`).

9. **Related Subjects** — The Twelve-Center Extended Energy Body; The 24 Chakra
   Gates; Solfeggio Frequencies in Practice; Chakra Balancing & Diagnostic
   Frameworks; (cross-school)
   [`SCHOOL_OF_NATURAL_INTELLIGENCE.md`](SCHOOL_OF_NATURAL_INTELLIGENCE.md) —
   Embodiment & Somatic Intelligence.

10. **Research Notes** — SOHMA cosmic report archive
    (`cosmic_reports/<period>/<date>/data.json`, `Type = Internal Observation`,
    `Owner Agent = SOHMA`) — each report's selected chakra-of-the-day is a
    time-series data point for eventually testing whether self-reported state
    correlates with the assigned chakra theme. `Confidence Level = Hypothesis`
    until a Lumiaion Observatory promotion pipeline run has accumulated enough
    entries.

11. **Content Opportunities** — Article: *"The Seven Chakras, Decoded: Color,
    Frequency, Theme"* (a plain-language primer using the table in §4); Carousel
    series: one post per chakra, pairing the color, the Hz value, and a one-line
    practice; Podcast topic: *"What SOHMA 'Sees' When It Picks Your Chakra of the
    Day."*

12. **Resources** — Arthur Avalon (John Woodroffe), *The Serpent Power* (translation
    of the *Sat-Cakra-Nirupana*, 1919) — primary historical text; Anodea Judith,
    *Wheels of Life: A User's Guide to the Chakra System* (1987) and *Eastern Body,
    Western Mind* (1996) — the modern Western synthesis this Study's framework
    draws on; `soma_v1_virtual/chakra_system.py` (`CHAKRAS_7`) — the internal
    implementation reference. All Research Vault `Type = External Source` except
    the code reference, which is `Type = Internal Observation`.

---

### ⭐ Schumann Resonance: The Planet's Pulse

**Flagship = ✅**

1. **Definition** — The study of the Schumann resonance — a set of extremely
   low-frequency electromagnetic resonances of the Earth-ionosphere cavity, with a
   fundamental near 7.83 Hz and a harmonic series above it — as both a measurable
   geophysical phenomenon and, in SOHMA's implementation, the basis for a daily
   *symbolic* reading of the planetary energetic field, modulated by real NOAA
   space-weather data.

2. **Historical Context** — The resonance is named for physicist Winfried Otto
   Schumann, who predicted it mathematically in 1952; it was first measured in the
   late 1950s/early 1960s. It arises because the space between the Earth's surface
   and the conductive ionosphere forms a cavity that resonates at wavelengths
   corresponding to the Earth's circumference, with a fundamental mode near 7.83 Hz
   and harmonics around 14.3, 20.8, 27.3, and 33.8 Hz — values SOHMA encodes
   directly as `SCHUMANN_HARMONICS_HZ`. In the 1990s–2000s, the Schumann resonance
   was widely adopted in wellness and New Age contexts as a "frequency of the
   Earth" associated with relaxation, meditation states, and human brainwave
   activity (the 7.83 Hz figure sits near the boundary between alpha and theta EEG
   bands) — a connection that is suggestive but not established as direct
   causation, and is treated here as `Confidence Level = Hypothesis`.

3. **Core Principles**
   - The Schumann fundamental (~7.83 Hz) is a **real, measured geophysical
     constant** — this part of the Study is empirical, not symbolic.
   - **No public live data feed for the Schumann resonance exists** at the
     consumer level — SOHMA's daily "reading" is explicitly a *deterministic
     symbolic estimate* (seeded from the date, modulated by the day's NOAA Kp
     index), not a live sensor value. This distinction must always be stated
     alongside any Schumann content this school produces (see
     `soma_v1_virtual/space_weather.py`, `SCHUMANN_METHOD_NOTE_FR`).
   - **Geomagnetic activity (Kp index) and solar activity (X-ray flares) ARE
     measured live** by NOAA SWPC and are the *real* data inputs SOHMA uses to
     modulate its symbolic Schumann reading and to generate independently
     verifiable "space weather" reports.
   - Whatever correlation may or may not exist between planetary field conditions
     and human state, **self-tracking is the only honest way to test it for a
     given individual** — this Study exists to make that tracking possible, not to
     assert the conclusion in advance.

4. **Frameworks** —
   - **The Schumann Reading Model**: base frequency 7.83 Hz → harmonic series
     [7.83, 14.3, 20.8, 27.3, 33.8] Hz → daily symbolic jitter (date-seeded) →
     swing amplitude scaled by the day's Kp index → `field_intensity` level
     (Calm Field / Active Field / Elevated Field / Highly Charged Field), each with
     a plain-language interpretation.
   - **The Space Weather Triad**: (1) Kp planetary geomagnetic index (NOAA
     `planetary_k_index_1m.json`) → 5-level scale from "Calm" to "Strong/Severe
     Storm"; (2) GOES X-ray solar flare classification (A/B/C/M/X, with magnitude)
     → 24-hour flare summary; (3) G-scale 3-day storm outlook
     (`noaa-scales.json`). All three feed SOHMA's daily/weekly/monthly cosmic
     reports.

5. **Applications** — The Space Weather Triad is read each morning by SOHMA as
   part of its cosmic report generation; the `field_intensity` level (and the Kp
   level/interpretation) becomes a plain-language note in Lumiaion Observatory
   entries (`Chakra / Frequency` multi-select field) and can inform a day's
   recommended energy-hygiene practice (cross-link to **Grounding & Clearing
   Practices**).

6. **Exercises**
   - *Field Check-In* (Beginner) — each morning, before checking SOHMA's report,
     write down a 1–10 self-rating of energy/mood/focus. After checking the
     report, note the day's `field_intensity` and Kp level. Do not try to make
     them match — just log both.
   - *Schumann Harmonic Listening* (Beginner/Intermediate) — listen to a 7.83 Hz
     (or harmonic) audio tone for 10 minutes during a quiet sit, paired with the
     *Field Check-In* journaling.
   - *30-Day Space Weather Log* (Intermediate/Advanced) — over 30 days, log Kp
     index, flare activity, and a personal state rating; at the end of the month,
     review for any patterns — the exercise's value is in the *practice of
     looking*, regardless of what is or isn't found.
   - *Grounding on High-Kp Days* (All levels) — on days SOHMA reports
     "Tempête modérée" or higher, deliberately apply one grounding practice from
     **Grounding & Clearing Practices** and note the felt effect.

7. **Reflection Questions**
   - Did today's reported field intensity match, contradict, or have no
     relationship to how I actually felt? What does "no relationship" tell me, if
     anything?
   - If the Schumann reading is symbolic rather than a live measurement, what is
     its value to me — as a ritual anchor, a journaling prompt, something else?
   - On a day with elevated solar/geomagnetic activity, what would "grounding"
     concretely look like for me — and did I do it?

8. **Client Applications** — Beginner: Field Check-In as a simple morning habit ·
   Intermediate: Schumann Harmonic Listening paired with check-in · Advanced: 30-Day
   Space Weather Log with end-of-month review · Mastery: designing a client-facing
   "energy weather" briefing format that clearly separates measured data (Kp,
   flares) from symbolic framing (Schumann reading) — a template for honest
   communication about energetic content.

9. **Related Subjects** — Reading Space Weather: Kp Index & Solar Flares; The
   Biofield Hypothesis; Geomagnetic Sensitivity & Self-Tracking; Solfeggio
   Frequencies in Practice; (cross-school)
   [`SCHOOL_OF_NATURAL_INTELLIGENCE.md`](SCHOOL_OF_NATURAL_INTELLIGENCE.md) —
   Circadian/Lunar/Seasonal Rhythms.

10. **Research Notes** — SOHMA's daily cosmic report archive is the primary
    Research Vault feed (`Type = Internal Observation`, `Reliability = Personal
    Experiment` until aggregated). The NOAA endpoints themselves
    (`services.swpc.noaa.gov/json/planetary_k_index_1m.json`,
    `.../goes/primary/xray-flares-7-day.json`, `.../products/noaa-scales.json`) are
    `Type = External Source`, `Reliability = Empirical`.

11. **Content Opportunities** — Article: *"Is the 'Schumann Resonance' Real? What
    SOHMA Actually Measures vs. Estimates"* — an honesty-first explainer; Weekly
    content series: "This Week's Space Weather" summarizing Kp/flare data in plain
    language; Course module: "Reading Your Own Energy Against the Planet's" (Field
    Check-In + 30-Day Log as a guided cohort exercise).

12. **Resources** — Schumann, W.O., "Über die strahlungslosen Eigenschwingungen
    einer leitenden Kugel..." (1952) — the original theoretical prediction; NOAA
    Space Weather Prediction Center, public JSON endpoints (Kp index, GOES X-ray
    flares, NOAA scales) — live empirical data sources;
    `soma_v1_virtual/space_weather.py` — internal implementation reference
    (`SCHUMANN_METHOD_NOTE_FR`, `KP_LEVELS`, `FLARE_SUMMARIES_FR`). All Research
    Vault `Type = External Source` except the code reference (`Type = Internal
    Observation`).

---

## 4. Domain Tag Additions

This school relies almost entirely on the existing Global Taxonomy. No new Domain
Tags are required:

- `Energy & Frequency` (existing) — primary tag for nearly every Subject/Study in
  this school.
- `Chakra System` (existing) — used across §2's Chakra System & Subtle Anatomy
  branch.
- `Cosmology & Cycles` (existing) — used for Schumann/space-weather and lunar
  Studies.
- `Practice`, `Embodiment`, `Shadow Work` (existing, from the pilot's additions) —
  used for breath and energy-hygiene Studies.

**No new tags introduced by this school.**

---

## 5. Relations

### Within-school wiring (examples)

| Relation | From → To | Type |
|---|---|---|
| Frequency bridge | The Seven-Chakra System → Solfeggio Frequencies in Practice | Related Subjects (the shared Hz table in §3 is the literal edge) |
| Field-to-practice | Schumann Resonance: The Planet's Pulse → Grounding & Clearing Practices | Related Subjects (high-Kp days trigger grounding practice) |
| Subtle-anatomy convergence | Chakras Across Traditions ↔ Comparative Subtle Anatomy ↔ Nadis & the Yogic Subtle Body | Related Subjects (three Studies converging on "what is the subtle body, really") |
| Breath as the bridge | Pranayama & Breath as Energy Technology → Energetic Boundaries: A Working Model | Related Subjects (breath as the first-line tool for boundary/grounding work) |
| Lunar continuity | The Lunar Body: Cycles & Subtle Rhythm → Solar Cycles & Long-Range Rhythms | Related Subjects (short-cycle and long-cycle rhythm Studies) |

### Cross-school relations

| Relation | From → To | Type |
|---|---|---|
| Lumiaion core | The Seven-Chakra System; Schumann Resonance: The Planet's Pulse ↔ [`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md`](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md) §6 (SOHMA runtime table) | Schools DB → Related Schools — this school is SOHMA's primary content home, and SOHMA's daily reports are Lumiaion's live sensory feed for "what is the energetic field doing today" |
| Metaphysical Consciousness | Schumann Resonance: The Planet's Pulse ↔ [`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`](SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md) "States of Consciousness" (theta/meditative states near the Schumann band) | Related Subjects |
| Natural Intelligence | The Lunar Body: Cycles & Subtle Rhythm ↔ [`SCHOOL_OF_NATURAL_INTELLIGENCE.md`](SCHOOL_OF_NATURAL_INTELLIGENCE.md) "Circadian Rhythm as Energetic Foundation" | Related Subjects |
| Ancient Wisdom | Subtle Body Mapping (Auras, Meridians, Nadis) ↔ [`SCHOOL_OF_ANCIENT_WISDOM.md`](SCHOOL_OF_ANCIENT_WISDOM.md) "Vedantic & Eastern Philosophy" | Related Subjects |

---

## 6. Views

This school applies the pilot's view set verbatim — Department Map (grouped by
`Parent Subject`), Glossary, Flagship Subjects, Practice Library by Level,
Reflection Question Bank, Research Threads, Content Pipeline, and Cross-School
Bridges — exactly as defined in
[`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md#building-a-new-school--checklist) §6 and
demonstrated in
[`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`](SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md)
§8. Only `School = School of Energetic Sciences` changes in every filter; no view
mechanics are redefined here. One additional saved filter is recommended for
**Research Threads**: `Owner Agent = SOHMA` as a default sort, since this school's
Research Vault rows are dominated by SOHMA's cosmic report stream.

---

## 7. How This School Connects to LUMIAION

1. **Feeds Lumiaion** — SOHMA's daily/weekly/monthly cosmic reports
   (`cosmic_reports/<period>/<date>/data.json`) are structured Research Vault rows
   the moment they're synced (`Type = Internal Observation`, `School = Energetic
   Sciences`, `Owner Agent = SOHMA`) — this school is the steadiest, highest-volume
   data feed into the Archives of any school, because it runs on a schedule rather
   than waiting on manual content creation.

2. **Lumiaion reads this** — via `Domain Tags: Energy & Frequency, Chakra System,
   Cosmology & Cycles` and `Owner Agent = SOHMA`; the Seven-Chakra frequency table
   (§3) and the Space Weather Triad (§3) are the two machine-legible "lookup
   tables" Lumiaion can join against any Observatory entry that carries a
   `Chakra / Frequency` tag.

3. **Connects to transformation** — the *Field Check-In* and *30-Day Space Weather
   Log* exercises (§3) are explicitly designed to generate L7 evidence: each
   carries `Transformation Markers` describing the self-report/field-data pairing,
   which Lumiaion Observatory `Entry Type = Transformation Log` rows can
   corroborate or fail to corroborate — closing the loop on whether `Confidence
   Level = Hypothesis` claims (e.g., "elevated Kp correlates with reported
   emotional intensity") should be revised.

4. **Converts to action/insight/service** — via the Client Portal (Field Check-In →
   Chakra Affirmation Cycle → 30-Day Space Weather Log as a Beginner→Advanced
   progression), and via Content Opportunities into a recurring "weekly space
   weather" content series — a low-effort, high-frequency content pipeline that
   doubles as a public-facing demonstration of LUMIAION's live data integration.
