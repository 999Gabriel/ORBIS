import json
import os
import anthropic

_client: anthropic.AsyncAnthropic | None = None

SYSTEM_PROMPT = """You are a geographic intelligence analyst. For each news headline I give you, return a JSON object with these exact fields:
- country: primary country this article is about (full English name)
- city: primary city (use capital if no specific city mentioned)
- lat: latitude as number (e.g. 48.8566)
- lon: longitude as number (e.g. 2.3522)
- sentiment: exactly one of "positive", "neutral", "negative"
- category: exactly one of "politics", "economy", "technology", "climate", "culture", "infrastructure"
- summary: array of exactly 3 complete sentences summarizing the article for an intelligence analyst

Return ONLY valid JSON. No markdown, no explanation."""


def get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


async def enrich_article(title: str) -> dict | None:
    """Call Claude once and get location + sentiment + category + summary."""
    try:
        msg = await get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f'Headline: "{title}"'}],
        )
        raw = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)
        # Validate required fields
        required = {"country", "city", "lat", "lon", "sentiment", "category", "summary"}
        if not required.issubset(data.keys()):
            return None
        if not isinstance(data["summary"], list) or len(data["summary"]) != 3:
            return None
        if data["sentiment"] not in ("positive", "neutral", "negative"):
            return None
        return data
    except Exception as exc:
        print(f"[claude] enrichment failed for '{title[:60]}': {exc}")
        return None
