from fastapi import Depends
from passlib.context import CryptContext

from .database import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()