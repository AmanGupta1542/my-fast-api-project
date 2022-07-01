from fastapi import APIRouter, HTTPException
from typing import Any, List

from . import operations as AdminO
from .. import schemas as CSchemas
router = APIRouter()

@router.get("/")
def root():
    return {"status": "success"}

@router.get("/{id}", response_model=CSchemas.User)
def get_admin(id: int):
    admin = AdminO.get_person(id)
    if admin:
        return admin
    else:
        raise HTTPException(status_code= 404, detail="Not found")

@router.get("/all-admins", response_model= List[CSchemas.User])
def get_all_admins():
    admins =  AdminO.get_all_person(admin=True)
    if admins:
        return admins
    else:
        raise HTTPException(status_code= 404, detail="Not found")

@router.get("/all-users", response_model= List[CSchemas.User])
def get_all_users():
    users = AdminO.get_all_person()
    if users:
        return users
    else:
        raise HTTPException(status_code= 404, detail="Not found")