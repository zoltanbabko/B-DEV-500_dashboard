##
## EPITECH PROJECT, 2025
## Dashboard
## File description:
## citybikes.py
##

import httpx
from fastapi import HTTPException
from app.services.registry import register_widget


@register_widget(
    service="transport",
    name="City Bikes",
    type="city_bikes",
    description="View real-time bike availability in major cities using the CityBikes API.",
    params=[{"name": "city", "type": "string", "label": "By", "default": "Paris"}]
)
async def get_city_bikes(params: dict, token: str = None):
    city_name = params.get("city", "Paris").lower().strip()

    async with httpx.AsyncClient() as client:
        resp = await client.get("http://api.citybik.es/v2/networks")
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Error fetching bike networks")

        networks = resp.json().get("networks", [])
        network_id = None
        network_name = ""

        for net in networks:
            if net.get("location") and city_name in net["location"].get("city", "").lower():
                network_id = net["id"]
                network_name = net["name"]
                break

        if not network_id:
            raise HTTPException(status_code=404, detail=f"No bike network found for '{city_name}'")

        resp_stations = await client.get(f"http://api.citybik.es/v2/networks/{network_id}")
        if resp_stations.status_code != 200:
            raise HTTPException(status_code=400, detail="Error fetching bike stations")

        stations = resp_stations.json().get("network", {}).get("stations", [])
        sorted_stations = sorted(stations, key=lambda x: x.get("free_bikes", 0), reverse=True)
        top_stations = sorted_stations[:5]
        total_bikes = sum(s.get("free_bikes", 0) for s in stations)
        total_slots = sum(s.get("empty_slots", 0) for s in stations)

        return {
            "city": city_name.capitalize(),
            "network_name": network_name,
            "total_bikes": total_bikes,
            "total_slots": total_slots,
            "stations": [
                {
                    "name": s["name"],
                    "free_bikes": s["free_bikes"],
                    "empty_slots": s["empty_slots"]
                } for s in top_stations
            ]
        }
