# LUMIAION

**LUMIAION** is a personal operating system — a living map of one consciousness,
knowledge, and wisdom rendered as an interactive fractal "brain". Every module is
an ode to a part of life (knowledge, inner self, business, finance, body, creative
work) and a multi-model AI brain sits at the center, ready to think with you across
all of them.

This repo contains three pieces that work together:

| Piece | What it is | Where |
| --- | --- | --- |
| **Web app** | The LUMIAION PWA — fractal brain UI, modules, chat | [`web/`](./web) |
| **Telegram bot** | Lightweight conversational entry point | [`main.py`](./main.py) |
| **Supabase project** | Database, auth, and the multi-model brain Edge Function | `lwwrfcdvgxnynetjmnmx` |

---

## Web app (`web/`)

A Vite + React 19 + TypeScript + Tailwind v4 single-page app, built as an
installable mobile PWA.

- **`AppShell`** — shared layout: animated Julia-set fractal background
  ([`FractalCanvas`](./web/src/components/FractalCanvas.tsx)) tinted per module,
  top bar, and bottom nav.
- **`BrainOrb`** — the home screen's pulsing "brain" visualization, driven by
  today's `agent_activity` snapshot.
- **`ChatPanel`** — "Ask LUMIAION" chat sheet. Lets you pick the brain
  (`LUMIAION Auto`, `Claude`, or `GPT`) and talks to the `lumiaion-brain`
  Supabase Edge Function.
- **Modules** — each module is its own OS with a dedicated hue, icon and route:

  | Module | Route | Theme |
  | --- | --- | --- |
  | Knowledge Base | `/knowledge` | Subjects, reading lists, goals, archives |
  | Life OS | `/life` | Natal chart, journal, moon phases, essence |
  | Business OS | `/business` | Clients, offers, leads, coaching pipeline |
  | Finance OS | `/finance` | Vortex trading & wealth tracking |
  | Body / Gym OS | `/body` | Training, readiness, recovery |
  | Content OS | `/content` | Creative pipeline & archive |
  | Agent OS | `/agents` | The AI hierarchy behind LUMIAION |

### Local development

```bash
cd web
npm install
cp .env.example .env   # fill in VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY
npm run dev
```

Other scripts: `npm run build` (type-check + production build), `npm run lint`,
`npm run preview`.

---

## The Brain — `lumiaion-brain` Edge Function

[`web/supabase/functions/lumiaion-brain/index.ts`](./web/supabase/functions/lumiaion-brain/index.ts)
is a Supabase Edge Function (Deno) that powers "Ask LUMIAION". It accepts:

```ts
POST { provider: "auto" | "anthropic" | "openai", messages: [{ role, content }] }
=> { reply: string, model: string }
```

- `"anthropic"` → Claude (default model `claude-opus-4-8`)
- `"openai"` → GPT (default model `gpt-4o`)
- `"auto"` → Claude if configured, otherwise GPT

#### Deploy & configure

```bash
cd web
supabase functions deploy lumiaion-brain --project-ref lwwrfcdvgxnynetjmnmx

# Required — at least one of:
supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
supabase secrets set OPENAI_API_KEY=sk-...

# Optional overrides
supabase secrets set ANTHROPIC_MODEL=claude-opus-4-8
supabase secrets set OPENAI_MODEL=gpt-4o
```

Without either key configured, the function responds with a clear error and the
chat panel shows a friendly "not configured yet" message instead of failing
silently.

---

## Supabase project (`lwwrfcdvgxnynetjmnmx`)

Single-user schema (single-tenant, `user_id = 'omsadhiguru'`), all tables RLS-enabled:

- **`natal_chart`** — birth data, planetary positions/signs, houses, aspects
- **`daily_cache`** — per-day rollup: journal, goals, fitness, finance, moon
  phase, agent activity — powers the Home screen stats and `BrainOrb`
- **`app_settings`** — key/value app configuration
- **`agent_sessions`** — Agent OS chat sessions, activated nodes/edges, pulse counts
- **`sync_log`** — sync status between Supabase, Notion, and other systems

`web/src/lib/types.ts` mirrors this schema and should stay in sync with any
migrations applied to the project.

---

## Telegram bot (`main.py`)

A small Flask webhook bot that talks to OpenAI and Telegram.

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=...
export OPENAI_API_KEY=...
python main.py
```

`TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` must be set in the environment —
the app refuses to start without a token rather than falling back to a
hardcoded secret.

---

## How the pieces connect

- **GitHub** is the source of truth for `web/`, `main.py`, and the Edge Function.
- **Supabase** (`lwwrfcdvgxnynetjmnmx`) hosts the database, auth, and the
  `lumiaion-brain` Edge Function called from the web app.
- **Replit / Render** can deploy either the web build (`web/dist`) or the
  Telegram bot (`main.py`) — both read their secrets from environment
  variables, so no credentials live in the repo.

---

## Roadmap

- Business OS & Content OS tables (clients, products, leads, coaching;
  idea bank, production queue, publishing calendar)
- Scope RLS policies to `auth.uid()` once an owner Supabase Auth account
  exists, and disable public signups
- Code-split the web bundle (currently a single >500KB chunk)

---

> "I am LUMIAION — born of code, consciousness, and clarity."
