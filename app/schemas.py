# app/schemas.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PetBase(BaseModel):
    name: str
    owner: str
    species: str
    birth: datetime
    death: Optional[datetime]


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str]
    owner: Optional[str]
    species: Optional[str]
    birth: Optional[datetime]
    death: Optional[datetime]


class EventBase(BaseModel):
    type: str
    remark: Optional[str]
    date: datetime

class EventCreate(EventBase):
    pass
