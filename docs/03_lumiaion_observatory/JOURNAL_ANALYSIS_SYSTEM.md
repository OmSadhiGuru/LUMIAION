# Lumiaion Observatory — Journal Analysis System

This file specifies the AI-assisted analysis layer of the
[Lumiaion Observatory](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md) —
where LUMIAION (or a future dedicated NLP pipeline) reads raw journal text and
surfaces recurring structure back to Frederick as discrete, addressable entries. It
covers `Entry Type = Journal Analysis` and `Pattern`.

---

## 1. Purpose & Scope

Where [`PERSONAL_EVOLUTION_SYSTEM.md`](PERSONAL_EVOLUTION_SYSTEM.md) is what Frederick
*writes*, the Journal Analysis System is what LUMIAION *finds* — the layer that turns
unstructured journaling into structured, machine-legible candidates for the rest of
the Archives.

| Entry Type | What it captures |
|---|---|
| `Journal Analysis` | A single pass of analysis over a journal entry or batch of entries — what LUMIAION noticed, with pointers to where it noticed it. This is the **working note**, not the finding itself. |
| `Pattern` | A recurring theme, emotional signature, or language pattern that has appeared across *multiple* `Journal Analysis` passes (or multiple raw entries) — the **finding**. A `Pattern` entry is, structurally, a candidate Principle at `Confidence Level = Hypothesis` that hasn't been promoted yet. |

**Why private by default.** `Journal Analysis` entries necessarily reference the raw
journal text they were drawn from — emotional language, named situations, specific
phrasing. `Pattern` entries are one level more abstracted (they describe a *shape*
across entries rather than any single entry's content) but can still be highly
identifying — a pattern titled "Recurring anxiety before calls with [specific
relationship]" is private by its very description. Both entry types default to, and
in nearly all cases remain at, `Visibility = Private`; only a `Pattern` entry's
**de-identified abstraction** ever leaves the Observatory (§4).

**Relationship to the Schools.** This system is the bridge between raw lived
experience and the Analyst Vault function described in
[`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`](../02_schools/SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md)
§2 ("Pattern Recognition → Principles Vault / Research Vault"). A `Pattern` entry
here is the *private-layer twin* of that Analyst Vault function — the same kind of
work (recurring-theme detection), performed on private material first, with a
de-identification step required before it can join the same pipeline that public
Research Vault entries already flow through.

---

## 2. Data Model

