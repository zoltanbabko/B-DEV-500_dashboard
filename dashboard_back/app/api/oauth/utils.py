##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## utils.py
##

from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, OAuth2Token
from app.security import create_access_token

def process_oauth_login(db: Session, provider: str, user_info: dict, token_data: dict, link_user_id: int = None):
    email = user_info.get("email")
    if not email and "login" in user_info:
         email = str(user_info['login'])

    if not email:
        raise ValueError("Can't retrieve email from provider")

    user_by_email = db.query(User).filter(User.email == email).first()
    target_user = None

    if link_user_id:
        target_user = db.query(User).filter(User.id == link_user_id).first()
        if not target_user:
            raise HTTPException(400, "User to link not found")
        if user_by_email and user_by_email.id != target_user.id:
            raise HTTPException(400, f"Account {provider} ({email}) is already linked to another user.")
    else:
        target_user = user_by_email
        if not target_user:
            target_user = User(email=email, password=None)
            db.add(target_user)
            db.commit()
            db.refresh(target_user)

    oauth_token = db.query(OAuth2Token).filter(
        OAuth2Token.user_id == target_user.id,
        OAuth2Token.provider == provider
    ).first()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")
    expires_at = None

    if expires_in:
        expires_at = int(datetime.now(timezone.utc).timestamp()) + int(expires_in)
    if oauth_token:
        oauth_token.access_token = access_token
        if expires_at:
            oauth_token.expires_at = expires_at
        if refresh_token:
            oauth_token.refresh_token = refresh_token
    else:
        oauth_token = OAuth2Token(
            user_id=target_user.id,
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        db.add(oauth_token)

    db.commit()

    jwt_token = create_access_token(data={"sub": str(target_user.id), "email": target_user.email})
    return jwt_token
