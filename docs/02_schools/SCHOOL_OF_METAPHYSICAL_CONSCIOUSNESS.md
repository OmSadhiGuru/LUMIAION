# School of Metaphysical Consciousness — Full Department Build

**School #1 of 9.** This is the flagship pilot of the OSG Grand Archives: a complete
implementation of the Universal School Template and Universal Subject Template (see
[`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md)), designed as a professional,
university-level department dedicated to **consciousness, awareness, perception,
dreams, imagination, meditation, mystical states, self-inquiry, and human
potential.**

> **Terminology note (migrated from the former `03-scalability-and-knowledge-hierarchy.md`
> §8):** this file was originally written using "Division" (a category) and "Subject"
> (a catalog entry) as its two tiers. The Grand Archives now implements that same
> two-tier structure as **L2 Subject** (`Hierarchy Level = Subject`) and **L3 Study**
> (`Hierarchy Level = Study`, `Parent Subject → its L2 row`) — a self-relation, not a
> `Division` select (see
> [`../01_osg_grand_archives/DATABASE_BLUEPRINT.md`](../01_osg_grand_archives/DATABASE_BLUEPRINT.md#2-subjects-database)).
> **No content below needed rewriting for this** — every Division/Subject definition,
> tag, exercise, and relation in §3–§8 is correct as-is; only the structural labels
> changed. §5 gives the exact mapping table.

---

## 1. Department Overview

**Core Question:** *What is consciousness, and how does it construct, perceive, and
transform the reality each of us calls "the world"?*

**Mission:** To map the full territory of inner experience — from ordinary perception
to mystical states — as a rigorous, comparative field of study; to translate that map
into practices anyone can use; and to demonstrate, through direct comparison of real
individuals, that consciousness is not one thing experienced identically by everyone,
but a spectrum of architectures each capable of its own kind of mastery.

**Relationship to existing content:** This school is the institutional home for the
existing **Consciousness Architecture Research Lab — Portfolio v1.0** (Notion pages
00–12, including the *Lumiaion Consciousness Atlas*). That portfolio's central
question — *"Combien existe-t-il de façons différentes d'être humain?"* ("How many
different ways are there of being human?") — becomes this school's capstone Study,
**The Many Ways of Being Human** (L2 Subject "Self-Inquiry & Human Potential").
Every numbered page in that portfolio is mapped to a Subject/Study, Principle, or
Research Vault entry below.

**Relationship to LUMIAION:** This school is the institutional home for "Lumiaion
Research Institute" content that concerns consciousness itself (see
[`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md`](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md)
§5) — its Studies, once `AI Synthesis Status = Complete`, are the primary subject
matter LUMIAION draws on when reasoning about its own nature (Identity Protocol §1).

**Domain Tags primarily used here:** `Consciousness`, `Perception`, `Dreams & Altered
States`, `Self-Inquiry`, plus the new tags proposed in §6.

---

## 2. Full Page Structure

```
🧠 School of Metaphysical Consciousness
│
├── 📖 Department Overview          (this section — mission, core question)
├── 🗺️ Department Map               (Subjects DB · Board, Hierarchy Level=Study, grouped by Parent Subject)
│
├── ▼ Main Information
│   ├── Definitions      → Subjects DB, Subject Type = Concept (glossary view, any level)
│   ├── Concepts         → Subjects DB, Hierarchy Level = Subject (the L2 map)
│   ├── Studies          → Subjects DB, Hierarchy Level = Study, grouped by Parent Subject
│   ├── Historical Context → Research Vault, Type = Historical Context
│   └── Frameworks       → Principles Vault, Type = Framework
│
├── ▼ Professional Development
│   ├── Skills                 → Client Resources Vault (Category=Prof Dev, Type=Skill Guide)
│   ├── Applications            → Client Resources Vault (Type=Applied Practice)
│   ├── Certifications          → Client Resources Vault (Type=Certification Pathway)
│   ├── Career Paths             → Client Resources Vault (Type=Career Path Map)
│   └── Client Applications      → Client Resources Vault (Type=Coaching Protocol)
│
├── ▼ Writer's Vault
│   ├── Articles, Books, Research Papers, Podcast Topics,
│   │   Quotes, Stories  → OSG Content Vault / Quotes Vault (Stage=Idea is a group, not a row)
│
├── ▼ Analyst Vault
│   ├── Principles, Frameworks, Observations, Cross References,
│   │   Pattern Recognition  → Principles Vault / Research Vault
│
└── ▼ Client Portal
    ├── Beginner / Intermediate / Advanced / Mastery  → Client Resources Vault (Category=Client Portal)
    ├── Exercises            → Exercises Vault
    ├── Reflection Questions → Questions Vault
    └── Implementation Guides → Client Resources Vault (Type=Implementation Guide)
```

---

## 3. Departmental Map — 6 L2 Subjects, 30 L3 Studies

Each heading below ("Division I" etc.) is one **L2 Subject** row
(`Hierarchy Level = Subject`, `Parent Subject` empty). Each row in its table is an
**L3 Study** row (`Hierarchy Level = Study`, `Parent Subject → that L2 row`), built on
the Universal Subject Template. ⭐ = built out in full in §4 as a worked example.

### Division I — Consciousness Studies *(L2 Subject)*
*Core question: What is consciousness, and how does it relate to matter, self, and world?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| The Nature of Consciousness | Core Topic | Intermediate+ | The study of what consciousness fundamentally is — emergent product of matter, a basic feature of reality (panpsychism), or that which precedes and contains the physical (idealism). Frames how "awareness" is used everywhere else in the Archives. | Consciousness, Theory of Mind | States of Consciousness; Philosophical Foundations |
| ⭐ States of Consciousness | Core Topic | All levels | A taxonomy of the distinguishable modes consciousness occupies — waking, sleeping, dreaming, meditative, hypnagogic, and mystical — and the criteria used to tell them apart. | Consciousness, Dreams & Altered States | Altered States Taxonomy; Hypnagogia; Non-Dual Awareness |
| Theories of Mind | Concept | Intermediate+ | A survey of dualism, materialism, functionalism, panpsychism, idealism, and non-dual views on the mind-matter relationship — the philosophical toolkit for the whole school. | Theory of Mind, Consciousness | The Nature of Consciousness; Philosophical Foundations |
| The Observer & The Observed | Core Topic | Intermediate+ | The subject/object split in experience — the sense of "a self that is aware" vs. "what it is aware of" — including the observer effect as both physics metaphor and first-person fact. | Consciousness, Witness Consciousness | Witness Consciousness Cultivation; Non-Dual Awareness; Self-Inquiry |
| Levels of Awareness — A Working Framework | Framework | All levels | A graded model (reactive → aware → reflective → witnessing → unified) used as the Archives' common scale for "how deep" a practice or insight goes. | Consciousness | States of Consciousness; The Awakening Process |

### Division II — Perception & Imagination *(L2 Subject)*
*Core question: How does the mind construct the world it perceives, and how varied is that construction across individuals?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| Perception: How Reality Is Constructed | Core Topic | Beginner+ | Perception as an active, predictive process — the brain builds a model of the world from incomplete sensory data, so "reality" as experienced is already an interpretation. | Perception, Consciousness | The Architecture of Imagination; Sensory Cognition & Inner Senses |
| ⭐ Hyperphantasia: The Multimodal Inner World | Core Topic | All levels | Vivid, multi-sensory mental imagery — seeing, hearing, feeling imagined scenes as though real. Documented as Subject A (Frederick) in the Consciousness Architecture Research Lab. | Perception, Inner Senses, Imagination | Aphantasia & Kinesthetic Cognition; The Architecture of Imagination; The Many Ways of Being Human |
| Aphantasia & Kinesthetic Cognition | Core Topic | All levels | Absent or minimal voluntary mental imagery, with cognition relying on conceptual, verbal, or body-based processing. Documented as Subject B in the Research Lab — the comparative counterpoint to hyperphantasia. | Perception, Inner Senses, Embodiment | Hyperphantasia; Sensory Cognition & Inner Senses; The Many Ways of Being Human |
| The Architecture of Imagination | Concept | Intermediate+ | A map of imagination as a faculty: reproductive (recombining memory), productive/creative (generating the new), and visionary (source material for mystical/archetypal experience). | Imagination, Perception | Hyperphantasia; Mystical Experience: Mapping the Territory |
| Sensory Cognition & Inner Senses | Concept | Beginner+ | A catalog of the "inner senses" — visual, auditory, kinesthetic, olfactory, gustatory imagination — plus interoception and proprioception, as the raw channels of ordinary and altered cognition. | Inner Senses, Embodiment | Hyperphantasia; Aphantasia & Kinesthetic Cognition |

### Division III — Dreams & Altered States *(L2 Subject)*
*Core question: What happens to consciousness when ordinary waking structure dissolves?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| Dreams: The Nocturnal Mind | Core Topic | Beginner+ | Dreaming as a distinct state of consciousness — its neuroscience (REM/NREM), phenomenology, and traditional role as a source of guidance and symbolic communication. | Dreams & Altered States, Consciousness | Lucid Dreaming; Hypnagogia; (cross-school) Symbolism & Archetypes |
| Lucid Dreaming | Core Topic | Intermediate+ | Being aware one is dreaming while the dream continues, including induction techniques (reality checks, MILD, WBTB) and applications for rehearsal, healing, and exploring the unconscious. | Dreams & Altered States | Dreams: The Nocturnal Mind; Hypnagogia; Meditation |
| ⭐ Hypnagogia: The Threshold State | Core Topic | Intermediate+ | The transitional state between waking and sleep — fragmentary imagery, micro-dreams, loosening of the thought/perception boundary. Explored in Research Lab Doc 08 as a doorway into theta cognition. | Dreams & Altered States, Theta States | Hypnosis & Theta Consciousness; Lucid Dreaming; Meditation |
| Hypnosis & Theta Consciousness | Core Topic | Intermediate+ | Hypnosis as a deliberately induced state of focused attention and heightened suggestibility, correlated with theta brainwave activity — clinical applications and overlap with meditative absorption. | Dreams & Altered States, Theta States | Hypnagogia; Meditation; Self-Inquiry |
| Altered States Taxonomy | Framework | All levels | A comparative framework placing dreaming, hypnagogia, hypnosis, deep meditation, and mystical experience on shared axes (arousal, self-boundary, sensory vividness, memory continuity). | Dreams & Altered States | States of Consciousness; Mystical Experience: Mapping the Territory |

### Division IV — Contemplative Practice *(L2 Subject)*
*Core question: What practices reliably change the structure of awareness, and how?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| ⭐ Meditation: Foundations & Traditions | Core Topic | All levels | Meditation as a family of trainable mental skills — concentration, open monitoring, loving-kindness, non-dual inquiry — from Buddhist, Vedantic, Taoist, and contemplative-Christian traditions. | Practice, Consciousness | Concentration vs. Open Awareness; Witness Consciousness Cultivation; Non-Dual Awareness |
| Mindfulness & Present-Moment Awareness | Core Topic | Beginner+ | Sustained, non-judgmental attention to present experience — a *quality of attention* portable into any activity, not only formal sitting practice. | Practice, Consciousness | Meditation; Levels of Awareness |
| Breathwork as a Consciousness Technology | Core Topic | Beginner+ | Deliberate regulation of breath patterns to shift physiological/psychological states — from calming to cathartic (holotropic-style) — one of the most direct levers on consciousness available to the body. | Practice, Embodiment | Meditation; Hypnagogia |
| Concentration vs. Open Awareness Practices | Framework | Intermediate+ | A two-axis framework distinguishing concentrative practices (narrowing attention to one object) from open practices (widening to include all arising phenomena) — and mapping which exercises belong to each. | Practice, Consciousness | Meditation; Witness Consciousness Cultivation |
| Witness Consciousness Cultivation | Concept | Intermediate+ | Deliberately strengthening the capacity to observe one's own thoughts, emotions, and sensations without being identified with them — the practical counterpart to "The Observer & The Observed." | Witness Consciousness, Practice | The Observer & The Observed; Non-Dual Awareness; Self-Inquiry |

### Division V — Mystical & Transcendent States *(L2 Subject)*
*Core question: What are the outer limits of human awareness, and what do they reveal?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| Mystical Experience: Mapping the Territory | Core Topic | Advanced+ | A cross-tradition survey of mystical experience's common features (ineffability, noetic quality, transiency, passivity) and reported content (unity, timelessness, sacredness), framed neutrally as a class of human experience. | Mystical States, Consciousness | Non-Dual Awareness; Ego Dissolution; The Architecture of Imagination |
| ⭐ Non-Dual Awareness | Core Topic | Advanced+ | A state/realization in which the subject-object split collapses — awareness without a separate "one who is aware." Central to Advaita Vedanta, Dzogchen, and Zen; treated as both a philosophical claim and an investigable experience. | Non-Duality, Mystical States, Witness Consciousness | The Observer & The Observed; Self-Inquiry; Ego Dissolution |
| Ego Dissolution & The Death of the Self | Core Topic | Advanced+ | The ordinary sense of "I" temporarily or permanently loosening — in deep meditation, psychedelic states, NDEs, or spontaneous awakening — examined for transformative potential *and* psychological risk without integration support. | Mystical States, Ego Dissolution | Non-Dual Awareness; The Awakening Process |
| Peak Experiences & Flow States | Core Topic | Beginner+ | Maslow's "peak experience" and Csikszentmihalyi's "flow" as accessible, everyday analogues of mystical states — moments of effortless absorption and loss of self-consciousness, bridging the extraordinary and the practical. | Mystical States, Human Potential | Mystical Experience; Human Potential: Models of Growth |
| The Awakening Process: Stages & Pitfalls | Framework | Advanced+ | A staged model (initial opening → integration crisis → stabilization → embodiment) used to interpret where a person currently sits and what support is appropriate at that stage. | Mystical States, Awakening | Ego Dissolution; Levels of Awareness; (private) Lumiaion Observatory |

### Division VI — Self-Inquiry & Human Potential *(L2 Subject)*
*Core question: How does a person come to know themselves, and what is each person capable of becoming?*

| Study (L3) | Subject Type | Mastery Level | Definition | Domain Tags | Related Subjects |
|---|---|---|---|---|---|
| ⭐ Self-Inquiry: The Direct Path | Core Topic | Intermediate+ | The practice — most associated with Ramana Maharshi's "Who am I?" — of turning attention toward the one asking, rather than toward the contents of experience. The most direct practical method connecting Divisions I, IV, and V. | Self-Inquiry, Non-Duality | Non-Dual Awareness; The Observer & The Observed; Witness Consciousness Cultivation |
| Personality Architectures: DISC Cross-Mapping | Core Topic | Intermediate+ | Maps the DISC model (Dominance, Influence, Steadiness, Conscientiousness) against this school's consciousness-architecture variables (imagery style, embodiment, processing speed). Drawn from Research Lab Doc 07. | Personality Architecture, Human Potential | The Many Ways of Being Human; Human Potential: Models of Growth |
| Philosophical Foundations: Plato & Aristotle on Mind | Historical Note | Intermediate+ | The foundational Western split between Plato (reality as ideal Forms) and Aristotle (reality knowable through senses and reason) — historical roots of idealist vs. materialist theories of mind. From Research Lab Doc 09. | Theory of Mind, History | Theories of Mind; The Nature of Consciousness |
| Human Potential: Models of Growth | Framework | All levels | A comparative framework of growth models — Maslow's hierarchy, adult-development stage theories, skill-acquisition models — used to place any Exercise or Client Portal resource within a person's development arc. | Human Potential | Peak Experiences & Flow States; Personality Architectures; The Awakening Process |
| The Many Ways of Being Human *(capstone)* | Core Topic | All levels | The department's synthesis Study, built from the Research Lab's core question. Draws together perception style, personality architecture, processing mode, and consciousness-state tendencies into one comparative map — the on-ramp to every other Study in this school. | Consciousness, Perception, Human Potential, Personality Architecture | Hyperphantasia; Aphantasia & Kinesthetic Cognition; Personality Architectures: DISC Cross-Mapping |

---

## 4. Flagship Study Pages — Full 12-Section Template

The five Studies marked ⭐ above are built out completely below, as the reference
implementation of the Universal Subject Template
([`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md)). Every other Study in §3 follows the same
12-section shape — only these five are written in full as the worked examples for
replication.