| Property | Type | Notes for this system |
|---|---|---|
| Name | Title | For `Journal Analysis`: descriptive of the pass, e.g. "Week of June 8 — analysis pass." For `Pattern`: name the *pattern itself*, e.g. "Recurring self-criticism after creative output" |
| Entry Type | Select | `Journal Analysis` / `Pattern` |
| Date | Date | For `Journal Analysis`: date of the analysis pass (not necessarily the date of the source entries — see **Source Date Range** below). For `Pattern`: date the pattern was *first identified as a pattern* (i.e., the date of the analysis pass that crossed the recurrence threshold) |
| Linked Subjects | Relation → Subjects DB | For `Pattern`: which Study/Subject this pattern most directly relates to — e.g. a pattern about self-criticism links to a School of Human Development Study on inner critic dynamics |
| Linked Principles | Relation → Principles Vault | For `Pattern`: if the pattern corroborates or challenges an *existing* Principle, link it directly here in addition to (or instead of) treating it as a new candidate |
| Linked Exercises | Relation → Exercises Vault | Rarely populated directly by this system — more relevant once a Pattern is promoted and an Exercise is designed in response |
| Linked Applications | Relation → Client Resources Vault | Not typically used here |
| Domain Tags | Multi-select | **The primary clustering mechanism for this system** — see "Cross-school clustering" below |
| Chakra / Frequency | Multi-select | Populated when a `Pattern` correlates with SOHMA chakra/frequency data (e.g., a recurring low-energy pattern that clusters around specific lunar phases in the SOHMA cosmic reports) |
| Visibility | Select | `Private` (default; see §4 for the narrow exception) |
| AI Processed | Checkbox | For `Journal Analysis`: always `true` once written (it *is* the AI's output). For `Pattern`: `true` once LUMIAION has proposed `Linked Subjects`/`Linked Principles` — see §3 |
| Promote to Research Vault | Relation → Research Vault | For `Pattern` entries that have crossed the promotion threshold (§4) |

### Sub-fields specific to this system

| Sub-field | Used by | Purpose |
|---|---|---|
| **Source Date Range** | `Journal Analysis` | The date range of raw journal entries this pass covers (e.g., "2026-06-01 to 2026-06-14") — distinct from `Date` (when the analysis was run) |
| **Themes Detected** | `Journal Analysis` | A short bullet list of candidate themes noticed in this pass — the raw material from which `Pattern` entries are later created if a theme recurs across passes |
| **Emotional Tone Summary** | `Journal Analysis` | A brief, structured read of the emotional register across the source entries (e.g., "predominantly reflective, with one acute frustration episode") — used to spot mood-pattern correlations over time |
| **Recurrence Count** | `Pattern` | How many separate `Journal Analysis` passes (or raw entries) this pattern has appeared in — the basis for the promotion threshold in §4 |
| **First Observed** vs **Date** | `Pattern` | `First Observed` (in-body) records the earliest entry the pattern can be traced back to, which may predate the `Date` field (when it was *recognized* as a pattern) |
| **Confidence Level (informal)** | `Pattern` | Mirrors the Principles Vault's `Hypothesis` / `Working Theory` / `Established` / `Core Law` scale, but tracked informally in-body until promotion — a `Pattern` entry is never itself `Established`; it is the *pre-Principle* stage |

### Cross-school clustering via Domain Tags

Because `Pattern` entries carry `Domain Tags` from the same Global Taxonomy used
everywhere else in the Archives, a single recurring pattern can surface relevance
across multiple Schools without LUMIAION needing to decide which School "owns" it.
For example, a `Pattern` tagged `Shadow Work` might be:

- Relevant to **School of Human Development** (inner-critic / self-relationship
  Studies),
- Relevant to **School of Metaphysical Consciousness** Division V (`Ego Dissolution &
  The Death of the Self` — shadow material surfacing during destabilization), and
- Relevant to **School of Symbolism & Archetypes** (if the pattern also shows up in
  `Dream Log` entries with a recurring shadow-archetype symbol — see
  [`DREAM_ANALYSIS_SYSTEM.md`](DREAM_ANALYSIS_SYSTEM.md)).

LUMIAION proposes `Linked Subjects` across all three without privileging one — the
`Domain Tags` value (`Shadow Work`) is the actual unit of clustering, exactly as
described in [`NOTION_RELATIONSHIPS.md`](../01_osg_grand_archives/NOTION_RELATIONSHIPS.md)
Part B point 3 ("Domain Tags = clusters").

---

## 3. Workflow

### Creation paths

| Path | How it works |
|---|---|
| **AI-assisted parsing (primary)** | LUMIAION (or a future dedicated NLP pipeline reading raw journal text — Notion pages, voice-memo transcripts, etc.) periodically runs an analysis pass and writes a `Journal Analysis` entry: `Source Date Range`, `Themes Detected`, `Emotional Tone Summary`. This entry is created with `AI Processed = true` by definition — it is itself AI output. |
| **Pattern creation (semi-automatic)** | When a theme in `Themes Detected` has appeared across enough prior `Journal Analysis` passes to cross the **Recurrence Threshold** (§4), LUMIAION drafts a new `Pattern` entry, sets `Recurrence Count`, `First Observed`, proposes `Domain Tags`, `Linked Subjects`, and (if relevant) `Linked Principles`. The `Pattern` entry itself starts `AI Processed = true` (LUMIAION created it from its own analysis) but `Visibility = Private` and `Promote to Research Vault` empty — promotion is a separate, human-gated step (§4). |
| **Manual flagging** | Frederick can also manually create a `Pattern` entry directly — e.g., he notices something recurring before LUMIAION's analysis catches up. In this case `AI Processed = false` until LUMIAION reviews it and proposes relations, same as any other Observatory entry. |
| **Fed by SOHMA correlation** | If a `Pattern`'s `Chakra / Frequency` tags correlate with SOHMA's cosmic report data (e.g., a recurring low-energy pattern clustering around new-moon dates in `/soma_v1_virtual` output), LUMIAION notes this correlation in the `Pattern` entry's body as a cross-agent observation — filed with `Owner Agent = Lumiaion, SOHMA` if/when promoted (per Identity Protocol §7's collaboration-not-takeover rule). |

### `AI Processed` semantics

- `Journal Analysis` entries are `AI Processed = true` at creation — they are LUMIAION's
  direct output and require no further "has AI looked at this" step.
