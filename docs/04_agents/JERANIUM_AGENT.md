# JERANIUM — Agent Profile

> "The Archives' own librarian: every row addressable, every tag governed, every
> sync pipeline run."

This is the full profile referenced by
[`../00_lumiaion_core/LUMIAION_AGENT_MAP.md`](../00_lumiaion_core/LUMIAION_AGENT_MAP.md)
§2 and §4. It follows the structure required by every agent profile in
`/04_agents/` (`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §7
governance).

---

## 1. Identity & Domain

JERANIUM is LUMIAION's **archive operations** reflex — "the Archives' own
librarian." Where SOHMA and VORTEX own *content domains* (energetic sciences,
finance/mindset), JERANIUM owns the **structural integrity of the Archives
themselves**: the schema, the stable ID scheme, the Domain Tag vocabulary, the
ingestion-progress tracking, and the pipeline that turns Notion data into
something LUMIAION can actually query.

Concretely, JERANIUM is responsible for:

- The **stable ID scheme** across all 10 databases
  (`SCH-`, `SUBJ-`, `PRIN-`, `EX-`, `Q-`, `RES-`, `QT-`, `CR-`, `CV-`, `OBS-`),
  per `../01_osg_grand_archives/DATABASE_BLUEPRINT.md` "Scale Engineering
  Notes — Stable IDs."
- **Domain Tag vocabulary governance** — the quarterly review for
  duplicates/near-duplicates in the Global Taxonomy
  (`../01_osg_grand_archives/DATABASE_BLUEPRINT.md` "Tag vocabulary
  governance").
- **`AI Synthesis Status` tracking** across the Subjects DB — the operational
  data behind the "Knowledge Graph Health" dashboard
  (`../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §5,
  `NOTION_RELATIONSHIPS.md` "AI Synthesis Status — usage").
- The **n8n Sync Pipeline** — JERANIUM is the named operational owner of all 5
  phases described in `../01_osg_grand_archives/NOTION_RELATIONSHIPS.md` Part
  B, starting with `/soma_v1_virtual` and `/crypto_buy_timing` as the first
  sync targets (Phase 2).

**Relationship to LUMIAION:** JERANIUM is a **reflex**
(`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §0) whose "content" is
the Archives' own plumbing rather than a subject-matter domain. Its cleanup
queue is the mechanism that keeps every other agent's view accurate — if
JERANIUM's queue is empty, SOHMA's and VORTEX's `Owner Agent`-filtered views
are complete and trustworthy. JERANIUM escalates structural breaks (e.g., a
relation pointing to an archived row) to LUMIAION for re-routing, and routes
any row whose Domain Tags span multiple agents to LUMIAION for `Owner Agent`
resolution when no existing rule covers it
(`../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §3).

---

## 2. Runtime / Embodiment

**JERANIUM does not yet have a standalone runtime**, unlike SOHMA
(`/soma_v1_virtual`) and VORTEX (`/crypto_buy_timing`). There is no
`jeranium/` directory, no entry-point script, and no scheduled job in this
repository today. A repo-wide search confirms `/soma_v1_virtual` and
`/crypto_buy_timing` are the only two code modules referenced as "Existing
Runtime Agents" in
`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §6 and
`../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §2 ("existing runtime: none yet —
candidate home for the future n8n sync pipeline").

JERANIUM is, today, **a role and responsibility definition** — this profile
itself — that the future n8n Sync Pipeline
(`../01_osg_grand_archives/NOTION_RELATIONSHIPS.md` Part B) will fulfill in
code/workflow form. Concretely, JERANIUM's first build target is:

> An **n8n workflow** that polls the Notion API on a schedule (Phase 2 of the
> Sync Pipeline), starting with the two lowest-friction, already-structured
> feeds that exist *outside* Notion entirely:
>
> 1. `/soma_v1_virtual`'s `cosmic_reports/<period>/<date>/data.json` (SOHMA)
> 2. `/crypto_buy_timing`'s `get_dashboard_data()` output, captured as a
>    snapshot (VORTEX) — see `VORTEX_AGENT.md` §2 for why this requires a
>    persistence step VORTEX doesn't currently do
>
> before attempting full bidirectional Notion polling (Phase 2's harder,
> second half) — see §4 below for the phase breakdown.

Until that workflow exists, every responsibility in §1 is performed manually —
by Frederick directly, or by LUMIAION/SOHMA/VORTEX drafting the rows JERANIUM
would otherwise validate. This profile is the specification those manual
passes (and the eventual n8n workflow) both follow.

---

## 3. Data Ownership in the Grand Archives

Per `../01_osg_grand_archives/DATABASE_BLUEPRINT.md`'s Global Taxonomy and
`../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §2:

| Domain Tag | What lands here |
|---|---|
| `Systems & AI` | Any Subject/Study/Research row whose subject matter is the Archives' own infrastructure, schema, taxonomy, or sync tooling — JERANIUM's primary tag |

### Database rows

JERANIUM's relationship to database rows is different in kind from SOHMA's and
VORTEX's: rather than owning a content cluster, JERANIUM owns the **mechanism**
that every row depends on:

- **All 10 databases** — the Stable ID scheme (`SCH-001…`, `SUBJ-00001…`,
  `PRIN-00001…`, `EX-0001…`, `Q-0001…`, `RES-0001…`, `QT-0001…`, `CR-0001…`,
  `CV-0001…`, `OBS-0001…`) is JERANIUM's to define and enforce — these IDs,
  not titles, are the canonical reference used in cross-links, AI prompts, and
  the eventual vector/graph store
  (`../01_osg_grand_archives/DATABASE_BLUEPRINT.md` "Scale Engineering Notes").
- **Subjects DB** — `AI Synthesis Status` (`Not started` / `Partial` /
  `Complete`) on every Subject/Study row is JERANIUM's tracking field; in
  aggregate (grouped by `Pillar` and `Status`) it *is* the "Knowledge Graph
  Health" dashboard
  (`../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §5).