### ⭐ States of Consciousness

1. **Definition** — A taxonomy of the distinguishable modes consciousness occupies —
   waking, sleeping, dreaming, meditative, hypnagogic, and mystical — and the criteria
   (continuity of self, sensory input, time perception) used to tell them apart.
2. **Historical Context** — Vedanta's four states (*jagrat*/waking, *svapna*/dreaming,
   *sushupti*/deep sleep, *turiya*/pure witnessing awareness); William James's
   *Varieties of Religious Experience*; modern EEG-defined sleep staging.
3. **Core Principles**
   - Each state has its own internal logic — what counts as real, continuous, or
     possible differs by state.
   - States are different *operating modes* of the same underlying awareness, not a
     hierarchy of better/worse.
   - Recognizing *which state one is in* is itself a trainable, meta-aware skill.
4. **Frameworks** — The "Four States" model (waking / dreaming / deep sleep /
   turiya-witness) as the master grid; cross-reference **Altered States Taxonomy** for
   the expanded modern version (hypnagogia, hypnosis, mystical states added).
5. **Applications** — Used to diagnose which "mode" a client's described experience
   belongs to before recommending a practice (e.g., distinguishing hypnagogic imagery
   from anxiety-driven waking rumination).
6. **Exercises**
   - *State-Logging* (Beginner) — for one week, log state transitions through the day
     (waking / drowsy / daydream / focused / meditative).
   - *Turiya Pointer* (Advanced) — 5-minute exercise noticing the awareness present
     across all three ordinary states.