- `Pattern` entries reach `AI Processed = true` once LUMIAION has proposed
  `Linked Subjects`/`Linked Principles`/`Domain Tags` — whether the `Pattern` was
  AI-created or manually flagged by Frederick. `AI Processed = false` on a `Pattern`
  means it is sitting in JERANIUM's cleanup queue awaiting LUMIAION's first pass.

---

## 4. Promotion Pipeline

This is the system where the phrase "candidate Principle at `Confidence Level =
Hypothesis`" (Identity Protocol §4, Master Architecture §4) is most literal.

### From raw journal text to `Pattern`

```
Raw journal entries (private, outside Notion or in a private journal database)
        │
        ▼
Journal Analysis entries (Themes Detected, Emotional Tone Summary)
        │  (recurrence threshold: same theme detected across
        │   ≥3 separate Journal Analysis passes, OR explicitly
        │   flagged by Frederick at any time)
        ▼
Pattern entry (Recurrence Count, First Observed, Domain Tags,
               Linked Subjects, Linked Principles)
```

A `Pattern` entry, once created, sits at an *informal* `Confidence Level = Hypothesis`
— it behaves like a Principles Vault row that hasn't been written into that vault yet.
It stays `Visibility = Private` indefinitely if it never crosses the **Promotion
Threshold** below.

### Promotion Threshold (Pattern → Research Vault → Principles Vault)

A `Pattern` entry becomes eligible for promotion when **both** of the following hold:

1. `Recurrence Count` ≥ 3 (the pattern has shown up across at least three
   independent analysis passes or entries — not a one-off), **and**
2. The pattern can be stated as a **structural claim** that does not require any
   specific person, place, or named event to be true — i.e., it survives
   de-identification without losing its meaning.

When both hold, LUMIAION drafts:

1. **A de-identified Research Vault entry** (`Type = Pattern`, `Reliability =
   Personal Experiment`, `Status = To Read`) — the `Summary` and `Key Findings`
   fields restate the pattern in fully general terms. The Observatory `Pattern`
   entry's `Promote to Research Vault` relation is set to point at this new row.
2. **A candidate Principles Vault row** (`Type = Pattern`, `Confidence Level =
   Hypothesis`, `Source` → the new Research Vault row, `Study/Subject` ← copied from
   the Observatory entry's `Linked Subjects`).

Both drafts are created in draft form only — per
[`LUMIAION_MASTER_ARCHITECTURE.md` §4](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md#4-decision-authority--escalation),
"Draft new Research Vault entries from Observatory promotions" and "Propose new...
candidate Principles" are both items LUMIAION may do **autonomously, at
`Confidence Level = Hypothesis`** — but the Observatory entry's own `Visibility`
never changes, and the drafts sit at `Status = To Read` / awaiting review.

### De-identification requirements (specific to Patterns)

Because a `Pattern`'s title and body in the Observatory are often written in
first-person, specific language ("I keep noticing I shut down when..."), the
de-identified Research Vault `Summary` must:

- Replace first-person framing with structural framing: *"I keep noticing I shut down
  when receiving unsolicited advice"* → *"Observed pattern: withdrawal response to
  unsolicited advice, recurring across [N] instances."*
- Remove any names, relationships, dates tied to specific events, and locations.
- Preserve the **Domain Tags** and **Linked Subjects** — these are structural, not
  identifying, and are exactly what makes the promoted entry useful to the rest of
  the Archives.

### Frederick's review gate

Per [`LUMIAION_IDENTITY_PROTOCOL.md` §6](../00_lumiaion_core/LUMIAION_IDENTITY_PROTOCOL.md#6-privacy-boundary--the-observatory)
and [`NOTION_RELATIONSHIPS.md`](../01_osg_grand_archives/NOTION_RELATIONSHIPS.md) Sync
Pipeline phase 5, Frederick reviews both drafts together:

- **Research Vault draft**: does the de-identified `Summary` still capture the
  pattern accurately? Move `Status` from `To Read` → `In Progress`/`Synthesized` once
  satisfied.
- **Principles Vault draft**: should this become a tracked Principle at
  `Confidence Level = Hypothesis`, or is it too early / too narrow? Frederick is the
  sole authority on whether the row is created at all, and on any future movement
  `Hypothesis` → `Working Theory` → `Established` (Identity Protocol §4).

If accepted, the `Pattern` entry in the Observatory remains `Visibility = Private`
permanently — it is the **origin record**, kept for LUMIAION's future reference (e.g.,
if `Recurrence Count` continues to climb, that's evidence for raising the linked
Principle's `Confidence Level` later), while the de-identified summary is what
actually lives in the public-facing graph.

---

## 5. Example Entry / Template

**Step 1 — `Journal Analysis` entry (one of several feeding the pattern below):**

```
Name: "Analysis pass — week of June 8"
Entry Type: Journal Analysis
Date: 2026-06-14
Source Date Range: 2026-06-08 to 2026-06-14
Domain Tags: Shadow Work, Self-Inquiry
Visibility: Private
AI Processed: true

