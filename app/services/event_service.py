from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *

def create_event_for_pet(pet_id: int, event: EventCreate, db: Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        return None
    
    new_event = Event(
        pet_id=pet_id,
        date=event.date,
        type=event.type,
        remark=event.remark
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "id": new_event.id,
        "pet_id": new_event.pet_id,
        "date": str(new_event.date),
        "type": new_event.type,
        "remark": new_event.remark
    }