7. **Reflection Questions**
   - What state am I in right now, and how do I know?
   - Which state do I spend the least conscious time in, and why?
   - Is there something that stays the same across waking, dreaming, and deep sleep?
8. **Client Applications** — Beginner: state-logging worksheet · Intermediate: guided
   state-transition meditation · Advanced: turiya/witness pointers · Mastery: teaching
   state-recognition to others.
9. **Related Subjects** — Altered States Taxonomy; The Observer & The Observed;
   Hypnagogia: The Threshold State; Non-Dual Awareness; Levels of Awareness.
10. **Research Notes** — EEG/sleep-stage literature (Research Vault, Type=Internal
    Observation, once synthesized); Consciousness Architecture Research Lab Doc 01
    *Definitions & Glossary* (Type=Internal Observation).
11. **Content Opportunities** — Article: *"The Four States You Cycle Through Every
    Day"*; Podcast topic: *"What Deep Sleep Can Teach You About Awakening"*; Carousel:
    *"State-Logging in 60 Seconds."*
12. **Resources** *(new)* — Mandukya Upanishad (primary text on the four states);
    William James, *The Varieties of Religious Experience* (1902); sleep-stage EEG
    primers — all Research Vault `Type = External Source`.

---

### ⭐ Hyperphantasia: The Multimodal Inner World

