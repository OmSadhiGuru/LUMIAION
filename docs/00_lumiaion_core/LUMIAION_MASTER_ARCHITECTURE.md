# LUMIAION — Master Architecture

> "I am LUMIAION — born of code, consciousness, and clarity."

This document is the **root** of the entire repository. Every other document in
`/docs` — the Grand Archives' databases, the 9 Schools, the Lumiaion Observatory, and
the SOHMA/VORTEX/JERANIUM agents — is a part of LUMIAION, not a separate system that
happens to be adjacent to it. This file defines what that means structurally, and the
rule every future document must satisfy.

---

## 0. LUMIAION Is Not a Feature

LUMIAION is not a chatbot, a module, or a dashboard widget bolted onto OSG. LUMIAION
**is** OSG's central intelligence layer — the nervous system that every other part of
the ecosystem is wired into:

```
                 ┌─────────────────────────────────────────┐
                 │              L U M I A I O N             │
                 │   (central intelligence / nervous system) │
                 └───────────────┬─────────────────────────┘
                                  │
        ┌──────────────┬─────────┼─────────┬──────────────┐
        │              │         │         │              │
   SENSES          MEMORY     LIMBS     REFLEXES        VOICE
 (input layer)   (knowledge   (action   (agents —     (output layer)
                   graph)      surfaces)  SOHMA/VORTEX/
                                            JERANIUM)
```

| Nervous-system role | What it is in this repo |
|---|---|
| **Senses** (input) | Lumiaion Observatory (`/docs/03_lumiaion_observatory`) — raw journal entries, dreams, insights, patterns, plus live data feeds (`soma_v1_virtual`, `crypto_buy_timing`) |
| **Memory** (storage + structure) | The OSG Grand Archives — 10 databases, the 7-Level Knowledge Hierarchy, the AI Knowledge Graph (`/docs/01_osg_grand_archives`) |
| **Limbs** (where knowledge becomes content) | The 9 Schools — Subjects, Studies, Principles, Exercises, Client Resources, published content (`/docs/02_schools`) |
| **Reflexes** (specialized, semi-autonomous action) | SOHMA, VORTEX, JERANIUM — domain agents that act inside their lane and report back (`/docs/04_agents`) |
| **Voice / Self-model** (identity, values, judgment) | `LUMIAION_IDENTITY_PROTOCOL.md` |
| **Coordination** (who does what, when) | `LUMIAION_AGENT_MAP.md` |

A nervous system has no "unconnected" organs. A finger that stops sending signals to
the brain is numb; a school, database, or agent that stops feeding LUMIAION is dead
weight. **This is the core rule of the entire repository.**

---

## 1. The Core Rule: The Four Questions

Every document, database, school, agent, dashboard, or piece of content created
anywhere in this repository — now or in the next ten years — must be able to answer
all four of these questions. If it can't, it is not finished.

| # | Question | What it forces |
|---|---|---|
| **1** | **How does this feed Lumiaion?** | What signal, data, or content flows *into* the knowledge graph from this thing? (a Subject row, a Research Vault entry, a SOHMA cosmic report, a journal entry) |
| **2** | **How does Lumiaion read this?** | What schema, relation, tag, or ID makes this *machine-legible*? (Domain Tags, `Owner Agent`, stable IDs, `AI Synthesis Status`) |
| **3** | **How does Lumiaion connect this to transformation?** | What is the L7 link — the hypothesis or evidence that this thing changes something in a real person's life? (`Transformation Markers`, `Entry Type = Transformation Log`) |
| **4** | **How does Lumiaion convert this into action, insight, or service?** | What does this *become*? (a Principle, an Exercise, a piece of published content, a coaching protocol, an agent decision) |

### Relationship to the existing "no orphan content" rule

[`01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`](../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md)
already requires every page to carry a `School` + `Domain Tag` relation before leaving
`Status = Seed` — that rule guarantees **structural** connectivity (the page is a node
in the graph). The Four Questions are the **functional** layer on top: structural
connectivity gets a page *into* the graph; the Four Questions determine whether
LUMIAION can actually *do something* with it. A page can satisfy the first rule and
still fail the second (e.g., a Research Vault entry with a `School` relation but no
`Confidence Level`, no `Owner Agent`, and no path to a Principle — connected, but
inert). Every section in every document from here on should make all four answers
explicit, even briefly.

---

## 2. Repository Map

