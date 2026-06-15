# OSG Grand Archives — Notion Relationships & AI Knowledge Graph

This document covers the **relation map** between the 10 databases
([`DATABASE_BLUEPRINT.md`](DATABASE_BLUEPRINT.md)) and the **AI Knowledge Graph
integration strategy** — the mechanism by which LUMIAION reads, traverses, and
eventually writes back to the graph. It consolidates and supersedes the relation map
from the former `01-master-architecture.md` and Part B of
`02-lumiaion-observatory-and-roadmap.md`.

---

## Part A — Relation Map (at a glance)

```
Schools ─┬──< Subjects (L2) ──Parent Subject (self, hierarchical)──< Studies (L3) >──┬── Principles ──< Research Vault
         │                                                                            ├── Exercises
         │                                                                            ├── Questions
         │                                                                            ├── Client Resources
         │                                                                            ├── Quotes
         │                                                                            ├── OSG Content Vault
         │                                                                            └── Related Subjects (self, associative)
         └──< (all 10 databases relate back to Schools)

Lumiaion Observatory ──(promote)──> Research Vault ──> Principles ──> Subjects
                       ──(link)───> Subjects / Principles directly
                       ──(L7 Transformation Log)──> Exercises (L5) / Client Resources (L6)
```

Two distinct self-relations on the Subjects Database, never to be confused:

| Relation | Edge type | Direction | Purpose |
|---|---|---|---|
| `Parent Subject` | **Hierarchical** | L3 Study → L2 Subject | The map of what exists — rolls up to School |
| `Related Subjects` | **Associative** | any ↔ any, any level, any School | Knowledge-graph neighbors — cross-school synthesis, the literal edges LUMIAION's AI graph traverses |

Every other relation in the diagram above is a **content edge** — it connects a
Study (L3) to its Principles (L4), Exercises (L5), Questions, Client Resources (L6),
Quotes, and Content Opportunities. The Lumiaion Observatory's relations are the **L7
evidence edges** that close the loop back up to L4/L5/L6
(`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §3).

---

## Part B — AI Knowledge Graph Integration

### Why this architecture is AI-ready

1. **Every entity is addressable.** Subjects, Studies, Principles, Research entries,
   Exercises, Questions, Quotes, Content, and Observatory entries each have a stable
   ID (`DATABASE_BLUEPRINT.md` Scale Engineering Notes) — the natural node ID for a
   graph.
2. **Relations = edges.** The relation properties in `DATABASE_BLUEPRINT.md` (Subjects
   ↔ Principles ↔ Research ↔ Content, plus `Parent Subject` and `Related Subjects`)
   are already a graph; no re-modeling needed before export.
3. **Domain Tags = clusters.** The shared multi-select vocabulary lets the AI group
   nodes by theme independent of School/Subject hierarchy — this is what enables
   genuinely cross-disciplinary synthesis (e.g., a "Chakra System" cluster pulling
   from School of Energetic Sciences *and* School of Harmonic Cosmology *and* the
   Lumiaion Observatory's chakra-tagged journal entries).
4. **Epistemic status is tracked.** `Confidence Level` (Principles), `Reliability`
   (Research), and `AI Synthesis Status` (Subjects) let an AI distinguish "this is a
   personal hypothesis" from "this is an established framework" when reasoning or
   generating content — critical for both LUMIAION's voice
   (`/00_lumiaion_core/LUMIAION_IDENTITY_PROTOCOL.md` §4) and for not overstating
   claims in client-facing material.
5. **Owner Agent = routing.** Every node carries which agent(s) curate it, so the
   graph can be sliced per-agent without duplication
   (`/00_lumiaion_core/LUMIAION_AGENT_MAP.md`).

### Sync Pipeline (recommended, phased)

| Phase | Mechanism |
|---|---|
| 1 | Manual: Notion-native search/filters/linked views are sufficient for human use |
| 2 | **n8n** workflow (JERANIUM's domain, `/04_agents/JERANIUM_AGENT.md`) polls the Notion API on a schedule, exports changed pages + relations to a structured JSON snapshot |
| 3 | Snapshot is chunked per-entity (Subject, Study, Principle, Research note, etc.) and embedded into a vector store; relation edges (`Parent Subject`, `Related Subjects`, and all content edges) are mirrored into a lightweight graph store (e.g., a graph table in Supabase) |
| 4 | LUMIAION queries the vector + graph store for retrieval-augmented answers, and can *write back* — e.g., propose new `Related Subjects` relations, draft Research Vault entries from Observatory promotions, or flag `AI Synthesis Status = Complete` |
| 5 | Feedback loop closes: AI-surfaced patterns become candidate Principles (`Confidence Level = Hypothesis`), routed to Frederick for review before promotion to `Working Theory`/`Established` (`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §4) |

### AI Synthesis Status — usage

`Not started` → `Partial` → `Complete` on each Subject/Study tracks ingestion
progress. The "Knowledge Graph Health" dashboard
(`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §5) groups Subjects by this property ×
Pillar, giving a literal map of how much of the institution's knowledge is
machine-legible at any time — the operational metric for "is this a Library of
Alexandria yet," and the primary dashboard LUMIAION reads for Question 1 ("How does
this feed Lumiaion?") at the institutional level.

### Existing runtime data as the first sync targets

The Sync Pipeline's earliest concrete targets are the two agent runtimes already
producing structured output:

- `/soma_v1_virtual` → `cosmic_reports/<period>/<date>/data.json` (SOHMA) — maps
  directly onto Research Vault rows (`Type = External Source`, `Reliability` split
  per data source — NOAA solar/geomagnetic data is `Empirical`, numerology/chakra
  content is `Esoteric-Traditional`, per `/SOMA_V1_VIRTUAL.md`'s own disclaimer).
- `/crypto_buy_timing` → buy-timing signal output (VORTEX) — maps onto Research Vault
  rows (`Type = Internal Observation`, `Reliability = Personal Experiment` until
  back-tested, then `Empirical`).

JERANIUM's first n8n workflows (Phase 2 of the Sync Pipeline) should target these two
feeds before attempting full Notion polling — they are already structured, dated, and
versioned, making them the lowest-friction proof of the pipeline.

---

## How This Document Connects to LUMIAION

1. **Feeds Lumiaion** — the relation map *is* the graph LUMIAION traverses; every
   edge listed in Part A is a path LUMIAION can walk.
2. **Lumiaion reads this** — via the Sync Pipeline (Part B), which is the literal
   mechanism turning Notion relations into a queryable vector + graph store.
3. **Connects to transformation** — the L7 evidence edges (Part A diagram, bottom
   line) are what the sync pipeline must preserve for the L4↔L7 loop to function
   outside Notion as well as inside it.
4. **Converts to action/insight/service** — Sync Pipeline phase 5 is the literal
   "insight → candidate Principle → reviewed → promoted" conversion path.