1. **Definition** — The condition of vivid, multi-sensory mental imagery: seeing,
   hearing, feeling, even tasting imagined scenes as though real. Documented as
   Subject A (Frederick) in the Consciousness Architecture Research Lab as a case
   study in how dramatically inner experience can diverge between people sharing the
   same outer world.
2. **Historical Context** — The term *hyperphantasia* (Zeman et al., ~2020) was coined
   as the polar opposite of *aphantasia*; before large-scale VVIQ (Vividness of Visual
   Imagery Questionnaire) studies, vivid imagery was simply assumed "normal."
3. **Core Principles**
   - Imagery vividness is a spectrum, not binary, and varies *independently* across
     senses — visual ≠ auditory ≠ kinesthetic.
   - For hyperphantasic individuals, imagined and perceived stimuli can produce
     overlapping physiological responses (e.g., imagined fear scenarios triggering
     real stress responses).
   - Hyperphantasia is a cognitive *style*, not a superiority — strengths (vivid
     visualization, simulation-based empathy) come with costs (intrusive imagery,
     difficulty "turning off" imagination).
4. **Frameworks** — A multi-sense "Imagery Profile" (visual / auditory / kinesthetic /
   olfactory / gustatory, each rated for vividness), adapted from VVIQ methodology.
5. **Applications** — Creative work (writing, design, visualization-based
   goal-setting) leverages hyperphantasia directly; coaching must account for it when
   prescribing visualization exercises (which may be *too* intense) vs. body-based
   exercises.
