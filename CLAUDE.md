# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Frontend scaffolded and running. Backend not yet started.

- `orbis/frontend/` — Vue 3 + Vite + Pinia app is live (`npm run dev` in that directory).
- Components written so far: `App.vue`, `GlobeView.vue`, `NavBar.vue`, `FilterBar.vue`, `NewsSidebar.vue`, `TimelineSlider.vue`. `LayerPanel.vue` was deleted (merged into NavBar).
- Globe renders via `globe.gl` using `useGlobe.js` composable.
- **Read PROJEKT.md before making any architectural decision**; it is the source of truth for scope, stack, design tokens, and roadmap.

## Context

- **ORBIS** — a live-intelligence dashboard: 3D globe with news pins (GDELT), live layers (flights/earthquakes/fires/weather), and Claude-powered location extraction, sentiment, and summaries.
- **Solo school project** for HTL Anichstraße, class 4BHWII (Web-Programmierung / Vue.js), ~2 months. Scope decisions should favor finishing Phase 1 (PROJEKT.md §Features) over breadth.
- Target look: "frosted glass over the universe" — glassmorphism panels floating over a dark globe. No neon, no hacker aesthetic. See PROJEKT.md §Design for the exact token values — do not invent colors.

## Planned architecture

Two-service layout (see PROJEKT.md §Projektstruktur for full tree):

- `frontend/` — **Vue 3 + Vite + Pinia**, `globe.gl` for the WebGL globe, Chart.js for sparklines. Pinia stores split by domain: `layers`, `news`, `globe`. Globe logic lives in a `useGlobe` composable; WebSocket live data in `useWebSocket`.
- `backend/` — **FastAPI + SQLite (aiosqlite) + httpx + APScheduler**. Routers per data source (`news`, `flights`, `earthquakes`, `fires`, `ai`); services wrap each external API (GDELT, OpenSky, USGS, NASA FIRMS, OpenWeatherMap, Claude). WebSockets for live flight/earthquake streams. APScheduler refreshes news every ~15 min into the SQLite cache.

Design principle: **the backend is a caching proxy + AI pipeline**, not a thin pass-through. Frontend should never call external APIs directly — always go through `backend/routers/*`. This keeps API keys server-side and lets the SQLite cache absorb rate limits (OpenWeatherMap 1000/day, OpenCage 2500/day).

## Claude API usage

Model: `claude-sonnet-4-20250514` (per PROJEKT.md) — keep this pinned unless the user asks to upgrade. Three distinct prompts (location extraction, sentiment, 3-sentence summary) live in `backend/services/claude.py`. Prompts are specified verbatim in PROJEKT.md §AI — match them exactly when implementing, since the spec depends on the structured output shape (e.g. `{ country, city, lat, lon }` JSON for location extraction).

## Data sources — constraints to remember

- **MarineTraffic / ship traffic is out of scope** (too expensive). Documented as "planned", not implemented. Don't add it.
- Free-tier rate limits (OpenWeatherMap, OpenCage) make the SQLite cache non-optional — always cache before serving.
- GDELT is the primary news source; do not swap it for a paid alternative without asking.

## Commands

```bash
cd orbis/frontend && npm run dev     # start Vite dev server on :5173
```

**IMPORTANT — PATH bug:** The parent directory `4BHWII:2025-26` contains a colon, which is the Unix PATH separator. This breaks npm's automatic `node_modules/.bin` injection, so `vite` (and any other local binary) is not found when running scripts. All scripts in `orbis/frontend/package.json` must use `./node_modules/.bin/<binary>` explicitly — never bare binary names like `vite`.

**globe.gl / Vite fix:** `globe.gl` must be listed in `optimizeDeps.include` (not `exclude`) in `vite.config.js`, together with `three-globe` and `frame-ticker`. This lets Vite pre-bundle the chain and convert the CJS `frame-ticker` module to ESM — without this, the globe fails with `SyntaxError: does not provide an export named 'default'`.

Backend: `uv` or `pip` with `pyproject.toml` / `requirements.txt` in `backend/` (not yet scaffolded). Ask before adding frameworks not listed in PROJEKT.md §Tech Stack.

## Working directory note

The parent folder `SWP-Web/` contains unrelated school exercises (PowerGuard, Mitschriften, etc.) with heavy `git status` noise — ignore changes outside this `news globe project/` directory unless explicitly asked.

## Current design — tokens & layout (as of 2026-04-29)

Design language: **"frosted glass over the universe"** — glassmorphism panels on a `#0A0A0B` dark canvas. No neon, no hacker aesthetic.

Key design tokens (see `orbis/frontend/src/assets/styles/tokens.css` for full list):
- Canvas: `--canvas: #0A0A0B`, `--canvas-soft: #111113`
- Surfaces: `rgba(255,255,255,0.035)` / hover `0.07`
- Ink: `--ink: #FAFAF7`, muted `0.58`, whisper `0.32`
- Accents: `--navy: #6B89C4`, `--beige: #DFD2BC`, `--alert: #F3C843`
- Sentiment: `--positive: #A3D9B1`, `--neutral: #DFD2BC`, `--negative: #E8A5A5`
- Font: DM Sans
- 8pt spacing grid (`--space-1` → `--space-16`)
- Z-layers: globe=0, panel=10, sidebar=20, nav=30, modal=40
- Layout dims: `--nav-height: 64px`, `--subnav-height: 44px`, `--timeline-height: 64px`, `--sidebar-width: 400px`

UI components live:
- **NavBar** — fixed top, `ORBIS` brand + pulsing live dot, layer pill-buttons in center, EN/DE switcher right
- **FilterBar** (subnav) — appears below NavBar when `news` layer active; category filter tabs (all/politics/economy/…)
- **GlobeView** — full-screen WebGL globe, `globe.gl`, auto-rotates, pauses on drag
- **NewsSidebar** — slides in from right when a pin is selected
- **TimelineSlider** — fixed at bottom

## Updates

Next up: backend scaffolding (FastAPI). Frontend phase 1 components are all written.
