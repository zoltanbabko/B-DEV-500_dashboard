##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## utils.py
##

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User, OAuth2Token
from app.security import create_access_token

def process_oauth_login(db: Session, provider: str, user_info: dict, token_data: dict):
    email = user_info.get("email")

    if not email and "login" in user_info:
         email = str(user_info['login'])
    if not email:
        raise ValueError("Impossible de récupérer l'email depuis le provider.")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(email=email, password=None)
        db.add(user)
        db.commit()
        db.refresh(user)

    oauth_token = db.query(OAuth2Token).filter(
        OAuth2Token.user_id == user.id,
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
            user_id=user.id,
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        db.add(oauth_token)

    db.commit()

    jwt_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return jwt_token
