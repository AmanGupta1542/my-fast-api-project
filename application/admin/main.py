from fastapi import FastAPI, Depends

from ..dependencies import get_db
from .routers import users

# app = FastAPI(dependencies= Depends[Depends(get_db) ])
app = FastAPI()

app.include_router(users.router)