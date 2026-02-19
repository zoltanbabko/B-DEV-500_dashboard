##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## weather.py
##

import os
import httpx
from fastapi import HTTPException
from app.services.registry import register_widget

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@register_widget(
    service="weather",
    name="City Weather",
    type="city_temperature",
    description="Displays the current temperature of a city.",
    params=[{"name": "city", "type": "string", "label": "City name"}]
)
async def get_weather_data(params: dict, token: str = None):
    city = params.get("city")
    if not city:
        raise HTTPException(status_code=400, detail="Parameter 'city' is required")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "en"
        })

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    data = response.json()

    return {
        "city": data.get("name"),
        "temp": round(data["main"]["temp"], 1),
        "desc": data["weather"][0]["description"].capitalize(),
        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }
