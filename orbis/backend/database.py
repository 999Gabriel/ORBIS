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
        await db.execute(CREATE_WEATHER_TABLE)
        await db.execute(CREATE_OIL_TABLE)
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


# ── Weather cache ─────────────────────────────────────────────────────────────

CREATE_WEATHER_TABLE = """
CREATE TABLE IF NOT EXISTS weather_cache (
    city_id      INTEGER PRIMARY KEY,
    city         TEXT    NOT NULL,
    country      TEXT,
    lat          REAL,
    lon          REAL,
    temp         REAL,
    feels_like   REAL,
    humidity     INTEGER,
    condition_id INTEGER,
    condition    TEXT,
    icon         TEXT,
    wind_speed   REAL,
    wind_deg     INTEGER,
    fetched_at   INTEGER NOT NULL
)
"""


async def upsert_weather(pins: list[dict]) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(
            """
            INSERT OR REPLACE INTO weather_cache
                (city_id, city, country, lat, lon, temp, feels_like, humidity,
                 condition_id, condition, icon, wind_speed, wind_deg, fetched_at)
            VALUES
                (:city_id, :city, :country, :lat, :lon, :temp, :feels_like, :humidity,
                 :condition_id, :condition, :icon, :wind_speed, :wind_deg, :fetched_at)
            """,
            pins,
        )
        await db.commit()


async def get_weather() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM weather_cache ORDER BY city") as cur:
            rows = await cur.fetchall()
    return [dict(r) for r in rows]


# ── Oil price cache ───────────────────────────────────────────────────────────

CREATE_OIL_TABLE = """
CREATE TABLE IF NOT EXISTS oil_cache (
    id         INTEGER PRIMARY KEY,
    data       TEXT    NOT NULL,
    fetched_at INTEGER NOT NULL
)
"""

OIL_TTL_SECONDS = 4 * 3600  # refresh at most every 4 hours


async def upsert_oil_prices(payload: dict) -> None:
    import time as _time
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM oil_cache")
        await db.execute(
            "INSERT INTO oil_cache (data, fetched_at) VALUES (?, ?)",
            (json.dumps(payload), int(_time.time())),
        )
        await db.commit()


async def get_oil_prices() -> dict | None:
    """Return cached oil prices if they are fresh, otherwise None."""
    import time as _time
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT data, fetched_at FROM oil_cache LIMIT 1") as cur:
            row = await cur.fetchone()
    if not row:
        return None
    if _time.time() - row["fetched_at"] > OIL_TTL_SECONDS:
        return None
    return json.loads(row["data"])
