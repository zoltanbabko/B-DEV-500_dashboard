##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## google.py
##

import os
import urllib.parse
import json
import jwt as pyjwt
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.oauth.utils import process_oauth_login
from app.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth/google", tags=["auth_google"])
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = "openid email profile https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/calendar.events.readonly"
FRONTEND_URL = os.getenv("FRONTEND_URL")

@router.get("/login")
def login(token: str = None):
    state_data = {}
    
    if token:
        try:
            payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id:
                state_data["link_user_id"] = int(user_id)
        except Exception:
            pass

    state_str = json.dumps(state_data)
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": state_str
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@router.get("/callback")
async def callback(code: str, state: str = None, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(400, "Code not found")

    link_user_id = None
    if state:
        try:
            state_data = json.loads(state)
            link_user_id = state_data.get("link_user_id")
        except Exception:
            pass

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

    try:
        jwt = process_oauth_login(db, "google", user_info, token_data, link_user_id)
    except HTTPException as exep:
        raise exep

    return RedirectResponse(f"{FRONTEND_URL}/login?token={jwt}")
