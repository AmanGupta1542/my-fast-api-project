from pydantic import BaseModel, EmailStr, Field
from pydantic.utils import GetterDict
import peewee
from typing import Any, Union

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class ChangePass(BaseModel):
    oldPassword: str = Field(min_length=6)
    newPassword: str = Field(min_length=6)
    
class EmailSchema(BaseModel):
    email: EmailStr

class TokenData(BaseModel):
    email: Union[EmailStr, None] = None

#***************************** Respose models ************************************ #
class Status(BaseModel):
    status: str

class SignUpUser(EmailSchema):
    is_active: bool


#***************************** Request models ************************************ #

class UserSignUpData(EmailSchema):
    password: str = Field(min_length=6)

class ResetPassword(BaseModel):
    password: str = Field(
        title="Password of the user", min_length=6
    )

class SignInData(EmailSchema):
    email: EmailStr
    password: str

class User(EmailSchema):
    id: int
    isActive: bool

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
