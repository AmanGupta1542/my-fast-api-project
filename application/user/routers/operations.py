from pydantic import EmailStr
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError

from ...models import User
from ...dependencies import pwd_context
from ... import settings as GSettings
from ..schemas import common as CSchemas

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, password):
    try:
        return pwd_context.verify(plain_password, password)
    except :
        print("unknown has error")
        return False

def get_user(email: EmailStr):
    try:
        return User.get(User.email == email)
    except User.DoesNotExist :
        return False
    except: 
        return False

def create_user(data: CSchemas.UserSignUpData):
    password = get_password_hash(data.password)
    db_user = User(email= data.email, password= password, isActive= False)
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