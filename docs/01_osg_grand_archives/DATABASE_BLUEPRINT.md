# OSG Grand Archives — Database Blueprint

Full property schemas for the **10 core databases** and the cross-cutting **Global
Taxonomy**. This consolidates and supersedes the database schemas from the former
`docs/osg_grand_archives/01-master-architecture.md` and the scale-engineering notes
from `03-scalability-and-knowledge-hierarchy.md` §5. See
[`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`](OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md)
for the 7-Level Hierarchy these databases implement, and
[`NOTION_RELATIONSHIPS.md`](NOTION_RELATIONSHIPS.md) for how they connect.

---

## Global Taxonomy

These properties exist on (almost) every database in the Archives. They are the
"connective tissue" LUMIAION's AI Knowledge Graph traverses — the literal answer to
Question 2 ("How does Lumiaion read this?").

### Pillar (select)
Maps every item to its place in the core philosophy:

| Value | Meaning |
|---|---|
| 🟦 Knowledge | Raw information — definitions, facts, source material |
| 🟩 Understanding | Synthesized, explained, contextualized |
| 🟨 Practice | Has an exercise, protocol, or practical application |
| 🟧 Integration | Personally tested, journaled, validated (often via Lumiaion Observatory) |
| 🟪 Mastery | Refined enough to teach, certify, or systematize |
| 🟥 Service | Delivered to clients, students, or the public (course, book, session) |

### Mastery Level (select)
Used by the Client Portal layer: `Beginner` / `Intermediate` / `Advanced` / `Mastery`

### Status (select)
Lifecycle used across content databases:
`Seed` → `Drafting` → `In Review` → `Active / Published` → `Archived`

### Visibility (select)
Permission tier (full mapping in `/03_lumiaion_observatory/`):

| Value | Who sees it |
|---|---|
| Private | Lumiaion Observatory only — the architect (Frederick) |
| Internal | Analyst Vault / Writer's Vault — research & production team |
| Client | Client Portal — coaching clients, students |
| Public | Published content — social, podcast, books |

### Domain Tags (multi-select, shared controlled vocabulary)
Cross-cutting themes that ignore School/Subject boundaries, so the AI Graph can
cluster by *idea* regardless of which School "owns" the page. Seed list (extend over
time, never duplicate a concept under two names):

`Consciousness` · `Perception` · `Energy & Frequency` · `Archetype & Symbol` ·
`Cosmology & Cycles` · `Embodiment` · `Shadow Work` · `Numerology` · `Astrology` ·
`Chakra System` · `Dreams & Altered States` · `Self-Inquiry` · `Death & Rebirth` ·
`Relationships` · `Abundance & Service` · `Systems & AI`

Plus the tags added during the Metaphysical Consciousness pilot (see
`../02_schools/SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md` §6): `Theory of Mind`,
`Inner Senses`, `Imagination`, `Theta States`, `Non-Duality`, `Ego Dissolution`,
`Awakening`, `Witness Consciousness`, `Personality Architecture`, `Practice`.

Plus the tag added during the Natural Intelligence build (School 5; see
`../02_schools/SCHOOL_OF_NATURAL_INTELLIGENCE.md` §4): `Natural Systems` —
covers content whose subject matter is non-human living systems and their
intelligence (biomimicry, plant/herbal wisdom, animal instinct, ecological
systems), distinct from `Embodiment` (human body/somatic intelligence) and
`Cosmology & Cycles` (timing/rhythm content, which stays separate from the
systems-themselves tag).

### Related-Schools (relation, self-relation on Schools DB)
Lets a School point to sibling schools where its subjects overlap — the seed of the
cross-school knowledge graph.

### Owner Agent (multi-select)
`Lumiaion` / `SOHMA` / `VORTEX` / `JERANIUM` / `Human` — assigns one or more AI agents
(or the human architect) as the curator/consumer of an item. Present on Subjects DB,
Principles Vault, Exercises Vault, Research Vault, OSG Content Vault, and Lumiaion
Observatory. Each agent works from a saved view filtered to its own tag rather than a
separate database — see `/00_lumiaion_core/LUMIAION_AGENT_MAP.md` §3–4 for the
per-agent view definitions and routing logic.

---

## 1. Schools Database