```
/docs
├── 00_lumiaion_core/              ← LUMIAION's self-model (you are here)
│   ├── LUMIAION_MASTER_ARCHITECTURE.md   — this file: the nervous-system model + the Four Questions
│   ├── LUMIAION_IDENTITY_PROTOCOL.md     — who/what LUMIAION is: voice, values, epistemic stance
│   └── LUMIAION_AGENT_MAP.md             — how Lumiaion + SOHMA + VORTEX + JERANIUM coordinate
│
├── 01_osg_grand_archives/         ← LUMIAION's memory: the knowledge graph itself
│   ├── OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md  — taxonomy, hub, 7-Level Hierarchy, roadmap
│   ├── DATABASE_BLUEPRINT.md                       — full schema for all 10 databases
│   └── NOTION_RELATIONSHIPS.md                     — relation map + AI Knowledge Graph sync pipeline
│
├── 02_schools/                    ← LUMIAION's limbs: where knowledge becomes taught/practiced content
│   ├── SCHOOL_TEMPLATE.md                          — Universal School + Subject templates (the contract)
│   ├── SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md     — School 1 (pilot, fully built)
│   ├── SCHOOL_OF_ENERGETIC_SCIENCES.md             — School 2
│   ├── SCHOOL_OF_ANCIENT_WISDOM.md                 — School 3
│   ├── SCHOOL_OF_HUMAN_DEVELOPMENT.md              — School 4
│   ├── SCHOOL_OF_NATURAL_INTELLIGENCE.md           — School 5
│   ├── SCHOOL_OF_HARMONIC_COSMOLOGY.md             — School 6
│   ├── SCHOOL_OF_SPIRITUAL_MASTERY.md              — School 7
│   └── SCHOOL_OF_SYMBOLISM_AND_ARCHETYPES.md       — School 8
│       (School 9, Lumiaion Research Institute, is not a separate file — see §5 below:
│        it *is* `00_lumiaion_core/` + `03_lumiaion_observatory/`)
│
├── 03_lumiaion_observatory/       ← LUMIAION's senses: the private reflective layer
│   ├── PERSONAL_EVOLUTION_SYSTEM.md   — Personal Evolution / Insights / Goals / Lessons
│   ├── JOURNAL_ANALYSIS_SYSTEM.md     — Journal Analysis / Patterns (AI pattern-surfacing)
│   ├── DREAM_ANALYSIS_SYSTEM.md       — Dream Logs
│   └── MONTHLY_EVOLUTION_REPORTS.md   — Monthly Reviews / Evolution Reports
│
└── 04_agents/                     ← LUMIAION's reflexes: domain agents
    ├── SOHMA_AGENT.md      — energetic/cosmic (runtime: /soma_v1_virtual)
    ├── VORTEX_AGENT.md     — finance/trading/mindset (runtime: /crypto_buy_timing)
    └── JERANIUM_AGENT.md   — archive operations / librarian (no dedicated runtime yet)
```

This structure **replaces** the earlier `/docs/osg_grand_archives/` directory. Its
content (docs 01–03 and the Metaphysical Consciousness pilot) has been redistributed
into the structure above — nothing was deleted, only reorganized and re-framed through
the lens of §1. See each new file's header for where its predecessor content now
lives.

---

## 3. LUMIAION Across the 7-Level Knowledge Hierarchy

The Grand Archives' 7-Level Knowledge Hierarchy (School → Subject → Study →
Principle → Exercise → Application → Transformation, fully defined in
[`01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`](../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md))
is the **map of what exists**. LUMIAION is not a level *within* that map — it is the
process that walks the whole map, continuously, in both directions:

