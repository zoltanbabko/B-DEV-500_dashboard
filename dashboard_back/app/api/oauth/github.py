##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## github.py
##

import os
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/github", tags=["auth_github"])

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")

@router.get("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "user:email"
    }
    url = f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        headers = {"Accept": "application/json"}
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            headers=headers
        )
        token_data = token_resp.json()

        if "error" in token_data:
            raise HTTPException(400, f"GitHub Error: {token_data}")

        access_token = token_data.get("access_token")

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_resp.json()
        if not user_info.get("email"):
            emails_resp = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            emails = emails_resp.json()
            for e in emails:
                if e.get("primary") and e.get("verified"):
                    user_info["email"] = e["email"]
                    break

    jwt = process_oauth_login(db, "github", user_info, token_data)
    return RedirectResponse(f"{FRONTEND_URL}/login?token={jwt}")
