"""
Fetch current weather for major world cities via Open-Meteo.

Open-Meteo does not require an API key. This module keeps the same response
shape the frontend already expects from the old OpenWeatherMap integration.
"""
import time

import httpx

OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"

# Stable city ids preserve the existing weather_cache primary keys.
CITIES = [
    {"city_id": 2643743, "city": "London", "country": "GB", "lat": 51.5074, "lon": -0.1278},
    {"city_id": 5128581, "city": "New York", "country": "US", "lat": 40.7128, "lon": -74.0060},
    {"city_id": 1850147, "city": "Tokyo", "country": "JP", "lat": 35.6762, "lon": 139.6503},
    {"city_id": 2988507, "city": "Paris", "country": "FR", "lat": 48.8566, "lon": 2.3522},
    {"city_id": 2950159, "city": "Berlin", "country": "DE", "lat": 52.5200, "lon": 13.4050},
    {"city_id": 524901, "city": "Moscow", "country": "RU", "lat": 55.7558, "lon": 37.6173},
    {"city_id": 2147714, "city": "Sydney", "country": "AU", "lat": -33.8688, "lon": 151.2093},
    {"city_id": 292223, "city": "Dubai", "country": "AE", "lat": 25.2048, "lon": 55.2708},
    {"city_id": 1880252, "city": "Singapore", "country": "SG", "lat": 1.3521, "lon": 103.8198},
    {"city_id": 1275339, "city": "Mumbai", "country": "IN", "lat": 19.0760, "lon": 72.8777},
    {"city_id": 1816670, "city": "Beijing", "country": "CN", "lat": 39.9042, "lon": 116.4074},
    {"city_id": 3448439, "city": "Sao Paulo", "country": "BR", "lat": -23.5558, "lon": -46.6396},
    {"city_id": 360630, "city": "Cairo", "country": "EG", "lat": 30.0444, "lon": 31.2357},
    {"city_id": 745044, "city": "Istanbul", "country": "TR", "lat": 41.0082, "lon": 28.9784},
    {"city_id": 2332459, "city": "Lagos", "country": "NG", "lat": 6.5244, "lon": 3.3792},
    {"city_id": 3530597, "city": "Mexico City", "country": "MX", "lat": 19.4326, "lon": -99.1332},
    {"city_id": 3435910, "city": "Buenos Aires", "country": "AR", "lat": -34.6037, "lon": -58.3816},
    {"city_id": 6167865, "city": "Toronto", "country": "CA", "lat": 43.6532, "lon": -79.3832},
    {"city_id": 5368361, "city": "Los Angeles", "country": "US", "lat": 34.0522, "lon": -118.2437},
    {"city_id": 4887398, "city": "Chicago", "country": "US", "lat": 41.8781, "lon": -87.6298},
    {"city_id": 1835848, "city": "Seoul", "country": "KR", "lat": 37.5665, "lon": 126.9780},
    {"city_id": 1642911, "city": "Jakarta", "country": "ID", "lat": -6.2088, "lon": 106.8456},
    {"city_id": 1609350, "city": "Bangkok", "country": "TH", "lat": 13.7563, "lon": 100.5018},
    {"city_id": 1273294, "city": "Delhi", "country": "IN", "lat": 28.6139, "lon": 77.2090},
    {"city_id": 1172451, "city": "Lahore", "country": "PK", "lat": 31.5204, "lon": 74.3587},
    {"city_id": 2314302, "city": "Kinshasa", "country": "CD", "lat": -4.4419, "lon": 15.2663},
    {"city_id": 3936456, "city": "Lima", "country": "PE", "lat": -12.0464, "lon": -77.0428},
    {"city_id": 3688689, "city": "Bogota", "country": "CO", "lat": 4.7110, "lon": -74.0721},
    {"city_id": 184745, "city": "Nairobi", "country": "KE", "lat": -1.2921, "lon": 36.8219},
    {"city_id": 993800, "city": "Johannesburg", "country": "ZA", "lat": -26.2041, "lon": 28.0473},
    {"city_id": 108410, "city": "Riyadh", "country": "SA", "lat": 24.7136, "lon": 46.6753},
    {"city_id": 112931, "city": "Tehran", "country": "IR", "lat": 35.6892, "lon": 51.3890},
    {"city_id": 1185241, "city": "Dhaka", "country": "BD", "lat": 23.8103, "lon": 90.4125},
    {"city_id": 1853909, "city": "Osaka", "country": "JP", "lat": 34.6937, "lon": 135.5023},
    {"city_id": 1701668, "city": "Manila", "country": "PH", "lat": 14.5995, "lon": 120.9842},
    {"city_id": 1668341, "city": "Taipei", "country": "TW", "lat": 25.0330, "lon": 121.5654},
    {"city_id": 1566083, "city": "Ho Chi Minh City", "country": "VN", "lat": 10.8231, "lon": 106.6297},
    {"city_id": 1275004, "city": "Kolkata", "country": "IN", "lat": 22.5726, "lon": 88.3639},
    {"city_id": 2553604, "city": "Casablanca", "country": "MA", "lat": 33.5731, "lon": -7.5898},
    {"city_id": 379252, "city": "Khartoum", "country": "SD", "lat": 15.5007, "lon": 32.5599},
    {"city_id": 2306104, "city": "Accra", "country": "GH", "lat": 5.6037, "lon": -0.1870},
    {"city_id": 344979, "city": "Addis Ababa", "country": "ET", "lat": 8.9806, "lon": 38.7578},
    {"city_id": 160263, "city": "Dar es Salaam", "country": "TZ", "lat": -6.7924, "lon": 39.2083},
    {"city_id": 2507480, "city": "Algiers", "country": "DZ", "lat": 36.7538, "lon": 3.0588},
    {"city_id": 2761369, "city": "Vienna", "country": "AT", "lat": 48.2082, "lon": 16.3738},
    {"city_id": 3169070, "city": "Rome", "country": "IT", "lat": 41.9028, "lon": 12.4964},
    {"city_id": 3117735, "city": "Madrid", "country": "ES", "lat": 40.4168, "lon": -3.7038},
    {"city_id": 2759794, "city": "Amsterdam", "country": "NL", "lat": 52.3676, "lon": 4.9041},
    {"city_id": 2673730, "city": "Stockholm", "country": "SE", "lat": 59.3293, "lon": 18.0686},
    {"city_id": 756135, "city": "Warsaw", "country": "PL", "lat": 52.2297, "lon": 21.0122},
    {"city_id": 3067696, "city": "Prague", "country": "CZ", "lat": 50.0755, "lon": 14.4378},
    {"city_id": 3054643, "city": "Budapest", "country": "HU", "lat": 47.4979, "lon": 19.0402},
    {"city_id": 264371, "city": "Athens", "country": "GR", "lat": 37.9838, "lon": 23.7275},
    {"city_id": 2267057, "city": "Lisbon", "country": "PT", "lat": 38.7223, "lon": -9.1393},
    {"city_id": 658226, "city": "Helsinki", "country": "FI", "lat": 60.1699, "lon": 24.9384},
    {"city_id": 2618425, "city": "Copenhagen", "country": "DK", "lat": 55.6761, "lon": 12.5683},
    {"city_id": 2964574, "city": "Dublin", "country": "IE", "lat": 53.3498, "lon": -6.2603},
    {"city_id": 2657896, "city": "Zurich", "country": "CH", "lat": 47.3769, "lon": 8.5417},
    {"city_id": 3369157, "city": "Cape Town", "country": "ZA", "lat": -33.9249, "lon": 18.4241},
    {"city_id": 2158177, "city": "Melbourne", "country": "AU", "lat": -37.8136, "lon": 144.9631},
]


