from pydantic import BaseModel


class NewsPin(BaseModel):
    id: int
    lat: float
    lon: float
    title: str
    sentiment: str
    country: str
    city: str
    category: str
    summary: list[str]
    url: str
    timestamp: int  # ms since epoch (matches Date.now() on frontend)
    domain: str | None = None
