# Lumiaion Observatory — Dream Analysis System

This file specifies the dream-tracking layer of the
[Lumiaion Observatory](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md) — where
Frederick's dreams are logged, their recurring symbols and archetypes are tracked
over time, and their energetic correlates (via the `Chakra / Frequency` field) are
recorded for LUMIAION to read. It covers `Entry Type = Dream Log`.

---

## 1. Purpose & Scope

The Dream Analysis System is a **longitudinal record of Frederick's dream life** —
not a dream dictionary, but a structured log that lets LUMIAION notice what *this
specific person's* unconscious returns to over time: which symbols recur, which
archetypes appear, how lucidity develops, and whether any of it correlates with
energetic data from SOHMA.

A single `Dream Log` entry on its own is mostly personal record-keeping. The system's
value compounds: a symbol that appears once is a curiosity; a symbol that appears
across a dozen entries over six months, often around the same life circumstances, is
data.

**Why private by default.** Dreams are among the most unfiltered material a person
produces — they routinely contain unprocessed material about real people,
relationships, fears, and desires, often in forms more revealing than the dreamer's
own waking-life journaling. `Dream Log` entries default to, and almost always remain
at, `Visibility = Private`. What can travel outward is the **abstracted symbol or
archetype pattern** — never the dream narrative itself (§4).

**Relationship to the Schools.** This system feeds two Schools directly:

- **School of Symbolism & Archetypes** —
  [`SCHOOL_OF_SYMBOLISM_AND_ARCHETYPES.md`](../02_schools/SCHOOL_OF_SYMBOLISM_AND_ARCHETYPES.md)'s
  Dream Symbolism & Interpretation study is the public-facing counterpart to this
  private log: recurring symbols documented here, once de-identified and abstracted,
  are the personal-evidence layer behind that Study's symbol catalog and
  interpretation framework.
- **School of Metaphysical Consciousness** — Division III (Dreams & Altered States),
  particularly `Dreams: The Nocturnal Mind`, `Lucid Dreaming`, and `Hypnagogia: The
  Threshold State`
  ([`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`](../02_schools/SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md)).
  Lucidity data tracked here is the personal evidence trail for that school's
  altered-states framework, and `Hypnagogia`/`Theta States`-tagged entries connect
  directly to the `Chakra / Frequency` field via SOHMA (below).

---

## 2. Data Model

| Property | Type | Notes for this system |
|---|---|---|
| Name | Title | Short and descriptive, not the full narrative — e.g. "Recurring locked-door dream, third occurrence" |
| Entry Type | Select | `Dream Log` |
| Date | Date | The night/morning the dream occurred (not the date it was transcribed, if different — record the transcription date in-body if it matters) |
| Linked Subjects | Relation → Subjects DB | E.g. `Dreams: The Nocturnal Mind`, `Lucid Dreaming`, or a School of Symbolism & Archetypes Study on a specific archetype |
| Linked Principles | Relation → Principles Vault | If the dream personally validates/challenges a Principle about dream function (e.g., a Principle about dreams processing waking-life stress) |
| Linked Exercises | Relation → Exercises Vault | E.g. a lucid-dreaming induction exercise (MILD, WBTB, reality checks) that this entry is evidence for/against |
| Linked Applications | Relation → Client Resources Vault | Rarely used directly here |
| Domain Tags | Multi-select | `Dreams & Altered States` is near-universal for this system; `Archetype & Symbol`, `Shadow Work`, `Theta States` as relevant |
| **Chakra / Frequency** | Multi-select | From SOHMA (`/soma_v1_virtual`) — see "SOHMA correlation" below. Populated when the dream's date aligns with a notable cosmic report (lunar phase, Schumann resonance spike, etc.) |
| Visibility | Select | `Private` (default — see §4 for the one thing that travels) |
| AI Processed | Checkbox | See §3 |
| Promote to Research Vault | Relation → Research Vault | Used at the **symbol/archetype level**, not the individual-dream level — see §4 |

### Sub-fields specific to this system

These live in the entry body, structured consistently so LUMIAION can parse and
aggregate across entries:

