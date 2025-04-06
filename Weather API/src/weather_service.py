import os
import requests
import redis
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_API_BASE_URL = os.environ.get("WEATHER_API_BASE_URL")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
CACHE_EXPIRATION = int(os.environ.get("CACHE_EXPIRATION_SECONDS", 43200))

redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True
)


def get_weather(city: str) -> dict:

    cached_data = redis_client.get(city)
    if cached_data:
        print(f"[CACHE] Returning cached weather for {city}")
        return {"source": "cache", "data": cached_data}

    print(f"[API] Fetching weather data for {city}")
    if not WEATHER_API_KEY or not WEATHER_API_BASE_URL:
        raise ValueError("API key or base URL not configured properly.")

    url = f"{WEATHER_API_BASE_URL}/{city}?key={WEATHER_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching weather data: {str(e)}")

    data = response.json()

    redis_client.setex(city, CACHE_EXPIRATION, str(data))

    return {"source": "api", "data": str(data)}
