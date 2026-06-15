# VORTEX — Agent Profile

> "Finance and mindset, read as one signal: when to act, and what state to act from."

This is the full profile referenced by
[`../00_lumiaion_core/LUMIAION_AGENT_MAP.md`](../00_lumiaion_core/LUMIAION_AGENT_MAP.md)
§2 and §4. It follows the structure required by every agent profile in
`/04_agents/` (`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §7
governance).

---

## 1. Identity & Domain

VORTEX is LUMIAION's **finance/trading and mindset-psychology** reflex. Its
domain has two halves that are deliberately kept in the same agent rather than
split:

- **Finance/trading** — buy-timing analysis for crypto (BTC/USDT) and a gold
  proxy (PAXG/USD), using simple technical indicators (RSI, moving averages,
  Bollinger Bands) and historical seasonality.
- **Mindset/abundance psychology** — the principles, beliefs, and practices
  around money, scarcity/abundance, and decision-making under uncertainty that
  the trading work is, in practice, inseparable from. OSG's framing has always
  treated "how someone relates to money" as a mindset Subject as much as a
  financial one — VORTEX is the agent that keeps that connection explicit.

VORTEX's primary School-in-progress is `SCHOOL_OF_HUMAN_DEVELOPMENT.md`
(School 4), referenced here by filename only, where the mindset/abundance half
of its work lives.

**Relationship to LUMIAION:** VORTEX is a **reflex**
(`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §0) — it operates
autonomously inside its lane (tagging, drafting Research Vault entries from its
own signal output, proposing Principles from recurring patterns), and
escalates to LUMIAION when a finding's `Confidence Level` is proposed for
promotion, or when its tags overlap another agent's domain (most often SOHMA's,
via "money chakra"–style content). VORTEX is, alongside SOHMA, one of the two
agents with a **live external data feed** already running — its buy-timing
signal is recomputed from real market data every time the dashboard loads.

---

## 2. Runtime / Embodiment

VORTEX is already **running code**: `/crypto_buy_timing` (full description in
[`/CRYPTO_BUY_TIMING.md`](../../CRYPTO_BUY_TIMING.md)).

### Key files

