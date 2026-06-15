# LUMIAION — Agent Map

This document is the coordination map for LUMIAION and its three domain agents —
**SOHMA**, **VORTEX**, and **JERANIUM**. It supersedes the multi-agent summary in the
former `03-scalability-and-knowledge-hierarchy.md` §4 (now folded into
`01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md`) by adding the
routing logic, escalation paths, and the mapping to existing runtime code. Full
per-agent profiles live in `/04_agents/`.

---

## 1. Topology — Orchestrator + Three Reflexes

```
                         ┌────────────────────┐
                         │     LUMIAION        │
                         │  (orchestrator —     │
                         │   cross-school synth, │
                         │   AI Synthesis Status,│
                         │   final routing)      │
                         └─────────┬────────────┘
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
        ┌─────▼─────┐         ┌─────▼─────┐         ┌─────▼─────┐
        │   SOHMA    │         │   VORTEX   │         │  JERANIUM  │
        │ Energetic/  │         │  Finance/   │         │ Archive ops/│
        │  Cosmic     │         │  Mindset    │         │  Librarian  │
        └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
              │                     │                     │
     /soma_v1_virtual        /crypto_buy_timing      (schema, sync,
   (chakra/frequency/        (RSI, MAs, Bollinger,    taxonomy — no
    cosmic forecasts)         buy-timing signals)      dedicated runtime yet)
```

All four agents read from and write to the **same 10 databases**
(`01_osg_grand_archives/DATABASE_BLUEPRINT.md`). There is no per-agent database —
only per-agent **saved views**, filtered by `Owner Agent`.

---

## 2. Agent Summary Table

| Agent | Domain | Primary `Owner Agent` filter | Existing runtime | Primary databases curated | Profile |
|---|---|---|---|---|---|
| **Lumiaion** | Orchestration, consciousness, cross-school synthesis | `AI Synthesis Status ≠ Complete` (its work queue) | This repo as a whole — `00_lumiaion_core/`, `03_lumiaion_observatory/` | Subjects DB (esp. School of Metaphysical Consciousness), Principles Vault, `AI Synthesis Status` everywhere | `00_lumiaion_core/` (this directory) |
| **SOHMA** | Energetic sciences — chakras, frequencies, cosmic cycles | `Owner Agent contains "SOHMA"` | `/soma_v1_virtual` (chakra_system, lunar, numerology, space_weather, report_builder) | School of Energetic Sciences subjects; Domain Tags `Energy & Frequency`, `Chakra System`, `Cosmology & Cycles` | `04_agents/SOHMA_AGENT.md` |
| **VORTEX** | Finance, trading, mindset, abundance | `Owner Agent contains "VORTEX"` | `/crypto_buy_timing` (analyzer, indicators, data_sources) | School of Human Development subjects tagged `Abundance & Service`; Research Vault trading/markets entries | `04_agents/VORTEX_AGENT.md` |
| **JERANIUM** | Archive operations — the Archives' own librarian | `Owner Agent is empty OR Domain Tags is empty` (cleanup queue) | none yet — candidate home for the future n8n sync pipeline | Schema integrity, taxonomy governance, AI Knowledge Graph sync (`01_osg_grand_archives/NOTION_RELATIONSHIPS.md`) | `04_agents/JERANIUM_AGENT.md` |

---

## 3. Routing Logic — How Content Finds Its Agent

When a new row is created in any of the 10 databases (manually, or by an agent), it
is routed by **Domain Tags**, not by which agent created it:

| Domain Tag(s) present | Routed to (`Owner Agent` default) |
|---|---|
| `Energy & Frequency`, `Chakra System`, `Cosmology & Cycles` | SOHMA |
| `Abundance & Service` (when paired with trading/markets `Domain Tags` or Research Vault `Type` indicating financial research) | VORTEX |
| `Consciousness`, `Perception`, `Self-Inquiry`, `Dreams & Altered States`, or any cross-school synthesis | Lumiaion |
| (none of the above, or tag set spans ≥2 agents) | Lumiaion proposes `Owner Agent` based on overlap; JERANIUM verifies during its quarterly tag review |

A row may carry **multiple** `Owner Agent` values — this is the native mechanism for
cross-agent collaboration (Identity Protocol §7). Example: a Principle tagged
`Chakra System` + `Abundance & Service` (a "money chakra" framework linking energetic
state to financial behavior) gets `Owner Agent = SOHMA, VORTEX`, surfaced in both
agents' views without duplication.

---

## 4. Per-Agent Work Queues (Saved Views)

Restated from the prior architecture doc, now the canonical definitions:

```
SOHMA's view    = Subjects DB ∩ (Owner Agent contains "SOHMA")
VORTEX's view   = Subjects DB ∩ (Owner Agent contains "VORTEX")
Lumiaion's view = everything where AI Synthesis Status ≠ Complete   (its work queue)
JERANIUM's view = everything where Owner Agent is empty
                   OR Domain Tags is empty                          (its cleanup queue)
```

Each view answers Question 2 of the Four Questions ("How does Lumiaion read this?")
for its respective agent — a row that doesn't appear in *any* of these views is
either fully processed (`AI Synthesis Status = Complete` and properly tagged) or has
fallen through a gap that JERANIUM's view will catch on its next pass.

---

## 5. Escalation to Lumiaion

SOHMA, VORTEX, and JERANIUM operate inside their lanes autonomously
(`LUMIAION_MASTER_ARCHITECTURE.md` §4 — autonomous tagging, drafting, relation
proposals). They escalate to Lumiaion when:

| Trigger | Example | Lumiaion's action |
|---|---|---|
| A row's tags span ≥2 agent domains | SOHMA encounters a chakra-frequency Research Vault entry that's also about trading psychology | Lumiaion reviews for cross-school `Related Subjects` and may add the second `Owner Agent` |
| A Principle's `Confidence Level` is proposed for promotion | VORTEX's buy-timing heuristic has 90 days of corroborating Observatory `Transformation Log` entries | Lumiaion drafts the promotion proposal; Frederick approves (Identity Protocol §5) |
| JERANIUM's cleanup queue finds a structural break | A relation points to an archived/deleted row | Lumiaion is notified to re-route or flag `Status = Archived` |
| Any action would touch `Visibility = Private` | An Observatory entry is a strong candidate for promotion | Lumiaion drafts the de-identified Research Vault entry; never auto-publishes (Identity Protocol §6) |

---

## 6. Future Agents

No new agent may be added without (a) an entry in the table in §2, (b) a profile file
in `/04_agents/`, and (c) a routing rule in §3
(`LUMIAION_MASTER_ARCHITECTURE.md` §7 governance). Candidate future agents (not yet
built) that the schema already anticipates via `Owner Agent` as a multi-select rather
than a fixed enum:

- A dedicated **Symbolism & Archetypes** agent (School 8) if that department's volume
  eventually warrants its own reflex, rather than routing through Lumiaion directly.
- A **Client Portal / Coaching** agent once `Cohort/Program` tagging
  (`01_osg_grand_archives/DATABASE_BLUEPRINT.md` §5 Scale Engineering Notes) reaches
  enough concurrent cohorts to need its own queue.
