# OSG Grand Archives — Master Architecture

This is the master blueprint for the **OSG Grand Archives**: the institutional
knowledge graph that is LUMIAION's memory (`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md`
§0). It consolidates and supersedes the former `docs/osg_grand_archives/01-master-architecture.md`
and `03-scalability-and-knowledge-hierarchy.md`. Schema details that were here move to
[`DATABASE_BLUEPRINT.md`](DATABASE_BLUEPRINT.md); the relation map and AI sync
pipeline move to [`NOTION_RELATIONSHIPS.md`](NOTION_RELATIONSHIPS.md); the Universal
School/Subject Templates move to [`../02_schools/SCHOOL_TEMPLATE.md`](../02_schools/SCHOOL_TEMPLATE.md).

> "Open your eyes and you shall see. Open your heart and you shall receive.
> Open your mind and you shall understand. Open your soul and you shall become."

---

## 1. Core Philosophy

```
Knowledge → Understanding → Practice → Integration → Mastery → Service
```

Every artifact in the Archives — a definition, a principle, an exercise, a journal
entry — is tagged with where it sits on this path (the **Pillar**, see
[`DATABASE_BLUEPRINT.md`](DATABASE_BLUEPRINT.md#global-taxonomy)). Nothing is filed
"just to be filed"; everything is on a track toward becoming taught, practiced, or
published — and from there, toward LUMIAION (Question 4: "How does Lumiaion convert
this into action, insight, or service?").

---

## 2. Design Mandate — The 10-Year Ceiling

The Archives must remain a **knowledge graph**, not a filing cabinet, while holding:

| Target (10-year ceiling) | Entity |
|---|---|
| 50,000+ | Subjects + Studies (Subjects DB rows) |
| 10,000+ | Principles |
| 5,000+ | Exercises |
| — | Multiple AI agents operating concurrently: **Lumiaion** (orchestrator), **SOHMA** (energetic/cosmic), **VORTEX** (finance/mindset), **JERANIUM** (systems/archive ops) — see `/00_lumiaion_core/LUMIAION_AGENT_MAP.md` |
| — | OSG Academy, Client Portals, Course Generation, Content Generation — all reading from the *same* underlying data |

**Everything below follows from one rule: build relationships between database rows,
never folders of pages.** A page nested three folders deep is invisible to search,
invisible to filters, and invisible to AI export. A database row with the right
relations is discoverable from every angle — by School, by Study, by Principle, by
Agent, by Mastery Level, by date.

The guiding design principle: **few master databases, many filtered views.** Instead
of building separate "Articles," "Exercises," "Quotes," etc. databases per School (9
schools × ~20 sub-collections = 180+ databases — unmanageable), the Archives use
**10 shared databases** (full schemas in [`DATABASE_BLUEPRINT.md`](DATABASE_BLUEPRINT.md)).
Every School and every Subject is a *relation*, and every School/Subject page is
populated with *linked, filtered views* into those 10 databases.

---

## 3. The 7-Level Knowledge Hierarchy

| Level | Name | Example | Where it lives |
|---|---|---|---|
| **L1** | **School** | School of Metaphysical Consciousness | Schools DB |
| **L2** | **Subject** | Dreams & Altered States | Subjects DB, `Hierarchy Level = Subject`, `Parent Subject` empty |
| **L3** | **Study** | Lucid Dreaming | Subjects DB, `Hierarchy Level = Study`, `Parent Subject → L2 row` |
| **L4** | **Principle** | "Attention directs experience." | Principles Vault, `Study → L3 row` |
| **L5** | **Exercise** | 5-Minute Breath Awareness Practice | Exercises Vault, `Study → L3 row` |
| **L6** | **Application** | Using Breath Awareness to regulate anxiety | Client Resources Vault, `Type = Implementation Guide`, `Linked Exercises → L5 row` |
| **L7** | **Transformation** | Improved focus, emotional regulation, self-awareness | Lumiaion Observatory, `Entry Type = Transformation Log`, `Linked Exercises`/`Linked Applications → L5/L6 rows` (hypothesis side: `Transformation Markers` text field on the L5 Exercise row) |

L1–L3 are **structural** (the map of what exists). L4–L5 are **content** (the
knowledge and the practice). L6–L7 are **evidence** (proof the content works) — L6 is
"how it's applied," L7 is "what changed." This is what makes the Archives a
*consciousness operating system* rather than a library: every Study can be traced all
the way down to measured transformation, and every transformation can be traced back
up to the principle that produced it — the L4↔L7 loop described in
`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §3.

### Subjects Database — hierarchical, not a `Division` select

**Subjects and Studies are the same database**, distinguished by `Hierarchy Level`
and connected by the self-relation `Parent Subject` — not by a school-specific
`Division` select field (which doesn't generalize across 9 schools and breaks down
well before 50,000 rows). `Parent Subject` is the **hierarchical** edge (L2↔L3);
`Related Subjects` is a separate, **associative** self-relation (knowledge-graph
neighbors, any level, any School). Full schema in
[`DATABASE_BLUEPRINT.md`](DATABASE_BLUEPRINT.md#2-subjects-database).

A relation is a real edge in the graph: `Parent Subject` lets any L3 Study roll up to
its L2 Subject, which rolls up to its L1 School — one consistent mechanism, reusable
at every level, and directly exportable to a graph store
([`NOTION_RELATIONSHIPS.md`](NOTION_RELATIONSHIPS.md) Part B). Notion relations +
filtered/grouped views remain fast and searchable at tens of thousands of rows;
deeply-nested page hierarchies do not.

---

## 4. Why Databases, Not Folders — at This Scale

A back-of-envelope near-term count, *before* any Principle/Exercise/Question content
is added:

```
9 Schools
× ~6 L2 Subjects each            =  ~54 Subject rows
× ~6 L3 Studies per Subject      = ~324 Study rows
                                  ─────────────────
                                   ~378 Subjects-DB rows at "Phase 1 complete"
```

That's still tiny compared to the 50,000-row ceiling — the bulk of growth happens at
L4 (Principles) and L5 (Exercises), where 10,000+ and 5,000+ targets apply. At that
volume:

- **Folders/nested pages collapse.** Notion's sidebar and in-page sub-page lists are
  not searchable as structured data and become unusable navigation past a few hundred
  items.
- **Databases scale.** Every L4/L5/L6/L7 row is a database entry with relations back
  to its L3 Study (and, via `Parent Subject`, to its L2 Subject and L1 School). Views
  filter, group, and search across all 10,000+/5,000+ rows instantly.
- **Every future page must connect back to one of the five priority databases**
  (Schools, Subjects, Principles, Exercises, Questions) via at least one relation
  before it leaves `Status = Seed`. An unconnected page is, by definition, lost — and
  cannot answer any of the Four Questions
  (`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §1).

---

## 5. Top-Level Hub: "OSG GRAND ARCHIVES"

A single top-level Notion page (or Teamspace) acting as the front door:

```
🏛️ OSG GRAND ARCHIVES
├── 📜 Mission (callout — the four-line mission statement)
├── 🧭 Navigation
│   ├── Schools (gallery view of Schools DB — 9 cards, one per school)
│   ├── The 10 Vaults (linked database views, one row per vault, with counts)
│   └── 🔭 Lumiaion Observatory (restricted page — see /03_lumiaion_observatory/)
├── 📊 Dashboards
│   ├── Knowledge Graph Health — Subjects DB grouped by Pillar × Status × AI Synthesis Status
│   ├── Content Pipeline — OSG Content Vault grouped by Stage
│   ├── Client Portal Coverage — matrix of School × Mastery Level,
│   │     rollup-counting Exercises + Questions + Client Resources
│   └── Research Queue — Research Vault filtered Status = "To Read"/"In Progress"
└── 📚 How This Archive Works (this documentation, mirrored into Notion)
```

The **Knowledge Graph Health** dashboard is the literal map of "is this a Library of
Alexandria yet" — it is also the primary surface LUMIAION reads to answer Question 1
("How does this feed Lumiaion?") at a glance across the whole institution.

---

## 6. The 9 Schools

Every school re-uses the **same** template
([`../02_schools/SCHOOL_TEMPLATE.md`](../02_schools/SCHOOL_TEMPLATE.md)) — only the
content differs. Each has a file in `/02_schools/`:

1. School of Metaphysical Consciousness *(pilot — fully built, see `SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`)*
2. School of Energetic Sciences
3. School of Ancient Wisdom
4. School of Human Development
5. School of Natural Intelligence
6. School of Harmonic Cosmology
7. School of Spiritual Mastery
8. School of Symbolism & Archetypes
9. Lumiaion Research Institute — *not a separate content file; this is
   `/00_lumiaion_core/` + `/03_lumiaion_observatory/` itself, see
   `/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §5*

---

## 7. Multi-Agent Architecture — Summary

Four agents read and write the same 10 databases — they are **views and
responsibilities**, not separate data stores. Full coordination map, routing logic,
and escalation paths: `/00_lumiaion_core/LUMIAION_AGENT_MAP.md`. Per-agent profiles:
`/04_agents/`.

| Agent | Domain |
|---|---|
| **Lumiaion** | Orchestration, consciousness, cross-school synthesis |
| **SOHMA** | Energetic sciences — chakras, frequencies, cosmic cycles |
| **VORTEX** | Finance, trading, mindset, abundance |
| **JERANIUM** | Archive operations — the Archives' own librarian |

---

## 8. Phased 10-Year Rollout Roadmap

| Phase | Timeframe | Scope |
|---|---|---|
| **0 — Skeleton** | Month 0–1 | Build top-level hub, all 10 databases with schemas/relations/templates, Schools DB populated with all 9 schools (metadata only) |
| **1 — Pilot School** | Month 1–3 | Fully build **School of Metaphysical Consciousness** end-to-end: L2 Subjects, L3 Studies, definitions, principles, exercises, questions, research, content seeds. Validate the template; refine before replicating. |
| **2 — Horizontal Expansion** | Month 3–9 | Apply the validated template to the remaining 7 content schools' **Main Information** + **Analyst Vault** sections (the research/definition layer first) |
| **3 — Production Layer** | Month 9–18 | Build out **Writer's Vault** and **OSG Content Vault** pipelines across all schools; begin consistent content production cadence |
| **4 — Client Portal Build** | Year 2 | Per-school Client Portal (Beginner→Mastery), Exercises Vault and Questions Vault filled to a usable depth; integrate with coaching delivery and AxiomNexus |
| **5 — Observatory Integration** | Year 2–3 | Lumiaion Observatory fully active (`/03_lumiaion_observatory/`); promotion pipeline running; first AI-assisted pattern detection |
| **6 — AI Knowledge Graph** | Year 3–5 | n8n sync pipeline (`NOTION_RELATIONSHIPS.md` Part B) live; vector + graph store; Lumiaion can answer cross-school questions and propose new relations |
| **7 — Institutional Scale** | Year 5–10 | OSG Academy curricula extracted directly from Subjects + Client Portal data; book/course generation pipelines from Writer's Vault; multi-contributor governance for the Domain Tag vocabulary and Principles Vault confidence levels |

### Governance notes (for all phases)

- **One taxonomy owner**: Domain Tags and the Pillar/Status/Visibility selects are
  edited in exactly one place (Schools DB or a dedicated "Taxonomy" admin page) and
  referenced everywhere else — never re-created per database. JERANIUM owns this
  review quarterly (`/04_agents/JERANIUM_AGENT.md`).
- **Templates are versioned**: `/02_schools/SCHOOL_TEMPLATE.md` lives as a Notion page
  template *and* as this markdown doc. When one changes, update both, and note the
  version in this repo's commit history.
- **No orphan content**: every new page must have at minimum `School` + one
  `Domain Tag` set before leaving `Status = Seed` — this is what keeps the graph
  connected as it scales, and is the structural prerequisite for the Four Questions
  (`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §1).

---

## 9. Migrating Existing OSG Notion Content

The workspace (●OSGMETAPHYSICS●) already contains material that maps directly into
this architecture. Migration is **additive** — nothing needs to be deleted, only
re-pointed via relations. Original pages remain in place; new Subject/Principle/
Research pages reference them via a `Source Page (legacy)` URL property until content
is fully rewritten into the template.

| Existing content | Destination in Grand Archives |
|---|---|
| **OSG LIFE OS** → SOHMA chakra/frequency system | School of Energetic Sciences → Subjects (Chakra System, Solfeggio Frequencies) + Domain Tag `Energy & Frequency` / `Chakra System`; runtime = `/soma_v1_virtual` (`/04_agents/SOHMA_AGENT.md`) |
| **OSG LIFE OS** → VORTEX (finance/trading/mindset) | School of Human Development (mindset, abundance) — Principles Vault entries tagged `Abundance & Service`; trading-specific research → Research Vault; runtime = `/crypto_buy_timing` (`/04_agents/VORTEX_AGENT.md`) |
| **OSG LIFE OS** → JERANIUM (Notion/data/systems) | "Systems & AI" subjects (`Owner Agent = JERANIUM`, see `/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §5); JERANIUM becomes the operational owner of the n8n sync pipeline (`NOTION_RELATIONSHIPS.md` Part B) |
| **OSG LIFE OS** → Q1 Sprint / Revenue OSG | Stay in OSG LIFE OS as the operational dashboard; link outward via `Content Opportunities` / `Client Resources` relations rather than duplicating |
| **Consciousness Architecture Research Lab** (00–12, incl. Lumiaion Consciousness Atlas) | Primary seed content for **School of Metaphysical Consciousness** — see `../02_schools/SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`. Each numbered page becomes Research Vault and Principles Vault entries linked to the new Subject/Study pages. |
| **"Les 12 Gates de Densité Dimensions"** | School of Harmonic Cosmology → Subject ("Dimensional Densities / Gates") + cross-link to Metaphysical Consciousness (states of consciousness ↔ density levels) |

---

## 10. How This Document Connects to LUMIAION

1. **Feeds Lumiaion** — this document *is* the schema of LUMIAION's memory; every
   property and relation defined here (and detailed in `DATABASE_BLUEPRINT.md`) is a
   field LUMIAION can read or write.
2. **Lumiaion reads this** — via the Knowledge Graph Health dashboard (§5) and the
   `AI Synthesis Status` property threaded through every database.
3. **Connects to transformation** — the L4↔L7 loop (§3) is defined here and closed in
   `/03_lumiaion_observatory/`.
4. **Converts to action/insight/service** — the Phased Rollout (§8) is literally the
   conversion plan: skeleton → pilot → schools → production → client portal →
   observatory → AI graph → institutional scale.