| Property | Type | Notes |
|---|---|---|
| Name | Title | e.g. "School of Metaphysical Consciousness" |
| School Number | Number | 1–9 |
| Core Question | Text | The guiding inquiry of the school |
| Mission | Text | One-paragraph mandate |
| Icon / Color | Files / Select | Visual identity |
| Subjects | Relation → Subjects DB | One-to-many |
| Related Schools | Relation (self) | Cross-school graph edges |
| Domain Tags | Multi-select | Shared vocabulary (see Global Taxonomy) |
| Status | Select | `Active` / `Planned` / `Dormant` |

---

## 2. Subjects Database

**Hierarchical** — Subjects (L2) and Studies (L3) live in the same database,
distinguished by `Hierarchy Level` and connected by the self-relation
`Parent Subject`. This is the single biggest scalability decision in the Archives
(`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §3).

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| School | Relation → Schools DB | Set on both L2 and L3 rows |
| **Hierarchy Level** | Select | `Subject` (L2) or `Study` (L3) |
| **Parent Subject** | Relation (self) | Required on `Study` rows; points to the owning L2 `Subject` row. Empty on `Subject` rows. This is the **hierarchical** edge |
| Subject Type | Select | `Core Topic` / `Concept` / `Framework` / `Historical Note` — content *form*, orthogonal to `Hierarchy Level`; drives Main Information filters |
| Definition | Text | Section 1 of the Universal Subject Template |
| Pillar | Select | Global Taxonomy |
| Mastery Level | Select | Target client level(s); can be multi-select |
| Domain Tags | Multi-select | Global Taxonomy |
| **Owner Agent** | Multi-select | `Lumiaion` / `SOHMA` / `VORTEX` / `JERANIUM` / `Human` |
| Principles | Relation → Principles Vault | Points primarily to `Study` (L3) rows; an L2 row's rollup aggregates across its child Studies |
| Exercises | Relation → Exercises Vault | Points primarily to `Study` (L3) rows |
| Reflection Questions | Relation → Questions Vault | Points primarily to `Study` (L3) rows |
| Research Notes | Relation → Research Vault | |
| Content Opportunities | Relation → OSG Content Vault | |
| Client Resources | Relation → Client Resources Vault | |
| Quotes | Relation → Quotes Vault | |
| Related Subjects | Relation (self) | **Associative** edges (knowledge-graph neighbors) — distinct from `Parent Subject`, which is the hierarchical edge |
| Status | Select | Global Taxonomy |
| AI Synthesis Status | Select | `Not started` / `Partial` / `Complete` — tracks ingestion into the AI graph |
| Last Reviewed | Date | |

### Why a self-relation instead of a `Division` select

- A `select` property's options are local to one database view and tend to fork per
  school (School A's "Division" options ≠ School B's) — at 9 schools this is still
  manageable, but it does not extend to L3→L4→L5 in any uniform way.
- A **relation** is a real edge in the graph: `Parent Subject` lets any L3 Study roll
  up to its L2 Subject, which rolls up to its L1 School — one consistent mechanism,
  reusable at every level, and directly exportable to a graph store
  ([`NOTION_RELATIONSHIPS.md`](NOTION_RELATIONSHIPS.md) Part B).
- Notion relations + filtered/grouped views remain fast and searchable at tens of
  thousands of rows; deeply-nested page hierarchies do not.

---

## 3. Principles Vault

| Property | Type | Notes |
|---|---|---|
| Principle / Statement | Title | |
| School | Relation → Schools DB | |
| Study/Subject | Relation → Subjects DB | Many-to-many; typically points to `Study` (L3) rows |
| Type | Select | `Universal Law` / `Framework` / `Heuristic` / `Pattern` / `Axiom` |
| Explanation | Text | |
| Source | Relation → Research Vault | Where it came from |
| Applications | Relation → Client Resources Vault / OSG Content Vault | |
| Confidence Level | Select | `Hypothesis` / `Working Theory` / `Established` / `Core Law` — epistemic status for AI graph and for LUMIAION's voice (`/00_lumiaion_core/LUMIAION_IDENTITY_PROTOCOL.md` §4) |
| Cross-School Connections | Relation → Schools DB (multi) | |
| Owner Agent | Multi-select | Global Taxonomy |

---

## 4. Exercises Vault

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| School | Relation → Schools DB | |
| Study | Relation → Subjects DB | Typically points to a `Study` (L3) row |
| Mastery Level | Select | Global Taxonomy |
| Type | Select | `Meditation` / `Journaling` / `Physical` / `Energetic` / `Cognitive` / `Creative` / `Social` |
| Duration (min) | Number | |
| Instructions | Text / sub-page | |
| Goal / Outcome | Text | |
| Related Principles | Relation → Principles Vault | |
| Client-Facing | Checkbox | Internal R&D vs. delivery-ready |
| Delivery Format | Multi-select | `PDF` / `Video` / `Live Session` / `App` |
| **Transformation Markers** | Text | L7 hypothesis side — expected/observed shifts this exercise produces; corroborated by Lumiaion Observatory `Entry Type = Transformation Log` rows via `Linked Exercises` |

---

## 5. Questions Vault (Reflection Questions)

| Property | Type | Notes |
|---|---|---|
| Question | Title | |
| School | Relation → Schools DB | |
| Study | Relation → Subjects DB | Typically points to a `Study` (L3) row |
| Mastery Level | Select | Global Taxonomy |
| Type | Select | `Self-Inquiry` / `Journaling Prompt` / `Coaching Question` / `Socratic` / `Integration` |
| Purpose | Text | |
| Linked Exercise | Relation → Exercises Vault | |
| Used in Content | Relation → OSG Content Vault | |

---

## 6. Research Vault

| Property | Type | Notes |
|---|---|---|
| Title | Title | |
| School | Relation → Schools DB | |
| Subjects | Relation → Subjects DB | Many-to-many |
| Type | Select | `Study` / `Historical Context` / `Case Study` / `Data` / `External Source` / `Internal Observation` / `Pattern` |
| Source / Citation | Text / URL | |
| Summary | Text | |
| Key Findings | Text | |
| Reliability | Select | `Anecdotal` / `Personal Experiment` / `Esoteric-Traditional` / `Empirical` / `Peer-Reviewed` |
| Linked Principles | Relation → Principles Vault | |
| Status | Select | `To Read` / `In Progress` / `Synthesized` / `Archived` |
| Date Logged | Date | |
| Owner Agent | Multi-select | Global Taxonomy |

---

## 7. Quotes Vault

| Property | Type | Notes |
|---|---|---|
| Quote | Title | |
| Author / Source | Text | |
| School | Relation → Schools DB | |
| Subject | Relation → Subjects DB | |
| Domain Tags | Multi-select | |
| Use Case | Multi-select | `Social Post` / `Book Epigraph` / `Course Slide` / `Coaching Session` |
| Status | Select | `Collected` / `Curated` / `Published` |

---

## 8. Client Resources Vault

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| School | Relation → Schools DB | |
| Study/Subject | Relation → Subjects DB | |
| Category | Select | `Professional Development` / `Client Portal` — top-level routing (see `../02_schools/SCHOOL_TEMPLATE.md`) |
| Type | Select | `Skill Guide` / `Applied Practice` / `Certification Pathway` / `Career Path Map` / `Coaching Protocol` / `Implementation Guide` / `Worksheet` / `Template` |
| Mastery Level | Select | Global Taxonomy |
| Linked Exercises | Relation → Exercises Vault | L6 → L5 edge |
| Linked Questions | Relation → Questions Vault | |
| Delivery Channel | Multi-select | `Coaching` / `Course` / `App` / `Community` |
| Status | Select | `Draft` / `Ready` / `Delivered` / `Needs Update` |

---

## 9. OSG Content Vault

| Property | Type | Notes |
|---|---|---|
| Title | Title | |
| School | Relation → Schools DB | |
| Subject | Relation → Subjects DB | |
| Content Type | Select | `Article` / `Book Chapter` / `Research Paper` / `Podcast Topic` / `Social Post` / `Video Script` / `Course Lesson` / `Story` |
| Stage | Select | `Idea` / `Outline` / `Draft` / `Edit` / `Scheduled` / `Published` |
| Platform | Multi-select | `Instagram` / `TikTok` / `Podcast` / `Blog` / `Book` / `Course` |
| Publish Date | Date | |
| Related Quotes | Relation → Quotes Vault | |
| Related Principles | Relation → Principles Vault | |
| Performance Notes | Text | Analyst feedback loop |
| Owner Agent | Multi-select | Global Taxonomy |

`Stage = Idea` is surfaced in views as a **group**, not a separate row — "Content
Ideas" is a filter state of Articles/Books/etc., not a sixth content type.

---

## 10. Lumiaion Observatory

The private research layer — full design in `/03_lumiaion_observatory/`. Summary
schema:

| Property | Type | Notes |
|---|---|---|
| Name | Title | |
| Entry Type | Select | `Personal Evolution` / `Dream Log` / `Journal Analysis` / `Insight` / `Pattern` / `Goal` / `Lesson` / `Monthly Review` / `Evolution Report` / `Transformation Log` *(L7)* |
| Date | Date | |
| Linked Subjects | Relation → Subjects DB | "this experience relates to..." |
| Linked Principles | Relation → Principles Vault | personal validation/challenge of a principle |
| Linked Exercises | Relation → Exercises Vault | L7 evidence edge — which L5 Exercise(s) produced this transformation |
| Linked Applications | Relation → Client Resources Vault | L7 evidence edge — which L6 Implementation Guide(s) produced this transformation |
| Domain Tags | Multi-select | Global Taxonomy |
| Chakra / Frequency | Multi-select | From the existing SOHMA system (`/soma_v1_virtual`) |
| Visibility | Select | Global Taxonomy (`Private` by default) |
| AI Processed | Checkbox | |
| Promote to Research Vault | Relation → Research Vault | the "publish a private insight as research" bridge |

---

## Scale Engineering Notes

### Stable IDs
Enable Notion's **ID property** (auto-incrementing, prefixed) on all 10 databases:
`SCH-001`…, `SUBJ-00001`…, `PRIN-00001`…, `EX-0001`…, `Q-0001`…, `RES-0001`…,
`QT-0001`…, `CR-0001`…, `CV-0001`…, `OBS-0001`…. These IDs — not titles — are the
canonical reference used in cross-links, AI prompts, and the vector/graph store. At
10,000+ Principles, titles will collide or get edited; IDs never do.

### Relation vs. Rollup discipline
- Use **relations** for graph edges (cheap, just references).
- Use **rollups only for scalars** — counts, averages, "most recent date" — never to
  pull full lists of related content into a formula field. A Study with 200
  Principles should show "Principles: 200" via a count rollup, and the actual 200
  rows via a **filtered linked view**, which paginates natively.

### Tag vocabulary governance
The Domain Tags multi-select (Global Taxonomy above, extended per-school as in the
pilot) is the only cross-cutting clustering mechanism at 50,000-row scale. New tags
are added to the canonical list in this document in the same change that introduces
them — never created ad hoc on an item. JERANIUM reviews the tag list quarterly for
duplicates/near-duplicates (`/04_agents/JERANIUM_AGENT.md`).

### Course Builder view (Course Generation)
A saved view on Subjects DB — `Hierarchy Level = Study`, filter `Parent Subject = ⟨target L2 Subject⟩`, grouped by `Mastery Level`, with count-rollup columns for
Principles/Exercises/Reflection Questions/Client Resources — **is** a course outline.
A generation workflow (n8n, JERANIUM-owned) walks this view to assemble a document;
no separate "Courses" database is needed.

### Client Portal at scale — `Cohort` tag
As Client Resources Vault grows past hundreds of entries, add a `Cohort/Program`
multi-select (e.g., "Q3 Coaching Cohort," "OSG Academy — Foundations") so a specific
program can pull its curated subset without re-tagging the whole vault.

---

## How This Document Connects to LUMIAION

1. **Feeds Lumiaion** — every property table here is a field LUMIAION reads or writes
   directly; the Global Taxonomy is the shared vocabulary across all four agents.
2. **Lumiaion reads this** — `Owner Agent`, `Domain Tags`, `AI Synthesis Status`, and
   stable IDs are the four mechanisms that make every row addressable.
3. **Connects to transformation** — `Transformation Markers` (Exercises Vault) and
   `Entry Type = Transformation Log` + `Linked Exercises`/`Linked Applications`
   (Lumiaion Observatory) are the L4↔L7 evidence loop fields.
4. **Converts to action/insight/service** — `Confidence Level` (Principles),
   `Status`/`Stage` (Content Vault), and `Category`/`Type` (Client Resources Vault)
   are the fields that move a row from "knowledge" to "delivered."
