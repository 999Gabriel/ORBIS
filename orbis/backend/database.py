import aiosqlite
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "orbis.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS news (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    url       TEXT    NOT NULL UNIQUE,
    domain    TEXT,
    country   TEXT,
    city      TEXT,
    lat       REAL,
    lon       REAL,
    sentiment TEXT    CHECK(sentiment IN ('positive','neutral','negative')),
    category  TEXT,
    summary   TEXT,   -- JSON array of 3 strings
    timestamp INTEGER NOT NULL,
    created_at INTEGER NOT NULL
)
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE)
        await db.commit()


async def upsert_article(article: dict):
    """Insert or ignore (deduplicate by url)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO news
                (title, url, domain, country, city, lat, lon, sentiment, category, summary, timestamp, created_at)
            VALUES
                (:title, :url, :domain, :country, :city, :lat, :lon, :sentiment, :category, :summary, :timestamp, :created_at)
            """,
            {**article, "summary": json.dumps(article["summary"])},
        )
        await db.commit()


async def get_news(limit: int = 100) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM news ORDER BY timestamp DESC LIMIT ?", (limit,)
        ) as cur:
            rows = await cur.fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["summary"] = json.loads(d["summary"]) if d["summary"] else []
        result.append(d)
    return result


async def url_exists(url: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM news WHERE url = ?", (url,)) as cur:
            return await cur.fetchone() is not None


async def count_news() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM news") as cur:
            row = await cur.fetchone()
            return row[0] if row else 0
