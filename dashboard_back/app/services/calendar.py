##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## calendar.py
##

import httpx
from datetime import datetime
from fastapi import HTTPException
from app.services.registry import register_widget

@register_widget(
    service="google",
    name="Google Calendar",
    type="google_calendar",
    description="Display 5 upcoming events from Google Calendar",
    params=[]
)
async def get_upcoming_events(params: dict, token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Google non connecté")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    now = datetime.utcnow().isoformat() + "Z"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers=headers,
            params={
                "maxResults": 5,
                "orderBy": "startTime",
                "singleEvents": True,
                "timeMin": now
            }
        )

        if response.status_code != 200:
             raise HTTPException(status_code=400, detail="Error Calendar API try to reconnect Google")

        items = response.json().get("items", [])
        events = []
        for item in items:
            start = item["start"].get("dateTime", item["start"].get("date"))
            events.append({
                "summary": item.get("summary", "(Sans titre)"),
                "start": start,
                "link": item.get("htmlLink")
            })

    return events
