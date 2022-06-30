from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer 

from ..dependencies import get_db
from .routers import users

auth_admin = HTTPBearer()

app = FastAPI(dependencies=[Depends(get_db), Depends(auth_admin)])

app.include_router(users.router)