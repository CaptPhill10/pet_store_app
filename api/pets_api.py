import structlog
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import List, Dict
from data.pets_data import pets as init_pets

router = APIRouter()
logger = structlog.get_logger(__name__)


# Pet module
class Pet(BaseModel):
    id: int
    name: str
    status: str


# New pet module
class NewPet(BaseModel):
    name: str
    category: Dict[str, int | str]
    status: str


class PetStore:
    def __init__(self, init_pets):
        self.pets = init_pets

    def find_pets_by_status(self, status):
        logger.info("Finding pets with status", status=status)
        pets = [pet for pet in self.pets if pet["status"] == status]
        logger.info("Found pets with status", status=status, count=len(pets))
        return pets

    def get_pet_by_id(self, pet_id):
        logger.info("Getting pet by ID", pet_id=pet_id)
        pet = next((pet for pet in self.pets if pet["id"] == pet_id), None)
        if not pet:
            logger.warning("Pet with ID not found", pet_id=pet_id)
            raise HTTPException(status_code=404, detail="Pet not found")
        return pet

    def add_pet(self, pet: NewPet):
        logger.info("Adding new pet", pet=pet.model_dump())
        new_id = max([p["id"] for p in self.pets]) + 1 if self.pets else 1
        pet_data = pet.model_dump()
        pet_data["id"] = new_id
        self.pets.append(pet_data)
        logger.info("Added new pet with ID", pet_id=new_id)
        return pet_data

    def update_pet(self, pet: Pet):
        logger.info("Updating pet", pet_id=pet.id, pet=pet.model_dump())
        existing_pet = self.get_pet_by_id(pet.id)
        existing_pet.update({"name": pet.name, "status": pet.status})
        logger.info("Pet updated successfully", pet_id=pet.id, pet=existing_pet)
        return existing_pet

    def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None):
        logger.info("Updating pet with ID using form data", pet_id=pet_id, name=name, status=status)
        existing_pet = self.get_pet_by_id(pet_id)
        if name is not None:
            existing_pet["name"] = name
        if status is not None:
            existing_pet["status"] = status
        logger.info("Pet updated successfully with form", pet_id=pet_id, pet=existing_pet)
        return existing_pet

    def delete_pet(self, pet_id):
        logger.info("Deleting pet", pet_id=pet_id)
        pet = self.get_pet_by_id(pet_id)
        self.pets = [p for p in self.pets if p["id"] != pet_id]
        logger.info("Pet deleted successfully", pet_id=pet_id)
        return {"message": f"Pet with ID {pet_id} has been deleted"}


pet_store = PetStore(init_pets)


@router.get("/pet/findByStatus", response_model=List[Dict])
async def find_pets_by_status(status: str):
    logger.info("Received request to find pets by status", status=status)
    pets = pet_store.find_pets_by_status(status)
    if not pets:
        raise HTTPException(status_code=404, detail="Pets not found")
    return pets


@router.get("/pet/{pet_id}", response_model=Dict)
async def get_pet_by_id(pet_id: int):
    logger.info("Received request to get pet by ID", pet_id=pet_id)
    pet = pet_store.get_pet_by_id(pet_id)
    return pet


@router.post("/pet", response_model=Dict, status_code=201)
async def add_pet(pet: NewPet):
    logger.info("Received request to add new pet", pet=pet.model_dump())
    return pet_store.add_pet(pet)


@router.put("/pet", response_model=Dict)
async def update_pet(pet: Pet):
    logger.info("Received request to update pet", pet=pet.model_dump())
    return pet_store.update_pet(pet)


@router.post("/pet/{pet_id}")
async def update_pet_with_form(
    pet_id: int,
    name: str = Form(None),
    status: str = Form(None)
):
    logger.info("Received request to update pet with ID using form data", pet_id=pet_id, name=name, status=status)
    updated_pet = pet_store.update_pet_with_form(pet_id, name, status)
    return {"message": "Pet updated successfully", "pet": updated_pet}


@router.delete("/pet/{pet_id}")
async def delete_pet(pet_id: int):
    logger.info("Received request to delete pet", pet_id=pet_id)
    return pet_store.delete_pet(pet_id)

