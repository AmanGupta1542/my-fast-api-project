from fastapi import FastAPI, Depends

from ..dependencies import get_db
from .routers import users

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(users.router)