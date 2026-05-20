from fastapi import APIRouter
from database import get_weather, upsert_weather
from services.openmeteo import fetch_weather

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
