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
    name="Météo Ville",
    type="city_temperature",
    description="Affiche la température actuelle d'une ville.",
    params=[{"name": "city", "type": "string", "label": "Nom de la ville"}]
)
async def get_weather_data(params: dict, token: str = None):
    city = params.get("city")
    if not city:
        raise HTTPException(status_code=400, detail="Paramètre 'city' manquant")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Configuration serveur: Clé API Météo manquante")

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fr"
        })

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"Ville '{city}' introuvable")

    data = response.json()

    return {
        "city": data.get("name"),
        "temp": round(data["main"]["temp"], 1),
        "desc": data["weather"][0]["description"].capitalize(),
        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }
