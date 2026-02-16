##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## google.py
##

import os
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/google", tags=["auth_google"])

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = "openid email profile"

@router.get("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        token_data = token_resp.json()

        if "error" in token_data:
            raise HTTPException(400, f"Google Error: {token_data}")

        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data.get('access_token')}"}
        )
        user_info = user_resp.json()

    jwt = process_oauth_login(db, "google", user_info, token_data)
    return JSONResponse({"access_token": jwt, "token_type": "bearer", "provider": "google"})
