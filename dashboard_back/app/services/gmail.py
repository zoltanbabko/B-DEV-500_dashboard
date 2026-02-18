##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## gmail.py
##

import httpx
from fastapi import HTTPException
from app.services.registry import register_widget

@register_widget(
    service="google",
    name="Gmail - Non lus",
    type="gmail_unread",
    description="Affiche les 3 derniers emails non lus.",
    params=[]
)
async def get_gmail_unread(params: dict, token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Google non connecté")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        list_resp = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers=headers,
            params={"q": "is:unread", "maxResults": 3}
        )

        if list_resp.status_code != 200:
             raise HTTPException(status_code=400, detail="Erreur Gmail API")

        messages_meta = list_resp.json().get("messages", [])
        emails = []
        for msg in messages_meta:
            detail_resp = await client.get(
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}",
                headers=headers
            )
            data = detail_resp.json()
            payload = data.get("payload", {})
            headers_list = payload.get("headers", [])
            subject = next((h["value"] for h in headers_list if h["name"] == "Subject"), "(Sans sujet)")
            sender = next((h["value"] for h in headers_list if h["name"] == "From"), "Inconnu")
            emails.append({"subject": subject, "from": sender.split("<")[0].strip()})

    return {"count": len(emails), "emails": emails}
