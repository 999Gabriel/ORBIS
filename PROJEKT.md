# ORBIS — Live World Intelligence Dashboard

---

## Was ist ORBIS?

ORBIS ist ein interaktives Live-Intelligence-Dashboard, das weltweite Ereignisse, Nachrichten, Naturkatastrophen und Verkehrsdaten auf einem 3D-Globus visualisiert. Inspiriert von Bloomberg Terminal und modernen Geo-Intelligence-Plattformen verbindet ORBIS journalistische Nachrichtendaten mit Echtzeit-Layern (Flugverkehr, Erdbeben, Wetter) zu einem kohärenten Lagebild der Welt.

Die Seite beginnt minimalistisch — ein rotierender Globus im Dunkeln. Je mehr Layer und Inhalte der Nutzer aktiviert, desto mehr füllt sich das Interface mit Informationen. **Vom leeren Globus zum vollständigen Intelligence-Dashboard.**

---

## Projektziel

Schulprojekt im Fach Web-Programmierung (Vue.js) an der HTL Anichstraße, Innsbruck. Klasse 4BHWII — Wirtschaftsingenieurwesen und Informatik. Solo-Projekt, Zeitrahmen: ~2 Monate.

---

## Design & Stil

### Konzept
**"Frosted Glass über dem Universum"** — Das Interface schwebt über dem Globus wie ein Head-Up-Display in einem Cockpit. Panels sind halbtransparent, der Globus ist immer sichtbar dahinter. Alles fühlt sich an wie ein Tool das echte Analysten benutzen würden.

### Farbpalette

| Token | Farbe | Hex | Verwendung |
|---|---|---|---|
| `--bg-void` | Tiefschwarz | `#070A0F` | Hintergrund |
| `--bg-deep` | Nachtblau | `#0D1117` | Basis-Panels |
| `--surface` | Dunkelblau-grau | `#151C26` | Card-Hintergründe |
| `--glass` | Glassmorphism | `rgba(255,255,255,0.04)` | Frosted Panels |
| `--border` | Subtiler Rahmen | `rgba(255,255,255,0.08)` | Panel-Borders |
| `--gold` | Gold-Akzent | `#C9A84C` | Highlights, aktive States |
| `--gold-soft` | Gedämpftes Gold | `rgba(201,168,76,0.15)` | Hover-States |
| `--text-primary` | Reinweiß | `#F0F4F8` | Headlines |
| `--text-secondary` | Grau-blau | `#8896A8` | Subtext, Labels |
| `--red` | Kritisch | `#E05252` | Negative Sentiment, Krisen |
| `--green` | Positiv | `#52C97A` | Positive Sentiment |
| `--amber` | Neutral/Warnung | `#E09A3A` | Neutrale News |

### Typografie

| Rolle | Font | Quelle |
|---|---|---|
| Display / Headlines | `Instrument Serif` | Google Fonts |
| UI / Labels / Body | `DM Sans` | Google Fonts |
| Daten / Koordinaten / Codes | `JetBrains Mono` | Google Fonts / CDN |

`Instrument Serif` für Headlines gibt dem Dashboard eine journalistische, ernste Würde (ähnlich Financial Times). `DM Sans` für UI-Elemente bleibt modern und clean. `JetBrains Mono` für alle Datenpunkte (Koordinaten, Timestamps, Codes) gibt dem ganzen einen technischen, terminalhaften Unterton.

### UI-Prinzipien

- **Glassmorphism:** Alle Panels haben `backdrop-filter: blur(12px)` mit einem subtilen weißen Border (`rgba(255,255,255,0.08)`). Kein hartes Schwarz, kein Volldeckend.
- **Gold als einziger Akzent:** Gold wird sparsam eingesetzt — aktive Layer-Buttons, ausgewählte Pins, wichtige Zahlen. Nie als Hintergrundfarbe.
- **Progressive Disclosure:** Der Globus startet leer. Jeder aktivierte Layer fügt sichtbar Inhalt hinzu. Die Sidebar erscheint erst wenn ein Pin angeklickt wird.
- **Keine unnötige Dekoration:** Kein Neon-Glow, keine Scanlines, kein Hacker-Ästhetik. Clean, ernst, premium.
- **Spacing:** Großzügiges Padding in Panels. Dichte Daten werden durch klare Typografie-Hierarchie lesbar gemacht, nicht durch Trennlinien.

