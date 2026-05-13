"""
Fetch → Enrich → Store pipeline. Called at startup and every 15 min by APScheduler.
"""
import asyncio
import hashlib
import math
import os
import time

from database import count_news, upsert_article, url_exists
from services.gdelt import fetch_articles
from services.geo_fallback import lookup, COUNTRY_GEO

CONCURRENCY = 4
USE_CLAUDE = bool(os.environ.get("ANTHROPIC_API_KEY", "").startswith("sk-"))
_pipeline_lock = asyncio.Lock()  # prevent concurrent pipeline runs

# Build a title-keyword → geo lookup from known countries
_TITLE_KEYWORDS: list[tuple[str, tuple]] = []
for _code, _geo in COUNTRY_GEO.items():
    _lat, _lon, _country, _city = _geo
    # Add country name and capital city as keywords
    _TITLE_KEYWORDS.append((_country.lower(), _geo))
    if _city and _city != "Unknown":
        _TITLE_KEYWORDS.append((_city.lower(), _geo))
# Sort longest first so "United States" matches before "States"
_TITLE_KEYWORDS.sort(key=lambda x: -len(x[0]))


def _extract_geo_from_title(title: str) -> tuple | None:
    """Scan title for known country/city names."""
    lower = title.lower()
    for keyword, geo in _TITLE_KEYWORDS:
        if keyword in lower:
            return geo
    return None


def _jitter(lat: float, lon: float, url: str) -> tuple[float, float]:
    """Apply deterministic ±1.2° offset based on URL hash so same article never moves."""
    h = int(hashlib.md5(url.encode()).hexdigest()[:8], 16)
    dlat = ((h % 1000) / 1000 - 0.5) * 2.4  # range ±1.2
    dlon = (((h >> 10) % 1000) / 1000 - 0.5) * 2.4
    return round(lat + dlat, 4), round(lon + dlon, 4)


async def _enrich_with_claude(title: str) -> dict | None:
    from services.claude_service import enrich_article
    return await enrich_article(title)


def _enrich_fallback(art: dict) -> dict | None:
    """Best-effort enrichment from metadata + title keywords."""
    # 1. Try sourcecountry lookup
    geo = lookup(art.get("source_country", ""))

    # 2. If not found, scan the title
    if geo[0] == 0.0 and geo[1] == 0.0:
        geo = _extract_geo_from_title(art["title"]) or geo

    if geo[0] == 0.0 and geo[1] == 0.0:
        return None  # No location found — skip

    lat, lon, country, city = geo
    lat, lon = _jitter(lat, lon, art["url"])

    return {
        "country": country,
        "city": city,
        "lat": lat,
        "lon": lon,
        "sentiment": "neutral",
        "category": art.get("gdelt_category", "politics"),
        "summary": [
            art["title"],
            f"Source: {art.get('domain', 'international media')}.",
            "Add an Anthropic API key to backend/.env for AI-generated summaries.",
        ],
    }


async def run_pipeline():
    if _pipeline_lock.locked():
        print("[pipeline] already running, skipping")
        return
    async with _pipeline_lock:
        await _run_pipeline()


async def _run_pipeline():
    print("[pipeline] starting fetch…")
    raw_articles = await fetch_articles(max_per_query=15)
    print(f"[pipeline] GDELT returned {len(raw_articles)} articles")

    new_articles = [a for a in raw_articles if not await url_exists(a["url"])]
    print(f"[pipeline] {len(new_articles)} new (mode: {'claude' if USE_CLAUDE else 'fallback'})")
    if not new_articles:
        return

    sem = asyncio.Semaphore(CONCURRENCY)
    enriched = 0

    async def process(art: dict):
        nonlocal enriched
        async with sem:
            if USE_CLAUDE:
                result = await _enrich_with_claude(art["title"])
                if result is None:
                    result = _enrich_fallback(art)
            else:
                result = _enrich_fallback(art)

            if result is None:
                return

            await upsert_article({
                "title": art["title"],
                "url": art["url"],
                "domain": art.get("domain", ""),
                "country": result["country"],
                "city": result["city"],
                "lat": result["lat"],
                "lon": result["lon"],
                "sentiment": result["sentiment"],
                "category": result["category"],
                "summary": result["summary"],
                "timestamp": art["timestamp"],
                "created_at": int(time.time() * 1000),
            })
            enriched += 1

    await asyncio.gather(*[process(a) for a in new_articles])
    total = await count_news()
    print(f"[pipeline] done — added {enriched}, total in DB: {total}")
