##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## widget.py
##

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service = Column(String, nullable=False)
    type = Column(String, nullable=False)
    params = Column(JSON, nullable=False, default={})
    position = Column(Integer, default=0)

    user = relationship("User", back_populates="widgets")
