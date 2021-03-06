from fastapi import FastAPI, Depends, HTTPException, status

from ..dependencies import get_db
from .. import operations as GOperations
from .routers import users
from .dependencies import admin_auth

def admin_auth(active_admin = Depends(GOperations.get_current_active_admin)):
    if not active_admin.role :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized, only admin can access this root",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return active_admin

app = FastAPI(dependencies=[Depends(get_db), Depends(admin_auth)])

app.include_router(users.router)