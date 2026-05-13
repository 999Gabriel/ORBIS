from fastapi import APIRouter, BackgroundTasks, Query
from database import get_news
from models import NewsPin
from pipeline import run_pipeline

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("", response_model=list[NewsPin])
async def list_news(limit: int = Query(default=100, le=500)):
    return await get_news(limit)


@router.post("/refresh")
async def refresh_news(background_tasks: BackgroundTasks):
    """Manually trigger a fetch+enrich cycle."""
    background_tasks.add_task(run_pipeline)
    return {"status": "refresh started"}