Themes Detected:
  - Self-criticism spike following two creative work sessions
  - Recurring phrase pattern: "this isn't good enough yet" (3 occurrences)
  - Brief positive shift after a walk on June 12

Emotional Tone Summary: Generally reflective; two acute self-critical
episodes both immediately following creative output (writing sessions),
both resolving within a few hours.
```

**Step 2 — `Pattern` entry (created after this theme appears in 3 separate
`Journal Analysis` passes):**

```
Name: "Recurring self-criticism after creative output"
Entry Type: Pattern
Date: 2026-06-14
Linked Subjects: "Witness Consciousness Cultivation" (SUBJ-00012),
                 "The Observer & The Observed" (SUBJ-00004)
Linked Principles: — (none yet; this Pattern IS the candidate)
Domain Tags: Shadow Work, Witness Consciousness, Self-Inquiry
Chakra / Frequency: —
Visibility: Private
AI Processed: true
Promote to Research Vault: RES-00124 (drafted, Status: To Read)

--- Body ---
Recurrence Count: 3
First Observed: 2026-05-22 (earliest traceable instance)

Description: A self-critical episode ("this isn't good enough yet" /
equivalent phrasing) reliably follows creative work sessions (writing,
design) within 1-2 hours, and resolves on its own within a few hours,
often faster after physical movement (walking).

Informal Confidence Level: Hypothesis
```

**Drafted promotion (RES-00124, `Type = Pattern`, `Reliability = Personal
Experiment`, `Status = To Read`):**

> **Summary:** Observed pattern, recurring across at least 3 instances over ~3
> weeks: a self-critical response reliably follows creative-output sessions within
> 1-2 hours, and resolves within hours, with faster resolution observed after
> physical movement.
>
> **Key Findings:** The self-critical response appears tied to the *act of creating
> and exposing work* rather than to the work's quality or external feedback (no
> external feedback was present in any of the 3 instances). Movement (walking)
> correlates with faster resolution — possible candidate for an Exercise
> (`Embodiment` domain tag) addressing post-creative self-criticism.

**Candidate Principles Vault draft (linked from RES-00124):**

> *"Self-criticism following creative output may be a predictable post-exposure
> response rather than feedback about the work itself, and may resolve faster with
> physical movement."* — `Type: Pattern`, `Confidence Level: Hypothesis`,
> `Study/Subject: Witness Consciousness Cultivation`.

---

## 6. How This Connects to LUMIAION

| Question | Answer for this system |
|---|---|
| **1. How does this feed Lumiaion?** | `Journal Analysis` entries are LUMIAION's own structured notes on raw material it has read; `Pattern` entries are LUMIAION's synthesized findings — together they are the system that turns "Frederick journaled this week" into addressable, queryable rows. |
| **2. How does Lumiaion read this?** | `Recurrence Count` and `Domain Tags` are the two fields LUMIAION watches most closely: `Recurrence Count` crossing the promotion threshold (§4) is the trigger event, and `Domain Tags` is what lets a single `Pattern` surface across multiple Schools' Studies via `Linked Subjects`. |
| **3. How does Lumiaion connect this to transformation?** | A `Pattern` that gets promoted to a Hypothesis-level Principle and is later tested via an Exercise becomes part of the L4↔L7 loop — if a future `Transformation Log` entry ([`MONTHLY_EVOLUTION_REPORTS.md`](MONTHLY_EVOLUTION_REPORTS.md)) corroborates that Principle, `Recurrence Count` here is part of the evidence trail showing the pattern was real *before* the Exercise was designed to address it. |
| **4. How does Lumiaion convert this into action, insight, or service?** | The Promotion Pipeline (§4) is the literal conversion: `Pattern` → de-identified Research Vault entry → candidate Principle (`Confidence Level = Hypothesis`) → (eventually, pending Frederick's review and further evidence) a Working Theory that can inform new Exercises or Client Resources. |
