##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## main.py
##

from fastapi import FastAPI
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.models import user, widget
from app.api import auth, widgets
from app.api.oauth import google, github

import app.services.weather
import app.services.gmail
import app.services.github
import app.services.nasa
import app.services.cats
import app.services.calendar
import app.services.citybikes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(google.router)
app.include_router(github.router)
app.include_router(widgets.router)

@app.get("/")
def read_root():
    return {"status": "Dashboard Backend Running"}