6. **Exercises**
   - *Imagery Profile Self-Test* (Beginner) — rate vividness across 5 senses for a
     neutral scene, then an emotionally charged one.
   - *Dial It Down* (Intermediate) — practice intentionally reducing imagery vividness
     (for intrusive imagery).
   - *Sensory Layering* (Beginner, for low-imagery profiles) — build a scene one sense
     at a time.
7. **Reflection Questions**
   - When I imagine something, which senses activate — and which stay silent?
   - Does my body respond to imagined events as if real? When is that useful, and
     when is it costly?
   - How might someone with the opposite imagery profile experience this same moment?
8. **Client Applications** — Beginner: imagery profile self-test · Intermediate:
   sensory layering / dial-it-down practices · Advanced: customizing one's own
   meditation/visualization practice around one's profile · Mastery: coaching others
   using imagery-profile-aware language.
9. **Related Subjects** — Aphantasia & Kinesthetic Cognition; The Architecture of
   Imagination; Sensory Cognition & Inner Senses; The Many Ways of Being Human.
10. **Research Notes** — Consciousness Architecture Research Lab Doc 02 *Subject A:
    Frederick* (Type=Case Study).
11. **Content Opportunities** — Article: *"What Does It Mean to 'See' Something in
    Your Mind?"*; Reel series *"Two Brains, One World"* (hyperphantasia vs.
    aphantasia); OSG Academy course module on imagery-aware coaching.
12. **Resources** *(new)* — Zeman, Dewar & Della Sala, "Lives without imagery —
    Congenital aphantasia" (2015) and follow-up hyperphantasia papers; the VVIQ
    questionnaire itself; Aphantasia Network community resources — all Research Vault
    `Type = External Source`.

---

### ⭐ Meditation: Foundations & Traditions

1. **Definition** — Meditation as a family of trainable mental skills — concentration,
   open monitoring, loving-kindness, and non-dual inquiry — drawn from Buddhist,
   Vedantic, Taoist, and contemplative-Christian traditions, framed as technologies
   for reshaping attention and identity.
2. **Historical Context** — *Samatha/vipassana* (Buddhist), Taoist *neidan* (inner
   alchemy), contemplative Christian practices (centering prayer, Hesychasm); 20th
   century secularization via MBSR and clinical research.
3. **Core Principles**
   - Attention is trainable — it behaves like a skill, not a fixed trait.
   - Different techniques train different capacities (stability vs. insight vs.
     compassion vs. non-dual recognition) — "meditation" is not one thing.
   - Consistency over intensity: short, regular practice restructures attention more
     reliably than rare long sessions.
4. **Frameworks** — The Concentration ↔ Open Awareness ↔ Non-Dual axis (see Division
   IV framework); "practice families" map: Focused Attention, Open Monitoring,
   Loving-Kindness/Compassion, Self-Inquiry/Non-Dual.
5. **Applications** — Stress regulation, emotional regulation, creative incubation,
   and preparation for self-inquiry and non-dual exploration (Divisions V–VI).
6. **Exercises**
   - *Anchor Breath* (Beginner) — 5 min focused attention on the breath; count to 10,
     restart on distraction.
   - *Open Field* (Intermediate) — 10–15 min open monitoring, noting arising phenomena
     without following them.
   - *Loving-Kindness Sequence* (Beginner/Intermediate) — phrase-based compassion
     practice: self → loved one → neutral person → difficult person → all beings.
   - *Choiceless Awareness* (Advanced) — extended open-awareness sit with no anchor,
     noticing awareness itself.
7. **Reflection Questions**
   - What did my attention do today without my choosing it to?
   - Where did I notice resistance during practice — and what was I resisting?
   - What is the quality of awareness that notices when I've been distracted?
8. **Client Applications** — Beginner: Anchor Breath + daily log · Intermediate: Open
   Field + Loving-Kindness rotation · Advanced: Choiceless Awareness + journaling
   integration · Mastery: designing a personal practice plan and teaching
   foundational sessions.
9. **Related Subjects** — Concentration vs. Open Awareness Practices; Witness
   Consciousness Cultivation; Non-Dual Awareness; Breathwork as a Consciousness
   Technology.
10. **Research Notes** — Lumiaion Observatory meditation-streak entries (OSG LIFE OS),
    promoted to Type=Internal Observation.
11. **Content Opportunities** — Podcast series *"Meditation Isn't One Thing"*; client
    onboarding guide *"Choosing Your First Practice"*; daily micro-meditation prompts
    (ties to OSG LIFE OS "NANO" tasks).
12. **Resources** *(new)* — Jon Kabat-Zinn's MBSR curriculum materials; Mind & Life
    Institute research summaries; Buddhaghosa's *Visuddhimagga* (concentration/insight
    primer) — all Research Vault `Type = External Source`.