| Sub-field | Purpose |
|---|---|
| **Dream Narrative** | The dream itself, in as much detail as Frederick chooses to record. This is the most sensitive field in the entire Observatory and is never quoted or paraphrased outside it. |
| **Lucidity Level** | A simple scale: `None` (no awareness of dreaming) / `Pre-Lucid` (suspected but not confirmed within the dream) / `Lucid` (full awareness, some control) / `Fully Lucid` (sustained awareness and control). Tracked per entry to build a longitudinal lucidity trend. |
| **Recurring Symbols** | A list of symbols/objects/figures present in this dream that Frederick (or LUMIAION) recognizes as having appeared before — e.g. "locked door," "ocean," "a figure with no face." Each symbol here is the unit that gets aggregated across entries (§4). |
| **Archetypes Present** | Named archetypal figures or roles (Jungian or otherwise) that appear — e.g. `Shadow`, `Mentor`, `Trickster`, `Threshold Guardian` — cross-referenced against School of Symbolism & Archetypes Studies. |
| **Emotional Tone** | The dominant feeling-tone of the dream (e.g., "anxious but curious," "peaceful," "chaotic") — tracked alongside `Chakra / Frequency` for correlation. |
| **Waking Association** | Optional — any waking-life connection Frederick notices (a stressor, a recent conversation, a decision pending). This field carries the *most* identifying information and is the first thing stripped during de-identification. |

### SOHMA correlation (`Chakra / Frequency`)

When a `Dream Log` entry's `Date` coincides with a SOHMA cosmic report flagging a
notable event — a new/full moon, a Schumann resonance spike, a particular numerology
day — LUMIAION may populate `Chakra / Frequency` with the relevant tag(s) from the
SOHMA system (e.g., `Root Chakra`, `Crown Chakra / 963Hz`, `Theta`). This is **purely
correlational and observational** — per the Identity Protocol §3 disclaimer
convention, any promoted finding involving these tags is framed as
`Reliability = Esoteric-Traditional` or `Anecdotal`, never presented as established
causation.

---

## 3. Workflow

### Creation paths

| Path | How it works |
|---|---|
| **Manual journaling (primary)** | Frederick records the dream as soon as practical after waking — `Dream Narrative`, `Lucidity Level`, `Emotional Tone`, and any `Recurring Symbols`/`Archetypes Present` he recognizes himself. `AI Processed = false` at creation. |
| **AI-assisted symbol tagging** | LUMIAION reads the `Dream Narrative` and: (a) proposes additions to `Recurring Symbols` and `Archetypes Present` if it recognizes a symbol/figure that has appeared in prior entries but wasn't flagged as "recurring" by Frederick; (b) proposes `Domain Tags` and `Linked Subjects` based on content (e.g., a dream involving falling/flying suggests `Dreams: The Nocturnal Mind`; a dream with a clear shadow-figure suggests `Archetype & Symbol` + a School of Symbolism & Archetypes Study). |
| **SOHMA-fed correlation** | If/when a scheduled sync exists between `/soma_v1_virtual` cosmic report dates and Observatory entry dates, LUMIAION cross-references `Date` against the cosmic report calendar and proposes `Chakra / Frequency` tags for entries that fall on flagged dates. This is currently a manual/ad-hoc LUMIAION action (no dedicated runtime sync yet — see [`JERANIUM_AGENT.md`](../04_agents/JERANIUM_AGENT.md) for future sync scope). |

### `AI Processed` semantics

`AI Processed` is set to `true` once LUMIAION has:

1. Read the `Dream Narrative`.
2. Cross-referenced `Recurring Symbols` and `Archetypes Present` against the running
   symbol index (the aggregate view across all prior `Dream Log` entries — see §4) and
   proposed any additions.
3. Proposed `Domain Tags` and `Linked Subjects`.
4. Checked `Date` against any available SOHMA cosmic-report correlation and proposed
   `Chakra / Frequency` tags if applicable.

