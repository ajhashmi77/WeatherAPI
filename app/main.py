from fastapi import FastAPI

app = FastAPI(
    title="Weather API",
    description="Fetches weather data with caching",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Weather API!",
        "endpoints": {
            "future": "/weather?city={name}"
        }
    }