from pydantic import EmailStr
from fastapi import Depends, status, HTTPException
import string, random
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError

from ...models import User
from ...dependencies import pwd_context, token_auth_scheme
from ... import settings as GSettings
from ..schemas import common as CSchemas

def reset_password_token(size=24, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, password):
    try:
        return pwd_context.verify(plain_password, password)
    except :
        print("unknown hash error")
        return False

def get_user(email: EmailStr):
    try:
        return User.get(User.email == email)
    except User.DoesNotExist :
        return False
    except: 
        return False

def get_user_by_id(id: int):
    try:
        return User.get(User.id == id)
    except: 
        return False

def create_user(data: CSchemas.UserSignUpData):
    password = get_password_hash(data.password)
    db_user = User(email= data.email, password= password, isActive= False, role=0, accessType=0)
    db_user.save()
    return db_user

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta , None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, GSettings.settings.secret_key, algorithm=GSettings.settings.algorithm)
    return encoded_jwt