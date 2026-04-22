# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Greenfield. The only file is [PROJEKT.md](PROJEKT.md) — the full specification (German). No frontend or backend has been scaffolded yet. **Read PROJEKT.md before making any architectural decision**; it is the source of truth for scope, stack, design tokens, and roadmap.

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

No build/test/lint commands exist yet — nothing is scaffolded. When setting up:

- Prefer `npm create vue@latest` (Vite + Pinia + Vue Router) in `frontend/`, and `uv` or `pip` with a `pyproject.toml` / `requirements.txt` in `backend/`.
- Ask before adding frameworks not listed in PROJEKT.md §Tech Stack (e.g. don't introduce Nuxt, Next, Django, Postgres). The stack is part of the school assignment.

## Working directory note

The parent folder `SWP-Web/` contains unrelated school exercises (PowerGuard, Mitschriften, etc.) with heavy `git status` noise — ignore changes outside this `news globe project/` directory unless explicitly asked.
