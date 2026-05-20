from fastapi import APIRouter, Query
from database import get_weather, upsert_weather
from services.openmeteo import fetch_weather, search_weather

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("")
async def weather_pins():
    """Return cached weather pins. Frontend calls this when layer 05 is activated."""
    pins = await get_weather()
    if pins:
        return pins

    pins = await fetch_weather()
    if pins:
        await upsert_weather(pins)
    return pins


@router.post("/refresh")
async def weather_refresh():
    """Manually trigger a weather cache refresh (useful for development)."""
    pins = await fetch_weather()
    if pins:
        await upsert_weather(pins)
    return {"updated": len(pins)}


@router.get("/search")
async def weather_search(
    q: str = Query(min_length=2),
    limit: int = Query(default=8, ge=1, le=20),
    language: str = Query(default="en", min_length=2, max_length=2),
):
    """Search any city/place and return current weather for matching locations."""
    return await search_weather(q, limit=limit, language=language)
