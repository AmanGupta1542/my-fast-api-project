from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from . import operations as UserO
from ..schemas import common as CSchemas
from ... import schemas as GSchemas

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

@router.post("/sign-in", response_model= GSchemas.Token)
def sign_in(data: CSchemas.SignInData):
    user = UserO.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = UserO.create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=15))
        return {"status": "success", "access_token": access_token, "token_type": "bearer"}