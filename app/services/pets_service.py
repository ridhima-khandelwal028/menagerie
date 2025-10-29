from sqlalchemy.orm import Session
from app.schemas import *
from app.models import *

def create_pet(pet: PetCreate, db: Session):
    new_pet = Pet(
        name=pet.name,
        owner=pet.owner,
        species=pet.species,
        birth=pet.birth,
        death=pet.death
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return {
        "id": new_pet.id,
        "name": new_pet.name,
        "owner": new_pet.owner,
        "species": new_pet.species,
        "birth": str(new_pet.birth),
        "death": str(new_pet.death)
    }


def get_all_pets(db: Session, species: str | None = None):
    query = db.query(Pet)
    if species:
        query = query.filter(Pet.species == species)
    pets = query.all()

    return [
        {
            "id": pet.id,
            "name": pet.name,
            "owner": pet.owner,
            "species": pet.species,
            "birth": str(pet.birth),
            "death": str(pet.death)
        }
        for pet in pets
    ]


def update_pet_by_id(id: int, pet: PetUpdate, db: Session):
    existing_pet = db.query(Pet).filter(Pet.id == id).first()
    if not existing_pet:
        return None

    existing_pet.name = pet.name
    existing_pet.owner = pet.owner
    existing_pet.species = pet.species
    existing_pet.birth = pet.birth
    existing_pet.death = pet.death

    db.commit()
    db.refresh(existing_pet)

    return {
        "id": existing_pet.id,
        "name": existing_pet.name,
        "owner": existing_pet.owner,
        "species": existing_pet.species,
        "birth": str(existing_pet.birth),
        "death": str(existing_pet.death)
    }

def delete_pet_by_id(id: int, db: Session):
    pet = db.query(Pet).filter(Pet.id == id).first()
    if not pet:
        return False

    # Delete related events first
    db.query(Event).filter(Event.pet_id == id).delete()

    db.delete(pet)
    db.commit()
    return True


def get_pet_and_events(id: int, db: Session):
    pet = db.query(Pet).filter(Pet.id == id).first()
    if not pet:
        return None

    events = (
        db.query(Event)
        .filter(Event.pet_id == id)
        .order_by(Event.date.desc())
        .all()
    )

    return {
        "pet": {
            "id": pet.id,
            "name": pet.name,
            "owner": pet.owner,
            "species": pet.species,
            "birth": str(pet.birth),
            "death": str(pet.death),
        },
        "events": [
            {
                "id": event.id,
                "date": str(event.date),
                "type": event.type,
                "remark": event.remark,
                "pet_id": event.pet_id,
            }
            for event in events
        ],
    }