### Globus-Stil

- **Ozean:** Tiefdunkles Blau-Schwarz (`#0a1628`)
- **Kontinente:** Dunkelgrau mit subtiler Textur (`#1a2535`)
- **Atmosphäre:** Leichter blauer Glow am Rand (Atmosphären-Effekt via globe.gl)
- **Sterne im Hintergrund:** Statisches Sternfeld als CSS-Background oder via globe.gl Background
- **Pins:** Farbkodiert nach Sentiment (rot/amber/grün), goldener Ring bei aktivem Pin
- **Verbindungslinien:** Optionale Arcs zwischen verwandten News-Events (z.B. zwei Länder die im selben Artikel erwähnt werden)

---

## Features

### Phase 1 — Core (Wochen 1–4)
- [ ] 3D Globus mit globe.gl, rotierend, interaktiv
- [ ] News-Pins von GDELT API, farbkodiert nach Sentiment
- [ ] Location Extraction via Claude API (Artikel → Koordinaten)
- [ ] Klick auf Pin → Sidebar öffnet sich mit AI-Summary (3 Sätze) + Link
- [ ] Layer-Toggle Panel (ein/ausblenden)
- [ ] Basis-Filter: Zeitraum, Thema/Kategorie

### Phase 2 — Live Layers (Wochen 5–7)
- [ ] ✈️ Flugverkehr-Layer (OpenSky Network, live bewegende Punkte)
- [ ] 🌍 Erdbeben-Layer (USGS, Magnitude als Pin-Größe)
- [ ] 🔥 Waldbrand-Layer (NASA FIRMS)
- [ ] 🌦️ Sturm/Wetter-Events (OpenWeatherMap severe alerts)
- [ ] Zeitstrahl-Slider (News nach Datum filtern, animierte Pin-Erscheinung)

### Phase 3 — Intelligence Features (Woche 8, wenn Zeit)
- [ ] Layer-Korrelation: News-Pin aktiviert automatisch relevante Layer
- [ ] "Was passiert hier?" Button → Claude analysiert alle aktiven Layer in einer Region
- [ ] Heatmap-Modus: Dichte der Events als Farbgradient auf dem Globus

---

## Tech Stack

### Frontend

| Tool | Version | Zweck |
|---|---|---|
| Vue 3 | latest | Framework, Composition API |
| Vite | latest | Build Tool |
| Pinia | latest | State Management (Layer-Zustände, aktive News, Filter) |
| Vue Router | latest | Routing (falls mehrere Views nötig) |
| globe.gl | latest | 3D WebGL Globus (Three.js wrapper) |
| Chart.js + vue-chartjs | latest | Sparklines, Mini-Charts in Sidebar |
| date-fns | latest | Datum-Formatierung |

### Backend

| Tool | Version | Zweck |
|---|---|---|
| Python | 3.11+ | Sprache |
| FastAPI | latest | REST API Framework |
| SQLite + aiosqlite | latest | Lokale Datenpersistenz (gecachte News) |
| httpx | latest | Async HTTP Requests zu externen APIs |
| WebSockets | (via FastAPI) | Live Updates für Flugverkehr / Erdbeben |
| APScheduler | latest | Background Jobs (News alle 15min fetchen) |

### AI

| Tool | Zweck |
|---|---|
| Claude API (`claude-sonnet-4-20250514`) | Location Extraction aus Artikeltext, Sentiment-Analyse, AI-Summary, Layer-Korrelation |
| Prompt: Location Extraction | `"Extract the primary geographic location from this news article. Return only: { country, city, lat, lon }"` |
| Prompt: Sentiment | `"Classify the sentiment of this headline as: positive, neutral, negative. Return only one word."` |
| Prompt: Summary | `"Summarize this article in exactly 3 sentences for an intelligence analyst."` |

### Externe APIs & Datenquellen

