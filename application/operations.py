from fastapi import Depends, status, HTTPException
from pydantic import EmailStr
from typing import Union
from datetime import datetime, timedelta
from jose import jwt, JWTError

from .models import User
from .settings import settings
from .dependencies import token_auth_scheme
from . import schemas as GSchemas


def get_user(email: EmailStr):
    try:
        return User.get(User.email == email)
    except: 
        return False
        
def create_access_token(data: dict, expires_delta: Union[timedelta , None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(token_auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = GSchemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: GSchemas.User = Depends(get_current_user)):
    # if not current_user.isActive:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_admin(current_user: GSchemas.Admin = Depends(get_current_user)):
    # if not current_user.isActive:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user