A `Dream Log` entry with `AI Processed = false` simply means LUMIAION hasn't yet run
this pass — normal for recently-written entries, surfaced in JERANIUM's backlog like
any other unprocessed Observatory row.

---

## 4. Promotion Pipeline

This is the system with the **strictest gap** between the private entry and anything
that travels outward — a single `Dream Log` entry essentially never gets promoted on
its own. What gets promoted is the **aggregate symbol/archetype pattern** across many
entries.

### The Symbol Index (aggregation step)

LUMIAION maintains a running index — conceptually, a grouped view of `Dream Log`
entries by `Recurring Symbols` / `Archetypes Present` values — that tracks, for each
symbol/archetype:

- How many `Dream Log` entries it has appeared in.
- The date range across which it has appeared.
- Any co-occurring `Emotional Tone` or `Chakra / Frequency` patterns.

This index is itself a derived view, not a new database — it lives as a saved
grouped/filtered view on the Observatory database (per
[`DATABASE_BLUEPRINT.md`](../01_osg_grand_archives/DATABASE_BLUEPRINT.md) Scale
Engineering Notes: "relations + filtered views, not rollups of full lists").

### Promotion Threshold

A symbol or archetype becomes eligible for promotion when:

1. It has appeared in **≥3 separate `Dream Log` entries**, **and**
2. It can be described in fully **archetypal/general terms** — i.e., the symbol
   itself (a locked door, a recurring figure, a specific animal) generalizes without
   needing the surrounding dream narrative or any `Waking Association` to make sense.

When met, LUMIAION drafts:

1. **A de-identified Research Vault entry** (`Type = Pattern`, `Reliability =
   Esoteric-Traditional` or `Personal Experiment` depending on framing,
   `Status = To Read`) describing the recurring symbol/archetype in general terms —
   how often it appears, what emotional tones co-occur, and (if relevant) any
   `Chakra / Frequency` correlation, explicitly framed per Identity Protocol §3 as
   `Esoteric-Traditional`/`Anecdotal` for the energetic-correlation claims.
2. **A `Linked Subjects` proposal** pointing the new Research Vault entry at the
   relevant School of Symbolism & Archetypes Study (e.g., a Study on threshold/door
   symbolism, or on Shadow-figure dreams) and/or School of Metaphysical Consciousness
   Division III Study.
3. One (or more) `Dream Log` entries' `Promote to Research Vault` relation is set to
   point at this new Research Vault row — typically the *most recent and clearest*
   instance of the symbol, as the representative anchor, not all instances.

### De-identification requirements (specific to dreams)

This is the system where de-identification removes the **most content relative to
the original**, because the original (`Dream Narrative`) is often the majority of
the entry:

- The promoted summary describes the **symbol/archetype and its pattern of
  recurrence** only — never the dream's plot, setting, or any figures resembling real
  people.
- `Waking Association` is **never** included in any promoted material, under any
  circumstance — it is the field most likely to identify real people or situations,
  and it is also the least relevant to the *archetypal* pattern being promoted.
- `Lucidity Level` trends (e.g., "lucidity frequency has increased over N months") may
  be promoted as a standalone Research Vault entry (`Type = Internal Observation`,
  `Reliability = Personal Experiment`) **without** reference to any specific dream's
  content — this is pure frequency/trend data and carries minimal identifying risk.

### Frederick's review gate