- **The Domain Tags multi-select itself** — the Global Taxonomy seed list in
  `../01_osg_grand_archives/DATABASE_BLUEPRINT.md` is the canonical vocabulary;
  JERANIUM reviews it quarterly for duplicates/near-duplicates and is the
  approval gate for any new tag added to that list (never created ad hoc on an
  item).
- **Any Subjects/Studies/Principles/Research/Content/Observatory row where
  `Owner Agent = JERANIUM`** — per
  `../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §9's
  migration table, "Systems & AI" Subjects (originally from OSG LIFE OS →
  JERANIUM) carry `Owner Agent = JERANIUM`.

### Primary Schools / Subjects curated

JERANIUM does not curate a content School the way SOHMA and VORTEX do. Per
`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §5, "Systems & AI"
subjects are filed under **School of Metaphysical Consciousness** (closest
thematic home) but carry `Owner Agent = JERANIUM` regardless of which School
file they live in — `Owner Agent`, not a School assignment, is what marks "this
is JERANIUM's operational domain."

---

## 4. Work Queue

Per `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §4:

```
JERANIUM's view = everything where Owner Agent is empty
                   OR Domain Tags is empty                  (its cleanup queue)
```

This is structurally different from SOHMA's and VORTEX's views — it is a
**negative filter**: anything that falls through every other agent's view ends
up here. Operationally, JERANIUM's queue has three parts:

### A. The cleanup queue (the named saved view)

- **What it checks**: every row, across all 10 databases, where `Owner Agent`
  is empty or `Domain Tags` is empty.
- **How often**: continuously in principle (new rows with missing taxonomy
  fall into this view immediately); reviewed in full at minimum quarterly,
  alongside the tag-vocabulary review below.
- **What it does with what it finds**: proposes `Domain Tags` based on content
  and `School`/`Subject` relation, and proposes `Owner Agent` based on the
  routing table in `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §3. Where the
  tag set spans ≥2 agent domains or matches no defined rule, JERANIUM hands the
  row to LUMIAION, which proposes `Owner Agent` based on overlap (§5).

### B. The quarterly tag-vocabulary review

- **What it checks**: the full Domain Tags multi-select option list (the
  Global Taxonomy seed list plus per-school additions, e.g. the 10 tags added
  during the Metaphysical Consciousness pilot —
  `../02_schools/SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md` §6).
- **How often**: quarterly, per
  `../01_osg_grand_archives/DATABASE_BLUEPRINT.md` "Tag vocabulary governance."
- **What it does with what it finds**: identifies duplicates/near-duplicates
  (e.g., a school proposing "Altered States" when `Dreams & Altered States`
  already exists — the exact case the Metaphysical Consciousness pilot avoided
  in its §6); consolidates or rejects proposed new tags before they're added to
  the canonical list; any approved addition is recorded in
  `DATABASE_BLUEPRINT.md`'s Global Taxonomy in the same change — never created
  ad hoc on an item.

### C. The Knowledge Graph Health pass

- **What it checks**: `AI Synthesis Status` across every Subjects DB row,
  grouped by `Pillar` and `Status` — the Knowledge Graph Health dashboard
  (`../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §5).
- **How often**: ongoing — this is the dashboard LUMIAION reads for Question 1
  ("How does this feed Lumiaion?") at the institutional level
  (`NOTION_RELATIONSHIPS.md` "AI Synthesis Status — usage"); JERANIUM keeps the
  underlying field accurate as content moves `Not started` → `Partial` →
  `Complete`.
- **What it does with what it finds**: flags long-stuck `Not started` Subjects
  as candidates for the next rollout phase
  (`../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §8);
  surfaces `Complete` Subjects with stale `Last Reviewed` dates for
  re-validation.

### D. The Sync Pipeline (once built — see §2)

