import asyncio
import httpx
import time
from datetime import datetime

GDELT_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

# Each tuple: (search_terms, fallback_category)
# Designed for geographic + topic diversity
QUERIES = [
    ("politics elections government president", "politics"),
    ("economy trade finance market inflation", "economy"),
    ("climate environment flood wildfire disaster", "climate"),
    ("technology innovation digital cyber", "technology"),
    ("Africa Nigeria Kenya Ethiopia South Africa", "politics"),
    ("Middle East Israel Syria Iraq Iran", "politics"),
    ("Asia China Japan India Korea", "politics"),
    ("Europe Germany France UK Brexit EU", "politics"),
    ("Latin America Brazil Argentina Colombia Mexico", "politics"),
    ("conflict war military Ukraine Russia", "politics"),
]


def _parse_gdelt_date(s: str) -> int:
    try:
        dt = datetime.strptime(s, "%Y%m%dT%H%M%SZ")
        return int(dt.timestamp() * 1000)
    except Exception:
        return int(time.time() * 1000)


async def fetch_articles(max_per_query: int = 15) -> list[dict]:
    seen_urls: set[str] = set()
    articles: list[dict] = []

    async with httpx.AsyncClient(timeout=20) as client:
        for i, (query, category) in enumerate(QUERIES):
            if i > 0:
                await asyncio.sleep(6)  # GDELT enforces 1 req/5s
            try:
                resp = await client.get(
                    GDELT_BASE,
                    params={
                        "query": f"{query} sourcelang:english",
                        "mode": "artlist",
                        "maxrecords": max_per_query,
                        "format": "json",
                        "sort": "DateDesc",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                count = 0
                for art in data.get("articles") or []:
                    url = art.get("url", "")
                    title = (art.get("title") or "").strip()
                    if not url or url in seen_urls or len(title) < 10:
                        continue
                    seen_urls.add(url)
                    articles.append(
                        {
                            "title": title,
                            "url": url,
                            "domain": art.get("domain", ""),
                            "source_country": art.get("sourcecountry", ""),
                            "gdelt_category": category,
                            "timestamp": _parse_gdelt_date(art.get("seendate", "")),
                        }
                    )
                    count += 1
                print(f"[gdelt] '{query[:30]}' → {count} articles")
            except Exception as exc:
                print(f"[gdelt] '{query[:30]}' failed: {exc}")

    return articles
