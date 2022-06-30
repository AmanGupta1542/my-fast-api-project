from pydantic import EmailStr

from ...models import User
from ...dependencies import pwd_context
from ..schemas import common as CSchemas

def get_password_hash(password):
    return pwd_context.hash(password)

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
