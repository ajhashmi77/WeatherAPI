from fastapi import FastAPI, HTTPException
import httpx
import redis
import os
from dotenv import load_dotenv
import json

load_dotenv()
app = FastAPI()

# Redis setup
redis_client = redis.Redis(
    host="redis",  # Use 'redis' for Docker, 'localhost' for local
    port=6379,
    db=0,
    decode_responses=True
)

@app.get("/weather")
async def get_weather(city: str):
    try:
        # Check cache first
        cached_data = redis_client.get(f"weather:{city}")
        if cached_data:
            return {"data": json.loads(cached_data), "source": "cache"}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}"
            )
            
            # Handle API errors - must check status before accessing response
            if response.status_code != 200:
                # Parse error response
                error_data = response.json()
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_data.get("message", "API error")
                )
            
            # Get successful response data
            data = response.json()
            
            # Cache for 30 minutes (1800 seconds)
            redis_client.setex(
                f"weather:{city}",
                1800,
                json.dumps(data)
            )
            return {"data": data, "source": "API"}
    
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Weather service unavailable")