import asyncio
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from database import init_db, upsert_weather, upsert_oil_prices
from pipeline import run_pipeline
from routers.news import router as news_router
from routers.oil import router as oil_router
from routers.weather import router as weather_router
from services.oil_service import fetch_all_prices
from services.openmeteo import fetch_weather

scheduler = AsyncIOScheduler()


async def refresh_weather():
    pins = await fetch_weather()
    if pins:
        await upsert_weather(pins)


async def refresh_oil():
    data = await fetch_all_prices()
    if data["wti"] or data["brent"]:
        await upsert_oil_prices(data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # News pipeline — run immediately, then every 15 min
    asyncio.create_task(run_pipeline())
    scheduler.add_job(run_pipeline, "interval", minutes=15)
    # Weather cache via Open-Meteo - run immediately, then every 30 min
    asyncio.create_task(refresh_weather())
    scheduler.add_job(refresh_weather, "interval", minutes=30)
    # Oil prices via EIA - run immediately, then every 4 hours
    asyncio.create_task(refresh_oil())
    scheduler.add_job(refresh_oil, "interval", hours=4)
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="ORBIS Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)
app.include_router(weather_router)
app.include_router(oil_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