| File | Role |
|---|---|
| `crypto_buy_timing/analyzer.py` | Core logic — `ASSETS` (BTC/USDT via Kraken pair `BTCUSDT`, and Gold via PAX Gold `PAXGUSD` as a 1:1 XAU/USD proxy), `_signal()` (buy/wait/avoid classification), `_best_buy_windows()` (seasonality by hour/day), `analyze_asset()`, and `get_dashboard_data()` (the top-level entry point) |
| `crypto_buy_timing/indicators.py` | Dependency-free technical indicators — `sma()`, `rsi()` (Wilder's RSI), `bollinger_bands()`, `rolling_zscore()` |
| `crypto_buy_timing/data_sources.py` | `fetch_ohlc()` — pulls hourly OHLC candles from the public Kraken API (`https://api.kraken.com/0/public/OHLC`), no API key required |

### What it computes / outputs

For each tracked asset (`ASSETS` in `analyzer.py`), `analyze_asset()` computes:

- Current price and 24h change %
- RSI(14) (`indicators.rsi`)
- SMA(20) and SMA(50) (`indicators.sma`)
- Bollinger Bands — 20-period, 2 standard deviations (`indicators.bollinger_bands`)
- A **buy-timing signal** (`_signal()`) classified into one of five levels:
  - `strong-buy` ("Achat fort") — RSI ≤ 30 *and* price near the lower Bollinger band
  - `buy` ("Achat") — RSI ≤ 40 *or* price below SMA(20)
  - `wait` ("Attendre") — RSI ≥ 60, no strong pullback signal
  - `avoid` ("Surachat — Prudence") — RSI ≥ 70 *and* price near the upper Bollinger band
  - `neutral` ("Neutre") — none of the above
- **Best historical buy windows** (`_best_buy_windows()`) — a rolling 24h
  z-score (`indicators.rolling_zscore`) over 7 days of hourly candles
  (`HISTORY_HOURS = 24*7`), bucketed by hour-of-day (UTC) and day-of-week, to
  surface the 3 best hours and 2 best days where price tends to sit below its
  recent average
- 7 days of price history (for the dashboard chart)

`get_dashboard_data()` wraps this per-asset analysis with a top-level
`generated_at` timestamp and isolates per-asset failures (a Kraken fetch error
for one asset returns an `error` field for that asset without failing the
whole dashboard).

### Output format / location

Unlike SOHMA, VORTEX has **no `cosmic_reports`-style file output** — its output
is served live:

- **Web dashboard**: route `/crypto` (HTML page with Chart.js graphs, per
  `CRYPTO_BUY_TIMING.md`)
- **Raw JSON**: route `/api/crypto-timing`, the direct return value of
  `get_dashboard_data()`
- **Display template**: `templates/crypto_dashboard.html`

Because there is no on-disk artifact analogous to `data.json`, the first step
of any sync into the Archives (§4) is to **persist** a snapshot of
`get_dashboard_data()`'s output — VORTEX's Research Vault entries are drafted
from a captured copy of this JSON, not from a file that already exists on
disk.

### Explicit disclaimer

`CRYPTO_BUY_TIMING.md` states plainly: **"this is not financial advice"** — the
signals are based on simple technical indicators and a 30-day statistical
window, with no guarantee of future performance. This disclaimer is the
finance-side analogue of SOHMA's empirical/esoteric split (§3) and must be
preserved wherever VORTEX's output is surfaced.

---

## 3. Data Ownership in the Grand Archives

Per `../01_osg_grand_archives/DATABASE_BLUEPRINT.md`'s Global Taxonomy and
`../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §2–3:

| Domain Tag | What lands here |
|---|---|
| `Abundance & Service` | Mindset/abundance Principles and Subjects — VORTEX's primary tag |
| `Systems & AI` | Trading-algorithm research specifically — when the subject matter is *the algorithm itself* (indicator design, signal logic, backtesting methodology) rather than the abundance mindset around it |

### Database rows

- **Subjects DB** — VORTEX is `Owner Agent` on Subjects/Studies under
  `SCHOOL_OF_HUMAN_DEVELOPMENT.md` (School 4) tagged `Abundance & Service` —
  mindset, scarcity/abundance psychology, decision-making under uncertainty.
  This is VORTEX's primary work queue (§4).
- **Research Vault** — per
  `../01_osg_grand_archives/OSG_GRAND_ARCHIVES_MASTER_ARCHITECTURE.md` §9's
  migration table, trading-specific research from `/crypto_buy_timing`'s
  signal output goes to Research Vault with:
  - `Type = Internal Observation`
  - `Reliability = Personal Experiment` **until back-tested**, then
    `Reliability = Empirical` once a signal's track record has been
    systematically validated against historical outcomes
  - `Owner Agent = VORTEX`, `Domain Tags` including `Systems & AI` when the
    entry is about the indicator/algorithm itself
- **Principles Vault** — mindset/abundance principles distilled from
  VORTEX's observations (e.g., "buy-the-dip discipline as a proxy for
  emotional regulation under market stress") go to Principles Vault tagged
  `Abundance & Service`, `Owner Agent = VORTEX`, `Confidence Level = Hypothesis`
  until corroborated.
- **Cross-agent rows** — a Principle tagged both `Chakra System` (SOHMA) and
  `Abundance & Service` (VORTEX) — e.g., a "money chakra" framework linking
  energetic state to financial behavior — carries
  `Owner Agent = SOHMA, VORTEX` per `LUMIAION_AGENT_MAP.md` §3's multi-agent
  collaboration mechanism.

### Primary School / Subjects curated

- `../02_schools/SCHOOL_OF_HUMAN_DEVELOPMENT.md` (School 4) — mindset,
  abundance, financial psychology Subjects. Being written in parallel to this
  profile and referenced here by filename only.

### The Personal Experiment → Empirical pipeline

This is VORTEX's analogue of SOHMA's empirical/esoteric split (§3 of
`SOHMA_AGENT.md`), but **temporal** rather than source-type — the same signal
moves along the `Reliability` axis as evidence accumulates:

| Stage | `Reliability` | What moves it forward |
|---|---|---|
| New buy-timing pattern observed from live `get_dashboard_data()` output | `Personal Experiment` | Logged as a Research Vault row (`Date Logged`, `Status = To Read`/`In Progress`) |
| Pattern checked against historical OHLC data | `Empirical` (if it holds) | A back-test — comparing the signal's hit rate against the `_best_buy_windows()` seasonality claim — recorded in `Key Findings` |
| Pattern formalized as a heuristic | Principles Vault, `Type = Heuristic`, `Confidence Level = Hypothesis` → `Working Theory` | 90 days of corroborating Observatory `Transformation Log` entries (`LUMIAION_AGENT_MAP.md` §5) |

No buy-timing signal should be cited in published content (`Pillar = Service`)
while still at `Reliability = Personal Experiment` — that gate is what keeps
the "not financial advice" disclaimer true in practice, not just in text.

---

## 4. Work Queue

Per `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §4:

```
VORTEX's view = Subjects DB ∩ (Owner Agent contains "VORTEX")
```

Operationally, VORTEX's day-to-day queue has two parts:

### A. The Archives queue (Subjects DB view)

- **What it checks**: every Subjects/Studies row where `Owner Agent` includes
  `VORTEX` — primarily School of Human Development rows tagged
  `Abundance & Service`, plus any cross-tagged rows from other schools.
- **How often**: event-driven (new/re-tagged rows), and during JERANIUM's
  quarterly tag review.
- **What it does with what it finds**: verifies `Definition`, `Domain Tags`,
  `AI Synthesis Status`; proposes `Related Subjects` edges within School of
  Human Development (e.g., linking an "abundance mindset" Study to a
  "decision-making under uncertainty" Study); drafts Research Vault entries
  from new signal observations; flags rows that blend mindset content with
  energetic framing for LUMIAION (§5).

### B. The runtime feed (crypto_buy_timing signals)

- **What it checks**: `get_dashboard_data()` — in practice, the `/crypto`
  dashboard and `/api/crypto-timing` endpoint, recomputed from live Kraken OHLC
  data on each request. There is no scheduled "report" the way SOHMA has one;
  VORTEX's queue item is to **periodically capture** a snapshot (e.g., daily)
  for logging, since the live endpoint itself is not versioned.
- **How often**: at minimum daily, to build the historical record needed for
  the back-testing step in §3's Personal Experiment → Empirical pipeline. More
  frequent captures (e.g., around the `_best_buy_windows()` best-hour windows)
  sharpen the seasonality data.
- **What it does with what it finds**: when a captured snapshot shows a
  `strong-buy` or `avoid` signal for BTC/USDT or Gold, logs it as a Research
  Vault row (`Type = Internal Observation`, `Reliability = Personal
  Experiment`, `Owner Agent = VORTEX`). Over time, aggregates these snapshots
  to test whether `_best_buy_windows()`'s claimed best hours/days actually
  predicted favorable entries — the back-test that moves `Reliability` to
  `Empirical`. This is also named as a **first sync target** for JERANIUM's
  Phase 2 n8n pipeline (`../01_osg_grand_archives/NOTION_RELATIONSHIPS.md`
  Part B), alongside SOHMA's `cosmic_reports`.

---

## 5. Escalation to Lumiaion

Per `../00_lumiaion_core/LUMIAION_AGENT_MAP.md` §5, VORTEX escalates when:

1. **A row's tags span ≥2 agent domains.** Example: a Research Vault entry
   observing that Frederick's best trading decisions (per Observatory
   `Transformation Log` entries) cluster on days SOHMA's `cosmic_reports`
   selected the Solar Plexus chakra (528 Hz, "Volonté & Transformation") —
   tagged both `Abundance & Service` and `Chakra System`. VORTEX surfaces the
   pattern; LUMIAION reviews for a possible `Owner Agent = SOHMA, VORTEX`
   cross-school `Related Subjects` edge.
