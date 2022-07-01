from pydantic import BaseModel, EmailStr
from pydantic.utils import GetterDict
import peewee
from typing import Any, List

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class PersonId(BaseModel):
    id: int
    
class User(BaseModel):
    id: str
    email: EmailStr
    isActive: bool
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class Admin(User):
    access_type: int
