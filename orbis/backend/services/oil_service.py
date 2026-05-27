import asyncio
import os
import time

import httpx

EIA_KEY = os.getenv("EIA_API_KEY", "")
EIA_BASE = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

_SERIES = {
    "WTI": "RWTC",
    "BRENT": "RBRTE",
}


async def _fetch_series(name: str, length: int = 60) -> list[dict]:
    """Fetch daily crude oil prices for one series from EIA Open Data API."""
    if not EIA_KEY:
        return []
    series_id = _SERIES.get(name.upper(), "")
    if not series_id:
        return []

    params = [
        ("api_key", EIA_KEY),
        ("frequency", "daily"),
        ("data[0]", "value"),
        ("facets[series][]", series_id),
        ("sort[0][column]", "period"),
        ("sort[0][direction]", "desc"),
        ("length", str(length)),
    ]

    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(EIA_BASE, params=params)
        r.raise_for_status()
        payload = r.json()

    rows = payload.get("response", {}).get("data", [])
    result = []
    for row in rows:
        val = row.get("value")
        if val is not None and val != "":
            try:
                result.append({"date": row["period"], "price": float(val)})
            except (ValueError, KeyError):
                pass
    return result


async def fetch_all_prices(length: int = 60) -> dict:
    """Fetch WTI and Brent concurrently. Returns {wti, brent, fetched_at}."""
    wti, brent = await asyncio.gather(
        _fetch_series("WTI", length),
        _fetch_series("BRENT", length),
    )
    return {"wti": wti, "brent": brent, "fetched_at": int(time.time())}