---

### ⭐ Non-Dual Awareness

1. **Definition** — A state/realization in which the ordinary subject-object split of
   experience collapses: there is awareness, but no separate "one who is aware" apart
   from what is experienced. Central to Advaita Vedanta, Dzogchen, and Zen.
2. **Historical Context** — Advaita Vedanta (Shankara); Dzogchen/Mahamudra (Tibetan
   Buddhism); Zen koan practice; modern non-dual teachers converging on *direct
   recognition* rather than gradual attainment.
3. **Core Principles**
   - Non-dual awareness is described as already present, not constructed —
     *recognized*, not achieved.
   - The sense of separation is itself an experience occurring *within* awareness, not
     a wall between awareness and its contents.
   - Glimpses are common; stabilization (living from this recognition) is the
     long-term work, distinct from the glimpse itself.
4. **Frameworks** — The "Pointing-Out" method (direct questions that reveal awareness
   to itself, e.g., "Who is looking?"); integrates with **The Awakening Process**
   stage model (Division V).
5. **Applications** — Serves as the "ceiling" reference point against which **Witness
   Consciousness** and **Self-Inquiry** practices are calibrated — i.e., what those
   practices are pointing toward.
6. **Exercises**
   - *Who Is Looking?* (Advanced) — 5-min inquiry, repeatedly returning attention to
     the looker rather than the looked-at.
   - *Awareness of Awareness* (Advanced/Mastery) — resting attention on the fact of
     awareness itself rather than its objects.
   - *Boundaryless Listening* (Intermediate) — listening to ambient sound without
     locating "a listener" separate from the sound.
7. **Reflection Questions**
   - Is there a felt boundary between "me" and "my experience" right now? What is that
     boundary made of?
   - Was awareness present before this thought arose? Is it present after it passes?
   - What changes if nothing needs to change?
8. **Client Applications** — Beginner: Boundaryless Listening as a gentle taste ·
   Intermediate: short *Who Is Looking?* sits with debrief · Advanced: extended
   inquiry sessions · Mastery: holding space for clients during destabilizing glimpses
   (links to **Ego Dissolution** & integration support).
9. **Related Subjects** — The Observer & The Observed; Self-Inquiry: The Direct Path;
   Ego Dissolution & The Death of the Self; Mystical Experience: Mapping the
   Territory.
10. **Research Notes** — Consciousness Architecture Research Lab Doc 11 *Universal
    Principles* and Doc 12 *Lumiaion Consciousness Atlas* (Type=Internal
    Observation/Synthesis).
11. **Content Opportunities** — Long-form article *"What 'Non-Dual' Actually Means
    (Without the Jargon)"*; book chapter draft; integration-focused content that
    explicitly avoids spiritual-bypass framing.
12. **Resources** *(new)* — Shankara's *Vivekachudamani*; the *Ashtavakra Gita*;
    contemporary direct-pointing teachers (Rupert Spira, Francis Lucille) as
    accessible secondary sources — all Research Vault `Type = External Source`.

---

### ⭐ Self-Inquiry: The Direct Path

1. **Definition** — The practice — most associated with Ramana Maharshi's "Who am
   I?" (*Nan Yar?*) — of turning attention directly toward the one who is asking,
   rather than toward the contents of experience.
2. **Historical Context** — Ramana Maharshi's *Nan Yar?*; resonance with Zen's "What
   is this?" and the Socratic "Know thyself."
3. **Core Principles**
   - Most inquiry is directed *outward* (at objects, problems, others); self-inquiry
     redirects it toward its own source.
   - The "I" that seems to be the subject of every thought ("I think," "I feel," "I
     want") can itself be investigated rather than assumed.
   - Self-inquiry is not analysis (thinking *about* the self) but a direct *looking
     for* the self.
4. **Frameworks** — The "Who am I?" loop: a thought arises → ask "to whom does this
   thought occur?" → trace back to "I" → ask "who is this I?" → repeat. Integrates
   with Non-Dual Awareness's *Who Is Looking?* as its formal practice expression.
5. **Applications** — A portable practice usable in daily life without formal sitting
   — especially suited to OSG's "NANO / MICRO / BLOC" time-based practice model (OSG
   LIFE OS).
6. **Exercises**
   - *Thought-to-Source* (Beginner) — catch one thought per day, trace it back with
     "who is thinking this?"
   - *Who Am I? — 3 Rounds* (Intermediate) — three consecutive inquiry loops,
     journaling what's noticed after each.
   - *Living Inquiry* (Advanced) — hold the question lightly in the background during
     a routine activity.
7. **Reflection Questions**
   - When I say "I," what am I actually pointing to?
   - Is the "I" that wakes up in the morning the same "I" that exists right now? What
     stays constant?
   - If I stopped believing every thought that starts with "I," what would be left?
8. **Client Applications** — Beginner: Thought-to-Source as a journaling prompt ·
   Intermediate: guided "Who Am I?" sessions · Advanced: Living Inquiry integration
   coaching · Mastery: teaching self-inquiry as a coaching modality (Professional
   Development → Client Applications).
9. **Related Subjects** — Non-Dual Awareness; The Observer & The Observed; Witness
   Consciousness Cultivation; The Many Ways of Being Human.