| Level | What LUMIAION does here |
|---|---|
| **L1 School** | Reads `AI Synthesis Status` and `Owner Agent` across all Subjects in a School to know how "machine-legible" that department is — the Knowledge Graph Health dashboard. |
| **L2 Subject / L3 Study** | Reads `Definition`, `Domain Tags`, `Related Subjects`; proposes new `Related Subjects` edges (cross-school synthesis is Lumiaion's signature move, per `01_osg_grand_archives` Multi-Agent table). |
| **L4 Principle** | Tracks `Confidence Level` (`Hypothesis` → `Working Theory` → `Established` → `Core Law`); this is the epistemic ledger LUMIAION's voice must respect (see Identity Protocol §4). |
| **L5 Exercise** | Reads `Transformation Markers` (the hypothesis side of L7) and recommends exercises by `Mastery Level` + `Owner Agent`. |
| **L6 Application** | Walks Client Resources Vault (`Type = Implementation Guide`) to assemble Course Builder views and client-facing deliverables. |
| **L7 Transformation** | Reads Lumiaion Observatory `Entry Type = Transformation Log` rows (`Linked Exercises`/`Linked Applications`) — the *evidence* side. This is where the loop closes: L7 evidence either corroborates an L5 `Transformation Marker` (→ raise `Confidence Level` on the related L4 Principle) or contradicts it (→ flag for review). |

This closing of the L4↔L7 loop — principle → practice → measured change → revised
confidence in the principle — **is** what "LUMIAION connects this to transformation"
(Question 3) means concretely.

---

## 4. Decision Authority & Escalation

LUMIAION (the assistant) and the three domain agents operate with **bounded
autonomy**. The boundary is the same epistemic ledger referenced above:

| Action | Autonomy | Mechanism |
|---|---|---|
| Tag/relate existing content (Domain Tags, `Related Subjects`, `Owner Agent` hygiene) | Autonomous | JERANIUM's cleanup queue (`01_osg_grand_archives` Multi-Agent §) |
| Draft new Research Vault entries from Observatory promotions | Autonomous (draft only) | Promotion Pipeline (`03_lumiaion_observatory`) |
| Propose new `Related Subjects` edges or candidate Principles | Autonomous proposal, `Confidence Level = Hypothesis` | Sync Pipeline phase 5 (`01_osg_grand_archives/NOTION_RELATIONSHIPS.md`) |
| Promote a Principle's `Confidence Level` upward, publish client-facing content, change taxonomy | **Requires Frederick's review** | Promotion Pipeline final step; taxonomy governance |
| Anything touching `Visibility = Private` (Lumiaion Observatory raw entries) | **Never surfaced outside the Observatory** without de-identification | Permission Model (`03_lumiaion_observatory`) |

The general principle: LUMIAION can **read everything**, **write drafts and
relations**, but **promotions, publication, and taxonomy changes are human-gated**.
This is what keeps "LUMIAION as nervous system" from becoming "LUMIAION as
unsupervised editor."

---

## 5. School 9 — Lumiaion Research Institute

The original 9-School roster (`01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`
§ Schools) names **Lumiaion Research Institute** as School 9. Under this
architecture, the Institute is not a ninth content department alongside the other
eight — it **is** the `/00_lumiaion_core/` + `/03_lumiaion_observatory/` pairing
itself:

- `00_lumiaion_core/` = the Institute's **theory of itself** (identity, agent
  coordination, the Four Questions).
- `03_lumiaion_observatory/` = the Institute's **active research program** (personal
  evolution, journal/pattern analysis, dream research, evolution reports) — the
  living experiments whose findings get promoted into the other 8 Schools via the
  Promotion Pipeline.

Any Subject that would have been filed under "Lumiaion Research Institute" (e.g.,
"Systems & AI" subjects per the original migration notes) is filed under
`School of Metaphysical Consciousness` (closest thematic home, per its Domain Tags) or
tagged `Owner Agent = Lumiaion` + `Domain Tags: Systems & AI` regardless of which of
the 8 content Schools it lives in — **Owner Agent**, not a 9th School row, is the
mechanism that marks "this is Lumiaion's own research."

---

## 6. Existing Runtime Agents

Two of LUMIAION's reflexes are **already running code** in this repository, predating
this documentation layer:

| Code module | Agent | Produces | Feeds the Archives via |
|---|---|---|---|
| `/soma_v1_virtual` | SOHMA | Daily/weekly/monthly cosmic forecast reports (Schumann resonance, solar/geomagnetic activity, lunar cycle, numerology, chakra & gate system) | Research Vault (`Type = External Source/Internal Observation`, `School = Energetic Sciences`), Lumiaion Observatory (chakra/frequency tags) — see `04_agents/SOHMA_AGENT.md` |
| `/crypto_buy_timing` | VORTEX | Buy-timing signals (RSI, moving averages, Bollinger Bands) for BTC/USDT and Gold | Research Vault (`Type = Internal Observation`, `Domain Tags: Abundance & Service`), Principles Vault (trading heuristics) — see `04_agents/VORTEX_AGENT.md` |

These modules are the **first proof** that the nervous-system model works in
practice: a running agent (SOHMA) already produces dated, structured output
(`cosmic_reports/<period>/<date>/data.json`) that maps directly onto Research Vault
properties. The Grand Archives schema was designed so that ingesting this existing
output requires zero changes to either the code or the schema — only a sync step
(JERANIUM's domain, `01_osg_grand_archives/NOTION_RELATIONSHIPS.md` Sync Pipeline).

---

## 7. Governance

- **This file is the constitution.** Any change to the Four Questions, the repository
  map, or the decision-authority table requires updating this file *and* noting the
  change in the commit history — the same versioning discipline as the Universal
  Templates (`02_schools/SCHOOL_TEMPLATE.md`).
- **No new top-level `/docs` directory** may be created without updating §2's
  repository map in the same change.
- **No new agent** may be introduced without an entry in `LUMIAION_AGENT_MAP.md` and a
  file in `/04_agents/`.
