from ...models import User

def get_person(id: int):
    try:
        return User.get(User.id == id)
    except:
        return False

def get_all_person(admin:bool=False):
    try:
        if admin:
            return list(User.filter(User.role==1))
        else:
            return list(User.filter(User.role==0))
    except: 
        return False