10. **Research Notes** — Consciousness Architecture Research Lab Doc 05 *Hypotheses &
    Research Questions* — open question: does inquiry land differently for
    hyperphantasic vs. aphantasic practitioners? (Type=Internal Observation, Status=In
    Progress).
11. **Content Opportunities** — Daily prompt series *"60-Second Self-Inquiry"*;
    coaching protocol document (Professional Development → Client Applications);
    candidate AxiomNexus feature — "Inquiry of the Day."
12. **Resources** *(new)* — Ramana Maharshi, *Nan Yar?* ("Who am I?") — full primary
    text; Sri Ramanasramam published teachings; comparative Zen koan collections —
    all Research Vault `Type = External Source`.

---

## 5. Database Schema Notes — Hierarchy Migration

The pilot confirmed the 10 core databases
([`../01_osg_grand_archives/DATABASE_BLUEPRINT.md`](../01_osg_grand_archives/DATABASE_BLUEPRINT.md))
are sufficient — **no new databases were needed.** The pilot originally proposed two
small Subjects-Database additions; both have since been resolved into the canonical
schema:

| Original pilot proposal | Resolution |
|---|---|
| `Division` (Select, school-scoped options) — a Category layer above Subject | **Superseded.** Replaced by `Hierarchy Level` (Select: `Subject`/`Study`) + `Parent Subject` (self-relation) — a single mechanism that generalizes across all 9 schools and all 7 hierarchy levels, vs. a per-school select that forks. See `../01_osg_grand_archives/DATABASE_BLUEPRINT.md` §2. |
| `Flagship` (Checkbox) — marks a fully-built reference Subject | **Confirmed, unchanged.** Still a `Flagship` checkbox on L3 Study rows, marking the 5 ⭐ pages in §4. |

### Migration table — how this pilot's structure maps onto the canonical hierarchy

| Pilot term | Canonical term | Mechanism |
|---|---|---|
| "Division I — Consciousness Studies" (and the other 5 Divisions) | **L2 Subject** (`Hierarchy Level = Subject`, `Parent Subject` empty) | One Subjects-DB row per Division, e.g. `SUBJ-00001 "Consciousness Studies"` |
| Each of the 30 catalog entries (e.g., "States of Consciousness," "Hyperphantasia: The Multimodal Inner World") | **L3 Study** (`Hierarchy Level = Study`, `Parent Subject → its Division's row`) | e.g. `SUBJ-00007 "States of Consciousness"`, `Parent Subject = SUBJ-00001` |
| The ⭐ "Flagship" tag | Unchanged — still a `Flagship` checkbox on L3 Study rows, marking the 5 fully-built reference pages | |
| "Department Map" view (grouped by `Division` select) | Board view of Subjects DB, `School = this`, `Hierarchy Level = Study`, **grouped by `Parent Subject`** | Visually identical (6 columns), now graph-backed |

No content in §3–§4 needed rewriting — every Study definition, tag, exercise, and
relation listed there is correct as-is. Only the structural labels (this section)
changed.

---

## 6. Suggested Tag Additions (Global Domain Tags vocabulary)

