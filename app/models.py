# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    birth = Column(DateTime, nullable=True)
    death = Column(DateTime, nullable=True)

    # Relationship to events
    events = relationship("Event", back_populates="pet", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    type = Column(String(100), nullable=False)
    remark = Column(String(255), nullable=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)

    # Relationship back to pet
    pet = relationship("Pet", back_populates="events")
