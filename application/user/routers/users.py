from fastapi import APIRouter, HTTPException

from . import operations as UserO
from ..schemas import common as CSchemas

router = APIRouter()

@router.get("/")
def root():
    return {"status": "success"}

@router.post("/sign-up", response_model=CSchemas.SignUpUser)
def sign_up(data: CSchemas.UserSignUpData):
    user = UserO.get_user(data.email)
    if user:
        raise HTTPException(status_code= 404, detail="User already exist")
    create_user = UserO.create_user(data)
    return {"staus": "success", "is_active": create_user.isActive, "email": create_user.email}