# 🌦️ FastAPI Weather API Wrapper

A lightweight weather data API with caching, built with FastAPI. Fetches real-time weather from OpenWeatherMap.

## Features (Planned)
✅ Weather by city/coordinates  
✅ Redis caching  
✅ Rate limiting  
✅ Auto-generated docs (Swagger/Redoc)

## Tech Stack
- Python 3.9+
- FastAPI
- Redis (caching)
- OpenWeatherMap API

## 🚀 Quick Start
```bash
# Install dependencies
git clone https://github.com/yourusername/weather-api.git
cd weather-api
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload