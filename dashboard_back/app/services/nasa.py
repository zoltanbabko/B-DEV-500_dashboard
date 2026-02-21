##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## nasa.py
##

import httpx
from app.services.registry import register_widget

@register_widget(
    service="nasa",
    name="Astronomy Picture",
    type="nasa_apod",
    description="Picture of the day from NASA's Astronomy Picture.",
    params=[]
)
async def get_nasa_apod(params: dict, token: str = None):
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {
                "title": "Error NASA",
                "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                "copyright": "",
                "type": "image"
            }
            
        data = response.json()
        
        return {
            "title": data.get("title", "Without title"),
            "url": data.get("url"),
            "copyright": data.get("copyright", "NASA"),
            "type": data.get("media_type", "image")
        }

