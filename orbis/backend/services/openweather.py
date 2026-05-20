"""
Fetch current weather for major world cities via OpenWeatherMap /group endpoint.
Free tier: 1,000 calls/day — batching 20 cities per request keeps us well inside limits.
"""
import os
import time
import httpx

OWM_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OWM_GROUP = "https://api.openweathermap.org/data/2.5/group"

# ~60 major world cities — OpenWeatherMap city IDs
CITY_IDS = [
    2643743,  # London
    5128581,  # New York
    1850147,  # Tokyo
    2988507,  # Paris
    2950159,  # Berlin
    524901,   # Moscow
    2147714,  # Sydney
    292223,   # Dubai
    1880252,  # Singapore
    1275339,  # Mumbai
    1816670,  # Beijing
    3448439,  # São Paulo
    360630,   # Cairo
    745044,   # Istanbul
    2332459,  # Lagos
    3530597,  # Mexico City
    3435910,  # Buenos Aires
    6167865,  # Toronto
    5368361,  # Los Angeles
    4887398,  # Chicago
    1835848,  # Seoul
    1642911,  # Jakarta
    1609350,  # Bangkok
    1273294,  # Delhi
    1172451,  # Lahore
    2314302,  # Kinshasa
    3936456,  # Lima
    3688689,  # Bogotá
    184745,   # Nairobi
    993800,   # Johannesburg
    108410,   # Riyadh
    112931,   # Tehran
    1185241,  # Dhaka
    1853909,  # Osaka
    1701668,  # Manila
    1668341,  # Taipei
    1566083,  # Ho Chi Minh City
    1275004,  # Kolkata
    2553604,  # Casablanca
    379252,   # Khartoum
    2306104,  # Accra
    344979,   # Addis Ababa
    160263,   # Dar es Salaam
    2507480,  # Algiers
    2761369,  # Vienna
    3169070,  # Rome
    3117735,  # Madrid
    2759794,  # Amsterdam
    2673730,  # Stockholm
    756135,   # Warsaw
    3067696,  # Prague
    3054643,  # Budapest
    264371,   # Athens
    2267057,  # Lisbon
    658226,   # Helsinki
    2618425,  # Copenhagen
    2964574,  # Dublin
    2657896,  # Zurich
    3369157,  # Cape Town
    2158177,  # Melbourne
]


async def fetch_weather() -> list[dict]:
    if not OWM_KEY:
        print("[openweather] OPENWEATHER_API_KEY not set — skipping")
        return []

    results: list[dict] = []
    batch_size = 20
    now = int(time.time())

    async with httpx.AsyncClient(timeout=20) as client:
        for i in range(0, len(CITY_IDS), batch_size):
            batch = CITY_IDS[i : i + batch_size]
            try:
                resp = await client.get(
                    OWM_GROUP,
                    params={
                        "id": ",".join(str(x) for x in batch),
                        "appid": OWM_KEY,
                        "units": "metric",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as exc:
                print(f"[openweather] batch {i} failed: {exc}")
                continue

            for city in data.get("list", []):
                weather = city["weather"][0] if city.get("weather") else {}
                results.append({
                    "city_id":      city["id"],
                    "city":         city["name"],
                    "country":      city.get("sys", {}).get("country", ""),
                    "lat":          city["coord"]["lat"],
                    "lon":          city["coord"]["lon"],
                    "temp":         city["main"]["temp"],
                    "feels_like":   city["main"]["feels_like"],
                    "humidity":     city["main"]["humidity"],
                    "condition_id": weather.get("id", 800),
                    "condition":    weather.get("description", ""),
                    "icon":         weather.get("icon", "01d"),
                    "wind_speed":   city.get("wind", {}).get("speed", 0.0),
                    "wind_deg":     city.get("wind", {}).get("deg", 0),
                    "fetched_at":   now,
                })

    print(f"[openweather] fetched {len(results)} cities")
    return results