def _weather_details(code: int, is_day: bool) -> tuple[int, str, str]:
    suffix = "d" if is_day else "n"
    if code == 0:
        return 800, "clear sky", f"01{suffix}"
    if code == 1:
        return 801, "mainly clear", f"02{suffix}"
    if code == 2:
        return 802, "partly cloudy", f"03{suffix}"
    if code == 3:
        return 804, "overcast clouds", "04d"
    if code in {45, 48}:
        return 741, "fog", "50d"
    if code in {51, 53, 55}:
        return 300, "drizzle", "09d"
    if code in {56, 57}:
        return 511, "freezing drizzle", "13d"
    if code in {61, 63, 65}:
        return 500, "rain", f"10{suffix}"
    if code in {66, 67}:
        return 511, "freezing rain", "13d"
    if code in {71, 73, 75, 77}:
        return 600, "snow", "13d"
    if code in {80, 81, 82}:
        return 520, "rain showers", "09d"
    if code in {85, 86}:
        return 620, "snow showers", "13d"
    if code in {95, 96, 99}:
        return 200, "thunderstorm", "11d"
    return 800, "clear sky", f"01{suffix}"


def _csv(values: list[float]) -> str:
    return ",".join(f"{value:.4f}" for value in values)


def _value_or(value, fallback):
    return fallback if value is None else value


async def fetch_weather() -> list[dict]:
    results: list[dict] = []
    batch_size = 20
    now = int(time.time())

    async with httpx.AsyncClient(timeout=20) as client:
        for i in range(0, len(CITIES), batch_size):
            batch = CITIES[i : i + batch_size]
            try:
                resp = await client.get(
                    OPEN_METEO_FORECAST,
                    params={
                        "latitude": _csv([city["lat"] for city in batch]),
                        "longitude": _csv([city["lon"] for city in batch]),
                        "current": ",".join(
                            [
                                "temperature_2m",
                                "relative_humidity_2m",
                                "apparent_temperature",
                                "weather_code",
                                "wind_speed_10m",
                                "wind_direction_10m",
                                "is_day",
                            ]
                        ),
                        "temperature_unit": "celsius",
                        "wind_speed_unit": "ms",
                        "timezone": "auto",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as exc:
                print(f"[openmeteo] batch {i} failed: {exc}")
                continue

            entries = data if isinstance(data, list) else [data]
            for city, entry in zip(batch, entries):
                current = entry.get("current") or {}
                temp = current.get("temperature_2m")
                if temp is None:
                    continue

                condition_id, condition, icon = _weather_details(
                    int(current.get("weather_code") or 0),
                    bool(current.get("is_day", 1)),
                )
                results.append(
                    {
                        "city_id": city["city_id"],
                        "city": city["city"],
                        "country": city["country"],
                        "lat": city["lat"],
                        "lon": city["lon"],
                        "temp": temp,
                        "feels_like": _value_or(current.get("apparent_temperature"), temp),
                        "humidity": _value_or(current.get("relative_humidity_2m"), 0),
                        "condition_id": condition_id,
                        "condition": condition,
                        "icon": icon,
                        "wind_speed": _value_or(current.get("wind_speed_10m"), 0.0),
                        "wind_deg": _value_or(current.get("wind_direction_10m"), 0),
                        "fetched_at": now,
                    }
                )

    print(f"[openmeteo] fetched {len(results)} cities")
    return results
