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
    name="Gmail - Unread Emails",
    type="gmail_unread",
    description="Display the count and last 3 unread emails from Gmail",
    params=[]
)
async def get_gmail_unread(params: dict, token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Google token is required")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        list_resp = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers=headers,
            params={"q": "is:unread"}
        )

        if list_resp.status_code != 200:
             raise HTTPException(status_code=400, detail="Error Gmail API try to reconnect Google")

        nb_unread = list_resp.json().get("resultSizeEstimate", 0)
        messages_meta = list_resp.json().get("messages", [])[:3]
        emails = []
        for msg in messages_meta:
            detail_resp = await client.get(
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}",
                headers=headers
            )
            data = detail_resp.json()
            payload = data.get("payload", {})
            headers_list = payload.get("headers", [])
            subject = next((h["value"] for h in headers_list if h["name"] == "Subject"), "(Without Subject)")
            sender = next((h["value"] for h in headers_list if h["name"] == "From"), "Unknown Sender")
            emails.append({"subject": subject, "from": sender.split("<")[0].strip()})

    return {"count": nb_unread, "emails": emails}
