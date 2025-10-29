import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import *
from app.models import *
from app.database import get_db
from app.services.pets_service import *
from app.utils.response import response

logger = logging.getLogger("apis")
router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post("/add-pets",  
    summary="Add a new pet",
    description="This endpoint allows you to create a new pet by providing its details such as name, owner, species, birth, and death date."
    )
def add_pet(pet: PetCreate, db: Session = Depends(get_db)):
    """
    Add a new pat.
    """
    try:
        new_pet = create_pet(pet, db)
        return response(
            status_code=status.HTTP_201_CREATED,
            message="Pet added successfully",
            data=new_pet
        )
    except Exception as e:
        db.rollback()
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding pet: {str(e)}"
        )


@router.get("/get-pets", summary="List all pets",
    description="Retrieve all pets stored in the database. You can optionally filter by species."
    )
def list_pets(species: str | None = Query(default=None), db: Session = Depends(get_db)):
    """
    Retrieves all pets.
    """
    try:
        pets = get_all_pets(db, species)
        return response(
            message="Pets fetched successfully",
            data=pets
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching pets: {str(e)}"
        )
    
@router.put("/edit-pet/{id}", summary="Update a pet by ID",
    description="Update details of an existing pet using its ID."
    )
def update_pet(id: int, pet: PetUpdate, db: Session = Depends(get_db)):
    """
    Edit an existing pet by ID.
    """
    try:
        updated_pet = update_pet_by_id(id, pet, db)
        if not updated_pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return response(
            message="Pet updated successfully",
            data=updated_pet
        )
    except Exception as e:
        db.rollback()
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating pet: {str(e)}"
        )
    
@router.delete("/{id}", summary="Delete a pet by ID",
    description="Remove a pet from the system along with its related events using the pet's unique ID."
    )
def delete_pet(id: int, db: Session = Depends(get_db)):
    """
    Delete a pet by ID.
    """
    try:
        deleted = delete_pet_by_id(id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Pet not found")
        return response(
            status_code=status.HTTP_204_NO_CONTENT,
            message="Pet deleted successfully",
            data=None
        )
    except Exception as e:
        db.rollback()
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting pet: {str(e)}"
        )


@router.get("/pets-with-events/{id}", summary="Get a pet with its events",
    description="Fetch a specific pet along with events linked to it by providing the pet's unique ID."
    )
def get_pet_with_events(id: int, db: Session = Depends(get_db)):
    """
    Get a single pet and all its associated events.
    """
    try:
        pet_data = get_pet_and_events(id, db)
        if not pet_data:
            raise HTTPException(status_code=404, detail="Pet not found")

        return response(
            message="Pet with events fetched successfully",
            data=pet_data
        )
    
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching pet details: {str(e)}"
        )