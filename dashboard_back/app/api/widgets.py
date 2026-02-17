##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## widgets.py
##

from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, OAuth2Token
from app.models.widget import Widget
from app.schemas import WidgetCreate, WidgetOut, WidgetUpdate, AvailableWidget
from app.api.auth import get_current_user 
from app.services.registry import WIDGET_REGISTRY

router = APIRouter(prefix="/widgets", tags=["Widgets"])

@router.get("/available", response_model=List[AvailableWidget])
def get_available_widgets():
    return [
        AvailableWidget(
            service=w["service"],
            name=w["name"],
            type=w["type"],
            description=w["description"],
            params=w["params"]
        )
        for w in WIDGET_REGISTRY.values()
    ]


@router.get("/", response_model=List[WidgetOut])
def get_dashboard(user: User = Depends(get_current_user)):
    return user.widgets


@router.post("/", response_model=WidgetOut)
def add_widget(widget_in: WidgetCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if widget_in.type not in WIDGET_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Widget type '{widget_in.type}' does not exist.")

    new_widget = Widget(
        user_id=user.id,
        service=widget_in.service,
        type=widget_in.type,
        params=widget_in.params,
        position=widget_in.position
    )
    db.add(new_widget)
    db.commit()
    db.refresh(new_widget)
    return new_widget

@router.delete("/{widget_id}")
def delete_widget(widget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.user_id == user.id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    db.delete(widget)
    db.commit()
    return {"status": "deleted"}


@router.put("/{widget_id}", response_model=WidgetOut)
def update_widget(widget_id: int, update_in: WidgetUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.user_id == user.id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    if update_in.params is not None:
        widget.params = update_in.params
    if update_in.position is not None:
        widget.position = update_in.position

    db.commit()
    db.refresh(widget)
    return widget


@router.get("/{widget_id}/data")
async def get_widget_data(widget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id, Widget.user_id == user.id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found in your dashboard")

    definition = WIDGET_REGISTRY.get(widget.type)
    if not definition:
        raise HTTPException(status_code=500, detail=f"Widget handler for '{widget.type}' not found. Restart the server ?")

    handler_func = definition["handler"]
    service_name = definition["service"]

    access_token = None
    
    SERVICES_WITH_AUTH = ["github", "google"]

    if service_name in SERVICES_WITH_AUTH:
        oauth_token = db.query(OAuth2Token).filter(
            OAuth2Token.user_id == user.id,
            OAuth2Token.provider == service_name
        ).first()

        if oauth_token:
            access_token = oauth_token.access_token
        else:
            pass

    try:
        return await handler_func(widget.params, access_token)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Erreur Interne Widget {widget.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur interne du widget: {str(e)}")
