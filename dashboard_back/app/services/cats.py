##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## cats.py
##

import httpx
from app.services.registry import register_widget

@register_widget(
    service="fun",
    name="Random Cat",
    type="random_cat",
    description="Renders a random cat image.",
    params=[]
)
async def get_random_cat(params: dict, token: str = None):
    url = "https://api.thecatapi.com/v1/images/search"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
             return {"image": "https://cdn2.thecatapi.com/images/0xyvRd7oD.jpg"}

        data = response.json()
        if not data:
             return {"image": ""}

        return {
            "image": data[0]["url"]
        }
