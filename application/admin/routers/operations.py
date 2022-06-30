from ...models import Admin

def get_admin(id: int):
    try:
        return Admin.get(Admin.id == id)
    except:
        return False