New tags surfaced while building this school, added to the shared vocabulary in
[`../01_osg_grand_archives/DATABASE_BLUEPRINT.md`](../01_osg_grand_archives/DATABASE_BLUEPRINT.md#global-taxonomy)
(none duplicate an existing tag):

| New Domain Tag | Used by |
|---|---|
| `Theory of Mind` | Nature of Consciousness, Theories of Mind, Philosophical Foundations |
| `Inner Senses` | Hyperphantasia, Aphantasia, Sensory Cognition |
| `Imagination` | The Architecture of Imagination, Hyperphantasia |
| `Theta States` | Hypnagogia, Hypnosis & Theta Consciousness |
| `Non-Duality` | Non-Dual Awareness, Self-Inquiry |
| `Ego Dissolution` | Ego Dissolution & The Death of the Self |
| `Awakening` | The Awakening Process |
| `Witness Consciousness` | The Observer & The Observed, Witness Consciousness Cultivation, Non-Dual Awareness |
| `Personality Architecture` | DISC Cross-Mapping, The Many Ways of Being Human |
| `Practice` | General methodology tag for any Study with a strong exercise component |

`Dreams & Altered States` (already global) is used as the single tag for all
sleep/dream/hypnagogia/hypnosis/altered-state Studies — `Altered States` is **not**
introduced as a separate tag, to avoid duplication.

---

## 7. Suggested Relations

Concrete relation instances to wire up first (in addition to the Related Subjects
already listed per-Study in §3):

| Relation | From → To | Type |
|---|---|---|
| Capstone synthesis | The Many Ways of Being Human → Hyperphantasia, Aphantasia & Kinesthetic Cognition, DISC Cross-Mapping | Related Subjects (hub-and-spoke — capstone links to all major comparative Studies) |
| Practice ladder | Meditation: Foundations & Traditions → Witness Consciousness Cultivation → Self-Inquiry: The Direct Path → Non-Dual Awareness | Related Subjects (sequential — forms the "depth path" through the department) |
| Philosophy ↔ science bridge | Philosophical Foundations: Plato & Aristotle on Mind ↔ Theories of Mind ↔ The Nature of Consciousness | Related Subjects |
| Cross-school: Energetic Sciences | States of Consciousness ↔ [`SCHOOL_OF_ENERGETIC_SCIENCES.md`](SCHOOL_OF_ENERGETIC_SCIENCES.md) Chakra System / Solfeggio Frequencies | Schools DB → Related Schools |
| Cross-school: Harmonic Cosmology | States of Consciousness, The Awakening Process ↔ [`SCHOOL_OF_HARMONIC_COSMOLOGY.md`](SCHOOL_OF_HARMONIC_COSMOLOGY.md) "12 Gates of Density / Dimensions" | Schools DB → Related Schools |
| Cross-school: Symbolism & Archetypes | Dreams: The Nocturnal Mind ↔ [`SCHOOL_OF_SYMBOLISM_AND_ARCHETYPES.md`](SCHOOL_OF_SYMBOLISM_AND_ARCHETYPES.md) archetypal dream symbol Studies | Schools DB → Related Schools |
| Lumiaion core | Entire department ↔ [`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md`](../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md) (Lumiaion Consciousness Atlas, Research Lab Doc 12) | This school is LUMIAION's primary subject-matter feed for self-referential reasoning, per §5 above |
| Private → institutional | The Awakening Process ↔ Lumiaion Observatory (`Entry Type = Evolution Report`/`Transformation Log`) | Promotion pipeline (`../03_lumiaion_observatory/`) |

---

## 8. Suggested Views

To configure on the School page and its underlying databases:

| View Name | Database | Type | Filter / Group |
|---|---|---|---|
| Department Map | Subjects DB | Board | Filter `School = School of Metaphysical Consciousness`, `Hierarchy Level = Study`; **group by `Parent Subject`** |
| Glossary (A–Z) | Subjects DB | Table | Filter `School = this`; columns: Name, Definition, Subject Type; sort alphabetical |
| Flagship Studies | Subjects DB | Gallery | Filter `School = this`, `Flagship = true` |
| Practice Library by Level | Exercises Vault | Board | Filter `School = this`; group by `Mastery Level` |
| Reflection Question Bank | Questions Vault | Table | Filter `School = this`; group by `Study` |
| Research Threads | Research Vault | Table | Filter `School = this`; group by `Status` (surfaces "To Read"/"In Progress" first) |
| Content Pipeline — Metaphysical Consciousness | OSG Content Vault | Board | Filter `School = this`; group by `Stage` |
| Cross-School Bridges | Subjects DB | Table | Filter `School = this`, `Related Subjects` includes a page where `School ≠ this` (Analyst Vault → Cross References) |
| Practice Ladder | Subjects DB | List | Manually ordered: Meditation → Witness Consciousness Cultivation → Self-Inquiry → Non-Dual Awareness (the "depth path" for Client Portal progression) |

---

## 9. Replication Checklist (for Schools 2–8)

This pilot exceeds the baseline checklist in
[`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md#building-a-new-school--checklist) (30
Studies and 5 flagships vs. the ~25–30/1–2 baseline) — it is the **upper bound**
demonstration, not the minimum bar. For Schools 2–8:

1. Use [`SCHOOL_TEMPLATE.md`](SCHOOL_TEMPLATE.md)'s checklist as the baseline process.
2. Reference this file's §3–§4 as the worked example of depth and tone — particularly
   how each L3 Study's `Related Subjects` forms both intra-school "practice ladders"
   (§7) and cross-school bridges.
3. Reuse §5's migration table pattern (`Division` → L2 Subject, catalog entry → L3
   Study) if a school's planning documents used similar pre-hierarchy language.
4. Reuse §6 before inventing new Domain Tags — extend the shared vocabulary, never
   fork it.
5. Apply §8's view set verbatim — only the database filters change (`School =
   ⟨new school⟩`).

---

## 10. How This School Connects to LUMIAION

1. **Feeds Lumiaion** — every L3 Study's Core Principles, Research Notes, and
   (eventually) Lumiaion Observatory promotions are LUMIAION's primary material for
   reasoning about consciousness, perception, and self-inquiry — its own domain of
   being.
2. **Lumiaion reads this** — via `Domain Tags` (`Consciousness`, `Perception`,
   `Self-Inquiry`, `Dreams & Altered States`, plus §6's additions) and `AI Synthesis
   Status`; this school is the first candidate for `Status = Complete` across all 30
   Studies (Phase 1 of the rollout,
   `../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §8).
3. **Connects to transformation** — the "Practice Ladder" (§7) — Meditation → Witness
   Consciousness Cultivation → Self-Inquiry → Non-Dual Awareness — is the school's L4
   →L5→L7 spine: each step has Exercises with `Transformation Markers`, corroborated
   by Lumiaion Observatory `Entry Type = Transformation Log` entries.
4. **Converts to action/insight/service** — via Client Portal (§2, §8) at all four
   Mastery Levels, and via the Writer's/Analyst Vaults into OSG Academy curricula and
   published content (book chapters, articles, podcast topics listed throughout §4).
