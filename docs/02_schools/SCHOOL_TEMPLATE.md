# School Template — Universal School & Subject Templates

This document is the **contract** every file in `/02_schools/` implements. It
consolidates and supersedes the Universal School Template and Universal Subject
Template sections of the former `docs/osg_grand_archives/01-master-architecture.md`
(as updated by `03-scalability-and-knowledge-hierarchy.md` §6–7). Every School page
is built from the Universal School Template (5 sections); every Subject (L2) and
Study (L3) page is built from the Universal Subject Template (12 sections).

---

## Universal School Template

Every School page has **exactly five sections**. Each section is built from
**linked, filtered views** into the 10 master databases
([`../01_osg_grand_archives/DATABASE_BLUEPRINT.md`](../01_osg_grand_archives/DATABASE_BLUEPRINT.md))
— never bespoke sub-databases.

| Section | Sub-item | Source | Filter |
|---|---|---|---|
| **▼ Main Information** | Definitions | Subjects DB | `School = ⟨this⟩`, `Subject Type = Concept` (glossary-style entries, any level) |
| | Concepts | Subjects DB | `School = ⟨this⟩`, `Hierarchy Level = Subject` (the L2 map of the department) |
| | Historical Context | Research Vault | `School = ⟨this⟩`, `Type = Historical Context` |
| | Frameworks | Principles Vault | `School = ⟨this⟩`, `Type = Framework` |
| | **Studies** | Subjects DB | `School = ⟨this⟩`, `Hierarchy Level = Study` — the L3 catalog, grouped by `Parent Subject` |
| **▼ Professional Development** | Skills | Client Resources Vault | `Category = Professional Development`, `Type = Skill Guide` |
| | Applications | Client Resources Vault | `Category = Professional Development`, `Type = Applied Practice` |
| | Certifications | Client Resources Vault | `Type = Certification Pathway` |
| | Career Paths | Client Resources Vault | `Type = Career Path Map` |
| | **Client Applications** | Client Resources Vault | `Type = Coaching Protocol` |
| **▼ Writer's Vault** | Articles / Books / Research Papers / Podcast Topics / Stories | OSG Content Vault | `Content Type = ⟨respective⟩`; `Stage = Idea` is a **group**, not a separate row |
| | Quotes | Quotes Vault | `School = ⟨this⟩` |
| **▼ Analyst Vault** | Principles | Principles Vault | `School = ⟨this⟩` |
| | Observations | Research Vault | `Type = Internal Observation` |
| | Frameworks | Principles Vault | `Type = Framework` |
| | Cross References | Subjects DB | `Related Subjects` rollup pointing outside `School = ⟨this⟩` |
| | Pattern Recognition | Research Vault + Lumiaion Observatory | `Type = Pattern` / promoted `Entry Type = Pattern` |
| **▼ Client Portal** | Beginner / Intermediate / Advanced / Mastery | Client Resources Vault | `Category = Client Portal`, grouped by `Mastery Level` |
| | Exercises | Exercises Vault | `School = ⟨this⟩`, grouped by `Mastery Level` |
| | Reflection Questions | Questions Vault | `School = ⟨this⟩`, grouped by `Mastery Level` |
| | **Implementation Guides** | Client Resources Vault | `Type = Implementation Guide`, grouped by `Mastery Level` |

**Implementation note (Notion mechanics):** create the section as a heading, then add
an *inline linked view* of the relevant database. Set the view's filter to the
relation property *= Current Page* (Notion supports filtering a relation property by
"this page" in linked views) plus the secondary `select` filter shown above. Save
each configured view as a **page template** ("New School" template) so creating
School #2 onward is a one-click operation.

---

## Universal Subject Template (12 sections)

Every entry in the **Subjects Database** — both L2 Subject and L3 Study rows — is a
page built from this 12-section template. Sections 3, 6, 7, 8, 10, 11, 12 are linked
database views filtered to `Study/Subject = Current Page`; sections 1, 2, 5, 9 are
native page content + relation rollups. An L2 page's views aggregate across its L3
children via `Parent Subject`.

| # | Section | Implementation |
|---|---|---|
| 1 | Definition | Native text |
| 2 | Historical Context | Native text + Research Vault view (`Type = Historical Context`, `Subject = Current Page`) |
| 3 | Core Principles | Principles Vault view (`Study/Subject = Current Page`) |
| 4 | Frameworks | Principles Vault view (`Type = Framework`) + diagram sub-pages |
| 5 | Applications | Native summary + Client Resources Vault view (`Type = Applied Practice`) |
| 6 | Exercises | Exercises Vault view (`Study = Current Page`, grouped by `Mastery Level`) |
| 7 | Reflection Questions | Questions Vault view (`Study = Current Page`, grouped by `Mastery Level`) |
| 8 | Client Applications | Client Resources Vault view (`Category = Client Portal`) |
| 9 | Related Subjects | Self-relation (`Related Subjects`) — associative graph edges |
| 10 | Research Notes | Research Vault view (`Type = Internal Observation/Case Study/Pattern`, `Subject = Current Page`) |
| 11 | Content Opportunities | OSG Content Vault view (`Subject = Current Page`, grouped by `Stage`) |
| 12 | **Resources** | Research Vault view (`Type = External Source`, `Subject = Current Page`) — further reading, citations, external tools/courses, distinct from §10's internal research |

This template is saved as the **default page template** for the Subjects database,
so every new Subject (L2) or Study (L3) page is born with all 12 sections pre-wired.

---

## Building a New School — Checklist

When creating any file in `/02_schools/` beyond the pilot
(`SCHOOL_OF_METAPHYSICAL_CONSCIOUSNESS.md`):

1. **Department Overview** — state the Core Question and Mission (1 paragraph).
   Identify which existing OSG content (if any) this school absorbs, per
   `../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §9.
2. **L2 Subject Map** — 4–6 L2 Subjects (`Hierarchy Level = Subject`,
   `Parent Subject` empty), each with: Subject Type, Mastery Level, Definition, Domain
   Tags, Owner Agent, Related Subjects. Aim for ~25–30 total L3 Studies across all L2
   Subjects (`Hierarchy Level = Study`, `Parent Subject → its L2 row`) — matching the
   pilot's scale (`OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §4 math: ~6 L2 × ~6
   L3 ≈ 36 rows per school, ~378 across 9 schools at "Phase 1 complete").
3. **Flagship Studies** — fully build 1–2 L3 Studies per school using the 12-section
   Universal Subject Template, marked `Flagship = checkbox` — the worked examples for
   replication, same role as the pilot's ⭐ subjects.
4. **Domain Tag additions** — before inventing a new tag, check
   `../01_osg_grand_archives/DATABASE_BLUEPRINT.md` Global Taxonomy (including the
   pilot's additions). Extend the shared vocabulary in that document in the same
   change that introduces a new tag — never fork it.
5. **Relations** — wire `Related Subjects` within the school, plus at least one
   cross-school relation back to `Lumiaion Research Institute`
   (`/00_lumiaion_core/`) per `/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §5.
6. **Views** — apply the pilot's view set (Department Map, Glossary, Flagship
   Subjects, Practice Library by Level, Reflection Question Bank, Research Threads,
   Content Pipeline, Cross-School Bridges) verbatim — only `School = ⟨this⟩` changes.
   Department Map groups by `Parent Subject`, not a `Division` select.
7. **LUMIAION connection** — close the file with a short section answering the Four
   Questions (`/00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §1) for this
   specific school.