# import logging
# from fastapi import APIRouter, HTTPException, Form
# from pydantic import BaseModel
# from typing import List, Dict
# from data.pets_data import pets as init_pets
#
# router = APIRouter()
# logger = logging.getLogger(__name__)
#
#
# # Pet module
# class Pet(BaseModel):
#     id: int
#     name: str
#     status: str
#
#
# # New pet module
# class NewPet(BaseModel):
#     name: str
#     category: Dict[str, int | str]
#     status: str
#
#
# class PetStore:
#     def __init__(self, init_pets):
#         self.pets = init_pets
#
#     def find_pets_by_status(self, status):
#         logger.info(f"Finding pets with status: {status}")
#         pets = [pet for pet in self.pets if pet["status"] == status]
#         logger.info(f"Found {len(pets)} pets with status {status}")
#         return pets
#
#     def get_pet_by_id(self, pet_id):
#         logger.info(f"Getting pet by ID: {pet_id}")
#         pet = next((pet for pet in self.pets if pet["id"] == pet_id), None)
#         if not pet:
#             logger.warning(f"Pet with ID {pet_id} not found")
#             raise HTTPException(status_code=404, detail="Pet not found")
#         return pet
#
#     def add_pet(self, pet: NewPet):
#         logger.info(f"Adding new pet: {pet.dict()}")
#         new_id = max([p["id"] for p in self.pets]) + 1 if self.pets else 1
#         pet_data = pet.dict()
#         pet_data["id"] = new_id
#         self.pets.append(pet_data)
#         logger.info(f"Added new pet with ID: {new_id}")
#         return pet_data
#
#     def update_pet(self, pet: Pet):
#         logger.info(f"Updating pet with ID: {pet.id}")
#         existing_pet = self.get_pet_by_id(pet.id)
#         existing_pet.update({"name": pet.name, "status": pet.status})
#         logger.info(f"Pet with ID {pet.id} updated successfully: {existing_pet}")
#         return existing_pet
#
#     def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None):
#         logger.info(f"Updating pet with ID: {pet_id} using form data")
#         existing_pet = self.get_pet_by_id(pet_id)
#         if name is not None:
#             existing_pet["name"] = name
#         if status is not None:
#             existing_pet["status"] = status
#         logger.info(f"Pet with ID {pet_id} updated successfully: {existing_pet}")
#         return existing_pet
#
#     def delete_pet(self, pet_id):
#         logger.info(f"Deleting pet with ID: {pet_id}")
#         pet = self.get_pet_by_id(pet_id)
#         self.pets = [p for p in self.pets if p["id"] != pet_id]
#         logger.info(f"Pet with ID {pet_id} deleted successfully")
#         return {"message": f"Pet with ID {pet_id} has been deleted"}
#
#
# pet_store = PetStore(init_pets)
#
#
# @router.get("/pet/findByStatus", response_model=List[Dict])
# async def find_pets_by_status(status: str):
#     logger.info(f"Received request to find pets by status: {status}")
#     pets = pet_store.find_pets_by_status(status)
#     if not pets:
#         raise HTTPException(status_code=404, detail="Pets not found")
#     return pets
#
#
# @router.get("/pet/{pet_id}", response_model=Dict)
# async def get_pet_by_id(pet_id: int):
#     logger.info(f"Received request to get pet by ID: {pet_id}")
#     pet = pet_store.get_pet_by_id(pet_id)
#     return pet
#
#
# @router.post("/pet", response_model=Dict, status_code=201)
# async def add_pet(pet: NewPet):
#     logger.info(f"Received request to add new pet: {pet.dict()}")
#     return pet_store.add_pet(pet)
#
#
# @router.put("/pet", response_model=Dict)
# async def update_pet(pet: Pet):
#     logger.info(f"Received request to update pet: {pet.dict()}")
#     return pet_store.update_pet(pet)
#
#
# @router.post("/pet/{pet_id}")
# async def update_pet_with_form(
#     pet_id: int,
#     name: str = Form(None),
#     status: str = Form(None)
# ):
#     logger.info(f"Received request to update pet with ID {pet_id} using form data")
#     updated_pet = pet_store.update_pet_with_form(pet_id, name, status)
#     return {"message": "Pet updated successfully", "pet": updated_pet}
#
#
# @router.delete("/pet/{pet_id}")
# async def delete_pet(pet_id: int):
#     logger.info(f"Received request to delete pet with ID: {pet_id}")
#     return pet_store.delete_pet(pet_id)
