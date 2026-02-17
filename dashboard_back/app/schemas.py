##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## schemas.py
##

from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, List


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class AvailableWidget(BaseModel):
    service: str
    name: str
    type: str
    description: str
    params: List[Dict[str, Any]]

class WidgetBase(BaseModel):
    service: str
    type: str
    params: Dict[str, Any] = {}
    position: int = 0

class WidgetCreate(WidgetBase):
    pass

class WidgetUpdate(BaseModel):
    params: Optional[Dict[str, Any]] = None
    position: Optional[int] = None

class WidgetOut(WidgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
