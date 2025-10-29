import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import *
from app.models import *
from app.database import get_db
from app.services.event_service import *
from app.services.pets_service import *
from app.utils.response import response

logger = logging.getLogger("apis")
router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/pets/{pet_id}/events", summary="Add an event for a pet",
    description="Create a new event for a given pet by specifying the pet ID and event details such as type, date, and remarks."
    )
def add_event(pet_id: int, event: EventCreate, db: Session = Depends(get_db)):
    """
    Add a new event for a specific pet.
    """
    try:
        new_event = create_event_for_pet(pet_id, event, db)
        if not new_event:
            raise HTTPException(status_code=404, detail="Pet not found")

        return response(
            status_code=status.HTTP_201_CREATED,
            message="Event added successfully",
            data=new_event
        )

    except Exception as e:
        db.rollback()
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding event: {str(e)}"
        )