| API | Daten | Kosten | Docs |
|---|---|---|---|
| **GDELT Project** | Weltweite News mit Geo-Tags | Kostenlos | gdeltproject.org |
| **OpenSky Network** | Live Flugverkehr (ADS-B) | Kostenlos | opensky-network.org |
| **USGS Earthquake API** | Echtzeit Erdbeben weltweit | Kostenlos | earthquake.usgs.gov |
| **NASA FIRMS** | Aktive Waldbrände (MODIS/VIIRS) | Kostenlos | firms.modaps.eosdis.nasa.gov |
| **OpenWeatherMap** | Wetter-Alerts, Stürme | Kostenlos (1000 req/day) | openweathermap.org/api |
| **OpenCage Geocoding** | Ortsname → Koordinaten | Kostenlos (2500 req/day) | opencagedata.com |
| ~~MarineTraffic~~ | ~~Schiffsverkehr~~ | ~~Teuer~~ | — |

> **Hinweis Schiffsverkehr:** MarineTraffic API ist kostenpflichtig und zu teuer für ein Schulprojekt. Als Alternative: AISHub (kostenlos, aber komplex). Wird als "geplantes Feature" dokumentiert, aber nicht implementiert.

---

## Projektstruktur (geplant)

```
orbis/
├── frontend/                  # Vue 3 App
│   ├── src/
│   │   ├── components/
│   │   │   ├── GlobeView.vue          # 3D Globus Hauptkomponente
│   │   │   ├── LayerPanel.vue         # Layer Toggle Buttons
│   │   │   ├── NewsSidebar.vue        # Artikel-Details, AI Summary
│   │   │   ├── TimelineSlider.vue     # Zeitstrahl
│   │   │   └── FilterBar.vue         # Themen-Filter
│   │   ├── stores/
│   │   │   ├── layers.js              # Aktive Layer (Pinia)
│   │   │   ├── news.js                # News-Daten (Pinia)
│   │   │   └── globe.js              # Globus-Zustand (Pinia)
│   │   ├── composables/
│   │   │   ├── useGlobe.js            # globe.gl Logik
│   │   │   └── useWebSocket.js       # Live Data Connection
│   │   └── App.vue
│   └── index.html
│
├── backend/                   # FastAPI
│   ├── main.py
│   ├── routers/
│   │   ├── news.py            # /api/news
│   │   ├── flights.py         # /api/flights
│   │   ├── earthquakes.py     # /api/earthquakes
│   │   ├── fires.py           # /api/fires
│   │   └── ai.py              # /api/ai/summary, /api/ai/correlate
│   ├── services/
│   │   ├── gdelt.py           # GDELT Fetcher
│   │   ├── opensky.py         # OpenSky Fetcher
│   │   ├── usgs.py            # USGS Fetcher
│   │   └── claude.py          # Claude API Wrapper
│   ├── models.py              # Pydantic Models
│   ├── database.py            # SQLite Setup
│   └── scheduler.py           # Background Jobs
│
├── PROJEKT.md                 # Diese Datei
└── README.md
```

---

## Entwicklungs-Roadmap

| Woche | Ziel |
|---|---|
| 1 | Projektsetup, Vue + FastAPI boilerplate, globe.gl Globus läuft |
| 2 | GDELT API angebunden, erste News-Pins auf dem Globus |
| 3 | Claude API: Location Extraction + Sentiment funktioniert |
| 4 | Sidebar mit AI-Summary, Layer-Toggle, Filter — **Phase 1 fertig** |
| 5 | OpenSky Flugverkehr-Layer + WebSocket Live Updates |
| 6 | USGS Erdbeben + NASA FIRMS Waldbrand-Layer |
| 7 | Zeitstrahl-Slider, Wetter-Alerts, UI Polish |
| 8 | Layer-Korrelation (Claude), Testing, Dokumentation, Präsentation |

---

## Namensgebung

**ORBIS** — Lateinisch für "Welt" / "Erdkreis". Kurz, einprägsam, klingt nach einem echten Produkt. Passt zum eleganten, professionellen Stil.

Tagline: *"The world, at a glance."*
