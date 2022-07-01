from fastapi import HTTPException, Depends, status
from .. import operations as GOperations

def admin_auth(active_admin = Depends(GOperations.get_current_active_admin)):
    if not active_admin.role :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized, only admin can access this root",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return active_admin