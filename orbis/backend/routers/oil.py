from fastapi import APIRouter
from database import get_oil_prices, upsert_oil_prices
from services.oil_service import fetch_all_prices

router = APIRouter(prefix="/api/oil", tags=["oil"])


@router.get("/prices")
async def oil_prices():
    """Return oil price history (WTI + Brent, ~60 days).
    Serves from SQLite cache; falls back to live EIA fetch if cache is stale."""
    cached = await get_oil_prices()
    if cached is not None:
        return cached

    fresh = await fetch_all_prices()
    if fresh["wti"] or fresh["brent"]:
        await upsert_oil_prices(fresh)
    return fresh
