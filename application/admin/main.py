from fastapi import FastAPI, Depends

from ..dependencies import get_db
from ..dependencies import token_auth_scheme
from .routers import users

app = FastAPI(dependencies=[Depends(get_db), Depends(token_auth_scheme)])

app.include_router(users.router)