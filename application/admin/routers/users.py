from fastapi import APIRouter, HTTPException
from typing import Any, List

from . import operations as AdminO
router = APIRouter()

@router.get("/")
def root():
    return {"status": "success"}

@router.get("/{id}")
def get_admin(id: int):
    admin = AdminO.get_admin(id)
    if admin:
        return {"status": "success", "admin": admin}
    else:
        raise HTTPException(status_code= 404, detail="Admin not found")