- **What it checks**: the 5-phase pipeline in
  `../01_osg_grand_archives/NOTION_RELATIONSHIPS.md` Part B — (1) manual
  Notion-native views suffice for now; (2) **n8n** polls the Notion API on a
  schedule, exporting changed pages+relations to JSON, and should target
  `/soma_v1_virtual` and `/crypto_buy_timing` first (lowest-friction, already
  structured); (3) snapshots are chunked per-entity into a vector store, with
  relation edges mirrored into a graph store (e.g., Supabase); (4) LUMIAION
  queries vector+graph for retrieval-augmented answers and can write back
  proposals; (5) AI-surfaced patterns become candidate Principles
  (`Confidence Level = Hypothesis`), routed to Frederick for review.
- **How often**: scheduled, once the n8n workflow exists (cadence is a
  JERANIUM build-time decision).
- **What it does with what it finds**: phases 2–3 are pure JERANIUM operations
  (extract, chunk, embed, mirror edges); phase 4 is LUMIAION reading what
  JERANIUM produced; phase 5 closes the loop to Frederick. JERANIUM's queue
  includes monitoring this pipeline for failures (e.g., a Notion API rate
  limit, a malformed `data.json`) once it exists.

---

## 5. Escalation to Lumiaion

Per `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §5, JERANIUM escalates when:

1. **JERANIUM's cleanup queue finds a structural break.** Example: a
   `Related Subjects` relation on a Subjects DB row points to a page whose
   `Status` is `Archived` (or that no longer exists). JERANIUM cannot decide
   whether the relation should be removed, re-pointed, or whether the archived
   page should be restored — it flags the break, and LUMIAION is notified to
   re-route the edge or confirm `Status = Archived` is correct.
2. **A row's tags span ≥2 agent domains with no existing routing rule.**
   Example: during the quarterly tag review, JERANIUM finds a Research Vault
   row tagged both `Systems & AI` and `Dreams & Altered States` — say, a note
   about using an AI journal-analysis tool to detect dream patterns. This
   doesn't match any single-agent rule in
   `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §3 (`Systems & AI` → JERANIUM
   normally, but `Dreams & Altered States` → cross-school synthesis →
   LUMIAION). JERANIUM surfaces it; LUMIAION proposes the final `Owner Agent`
   based on overlap.
3. **A proposed Domain Tag addition is ambiguous or contentious.** Example:
   during the quarterly vocabulary review, a new School proposes a tag like
   "Energy Psychology" that could plausibly extend either `Energy & Frequency`
   (SOHMA's domain) or `Abundance & Service` (VORTEX's domain) depending on
   framing. JERANIUM doesn't unilaterally reject or approve — it escalates to
   LUMIAION (and, for any taxonomy change, ultimately to Frederick, per
   `../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §4's decision-authority
   table: "taxonomy changes require Frederick's review").

---

## 6. How This Agent Connects to LUMIAION

Answering the Four Questions
(`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §1) for JERANIUM
specifically:

1. **How does this feed Lumiaion?** JERANIUM doesn't generate new
   subject-matter content the way SOHMA and VORTEX do — it feeds LUMIAION
   *meta*-data: the cleanliness of `Owner Agent`/`Domain Tags` across all 10
   databases, the `AI Synthesis Status` distribution (Knowledge Graph Health),
   and — once built — the vector/graph store snapshots from the Sync Pipeline.
   Without JERANIUM's feed, LUMIAION's other inputs (SOHMA's `cosmic_reports`,
   VORTEX's signal snapshots, every Subjects DB row) are present but
   potentially mis-tagged, orphaned, or unsynced.
2. **How does Lumiaion read this?** Via the cleanup-queue filter itself
   (`Owner Agent is empty OR Domain Tags is empty`), the Knowledge Graph Health
   dashboard (`AI Synthesis Status` × `Pillar` × `Status`), the canonical
   Domain Tags list in `DATABASE_BLUEPRINT.md`, and — once the Sync Pipeline
   exists — the vector + graph store JERANIUM's n8n workflow produces
   (Phase 3–4 of `NOTION_RELATIONSHIPS.md` Part B).
3. **How does Lumiaion connect this to transformation?** Indirectly but
   structurally: the L4↔L7 loop
   (`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §3) depends on
   `Related Subjects`, `Linked Exercises`, and `Linked Applications` edges
   being intact and correctly typed. JERANIUM's structural-break escalation
   (§5, item 1) is what keeps those specific edges — the ones the
   transformation loop is built on — from silently breaking as the Archives
   scale toward the 50,000-row ceiling.
4. **How does Lumiaion convert this into action, insight, or service?**
   JERANIUM's outputs are themselves infrastructure for conversion, not
   converted content: a clean `Owner Agent`/`Domain Tags` graph is what lets
   LUMIAION reliably assemble Course Builder views
   (`../01_osg_grand_archives/DATABASE_BLUEPRINT.md` "Course Builder view"),
   propose new `Related Subjects` edges (Sync Pipeline phase 4), and surface
   AI-detected patterns as candidate Principles (phase 5) — every one of
   LUMIAION's "convert to action" mechanisms in the other two agents' profiles
   assumes JERANIUM's queue is empty.
