import asyncio
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from database import init_db
from pipeline import run_pipeline
from routers.news import router as news_router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Run initial pipeline in background so server starts immediately
    asyncio.create_task(run_pipeline())
    # Refresh every 15 minutes
    scheduler.add_job(run_pipeline, "interval", minutes=15)
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


@app.get("/health")
async def health():
    return {"status": "ok"}