Per [`LUMIAION_IDENTITY_PROTOCOL.md` §6](../00_lumiaion_core/LUMIAION_IDENTITY_PROTOCOL.md#6-privacy-boundary--the-observatory)
and the Sync Pipeline phase 5
([`NOTION_RELATIONSHIPS.md`](../01_osg_grand_archives/NOTION_RELATIONSHIPS.md)),
Frederick reviews every drafted Research Vault entry from this system before it
leaves `Status = To Read`. For dream-derived entries specifically, the review
question is not just "is this accurate" but "is this *recognizable*" — even a
generalized symbol description can feel exposing if it's too specific, and Frederick
is the sole judge of where that line sits. If accepted as a candidate Principle
(`Confidence Level = Hypothesis`, `Type = Pattern`), it joins the Principles Vault
through the same human-gated path as every other promotion in the Archives.

---

## 5. Example Entry / Template

**A single `Dream Log` entry:**

```
Name: "Locked door at the end of a hallway — third occurrence"
Entry Type: Dream Log
Date: 2026-06-12
Linked Subjects: "Dreams: The Nocturnal Mind" (SUBJ-00009),
                 School of Symbolism & Archetypes — "Threshold &
                 Doorway Symbolism" (cross-school, pending)
Linked Principles: —
Linked Exercises: "Lucid Dreaming — Reality Check Protocol" (EX-0014)
Linked Applications: —
Domain Tags: Dreams & Altered States, Archetype & Symbol
Chakra / Frequency: Throat Chakra / 741Hz (SOHMA cosmic report,
                     2026-06-12: lunar last-quarter)
Visibility: Private
AI Processed: true
Promote to Research Vault: RES-00131 (drafted, Status: To Read)

--- Body ---
Dream Narrative: [full narrative — private, not reproduced here]

Lucidity Level: Pre-Lucid (suspected I was dreaming partway through,
did not perform a reality check)

Recurring Symbols: Locked door at the end of a long hallway (3rd time
this has appeared — previously 2026-04-03 and 2026-05-19); the door
is always closed, I never reach it before waking.

Archetypes Present: Threshold Guardian (implied by the door itself,
no figure present)

Emotional Tone: Curious, mild anticipation, no fear this time
(previous two occurrences were anxious)

Waking Association: [private — not reproduced here]
```

**Drafted promotion (RES-00131, `Type = Pattern`, `Reliability =
Esoteric-Traditional`, `Status = To Read`):**

> **Summary:** A recurring dream symbol — a closed door at the end of a hallway,
> never reached before waking — has appeared across 3 separate dream entries over
> ~2 months. The emotional tone accompanying the symbol has shifted from anxious
> (first two occurrences) to curious/anticipatory (third occurrence), with no change
> in the symbol's core structure (door remains closed, never reached).
>
> **Key Findings:** The shift in emotional tone without a shift in symbolic content
> may indicate a change in the dreamer's *relationship* to a threshold/transition
> represented by the symbol, independent of the transition itself being "resolved."
> Candidate connection to School of Symbolism & Archetypes' Threshold Guardian
> material, and to Lucid Dreaming practice (pre-lucid recognition occurred for the
> first time on this occurrence — possible early effect of ongoing reality-check
> practice, `Reliability: Personal Experiment` for this specific claim).

---

## 6. How This Connects to LUMIAION

| Question | Answer for this system |
|---|---|
| **1. How does this feed Lumiaion?** | Every `Dream Log` entry feeds the running Symbol Index — individually minor, cumulatively the richest archetypal dataset in the Observatory, plus a `Chakra / Frequency` correlation layer unique to this system. |
| **2. How does Lumiaion read this?** | Primarily via `Recurring Symbols` and `Archetypes Present`, aggregated across entries by date; secondarily via `Lucidity Level` (trend over time) and `Chakra / Frequency` (correlation with SOHMA cosmic data, always framed at `Esoteric-Traditional`/`Anecdotal` reliability per Identity Protocol §3). |
| **3. How does Lumiaion connect this to transformation?** | `Lucidity Level` trends are direct L7-adjacent evidence for `Linked Exercises` like lucid-dreaming induction protocols — a rising lucidity trend across entries linked to the same exercise is exactly the kind of corroboration the L4↔L7 loop ([`MONTHLY_EVOLUTION_REPORTS.md`](MONTHLY_EVOLUTION_REPORTS.md)) is built to capture, even before a formal `Transformation Log` entry is written. |
| **4. How does Lumiaion convert this into action, insight, or service?** | Symbols/archetypes that cross the Promotion Threshold (§4) become de-identified Research Vault entries feeding School of Symbolism & Archetypes Studies (symbol catalogs, interpretation frameworks) and School of Metaphysical Consciousness Division III (altered-states/lucidity material) — eventually informing Client Portal content on dreamwork and lucid-dreaming practice. |