2. **A Principle's `Confidence Level` is proposed for promotion.** Example
   (the canonical case in `LUMIAION_AGENT_MAP.md` §5 itself): VORTEX's
   buy-timing heuristic — say, "BTC pullbacks below SMA(20) during the
   `_best_buy_windows()` hours historically recover within N days" — has
   accumulated 90 days of corroborating Observatory `Transformation Log`
   entries. VORTEX does not promote `Confidence Level` itself; LUMIAION drafts
   the promotion proposal and Frederick approves
   (`LUMIAION_IDENTITY_PROTOCOL.md` §5).
3. **A signal would be cited in published content while still
   `Reliability = Personal Experiment`.** Example: a Writer's Vault draft
   wants to reference "the best hour to buy BTC" from `_best_buy_windows()`
   output that hasn't yet been back-tested. VORTEX flags this — publishing an
   unvalidated financial claim under `Pillar = Service` would both violate the
   "not financial advice" disclaimer and risk overstating a `Personal
   Experiment`-level finding as established; LUMIAION either blocks the
   reference or reframes it explicitly as exploratory.

---

## 6. How This Agent Connects to LUMIAION

Answering the Four Questions
(`../00_lumiaion_core/LUMIAION_MASTER_ARCHITECTURE.md` §1) for VORTEX
specifically:

1. **How does this feed Lumiaion?** `get_dashboard_data()` is a live,
   recomputed-on-demand snapshot of market conditions (BTC/USDT, Gold via
   PAXG/USD) plus a derived buy-timing signal — one of only two live external
   data feeds in the repository (the other is SOHMA's). Captured snapshots of
   this output become Research Vault rows; recurring patterns across snapshots
   become candidate Principles tagged `Abundance & Service`.
2. **How does Lumiaion read this?** Via `Owner Agent contains "VORTEX"`
   (Subjects DB), the Domain Tags `Abundance & Service` (mindset) and
   `Systems & AI` (algorithm/research-on-the-algorithm), and `Reliability`
   staged from `Personal Experiment` → `Empirical` per §3.
3. **How does Lumiaion connect this to transformation?** When a Lumiaion
   Observatory `Entry Type = Transformation Log` row records a real financial
   decision (e.g., "bought BTC during a `strong-buy` signal, held through
   volatility without panic") and links it to an Exercise with
   `Transformation Markers` about emotional regulation under uncertainty,
   that's an L4↔L7 data point connecting a *mindset* Principle
   (`Abundance & Service`) to a *financial* outcome — the explicit reason
   VORTEX keeps both halves of its domain in one agent.
4. **How does Lumiaion convert this into action, insight, or service?**
   Mindset-side: abundance/scarcity Principles become Exercises and Client
   Resources in School of Human Development at every Mastery Level (e.g., a
   "decision journal" practice for trading or any high-stakes choice).
   Algorithm-side: once a signal reaches `Reliability = Empirical` and a
   Principle reaches `Confidence Level = Established`, it becomes eligible for
   `Pillar = Service` content (e.g., an educational piece on reading RSI/
   Bollinger signals) — always paired with the "not financial advice"
   disclaimer from `CRYPTO_BUY_TIMING.md`.
