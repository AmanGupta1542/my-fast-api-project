from lib2to3.pytree import Base
from pydantic import BaseModel, EmailStr, Field

class EmailSchema(BaseModel):
    email: EmailStr


#***************************** Respose models ************************************ #
class Status(BaseModel):
    status: str

class SignUpUser(EmailSchema):
    is_active: bool


#***************************** Request models ************************************ #

class UserSignUpData(EmailSchema):
    password: str = Field(min_length=6)

class SignInData(EmailSchema):
    email: EmailStr
    password: str
