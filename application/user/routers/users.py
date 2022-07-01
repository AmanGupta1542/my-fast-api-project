from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Path
from fastapi.requests import Request
from fastapi_mail import MessageSchema, FastMail
from datetime import datetime, timedelta
from typing import Any
from fastapi.responses import JSONResponse

from . import operations as UserO
from ..schemas import common as CSchemas
from ... import schemas as GSchemas
from ... import operations as GOperations
from ...models import ResetPasswordToken
from ...settings import conf as emailConf

router = APIRouter()

@router.get("/")
def root():
    return {"status": "success"}

@router.post("/sign-up", response_model=CSchemas.SignUpUser)
def sign_up(data: CSchemas.UserSignUpData):
    user = UserO.get_user(data.email)
    if user:
        raise HTTPException(status_code= 404, detail="User already exist")
    create_user = UserO.create_user(data)
    return {"staus": "success", "is_active": create_user.isActive, "email": create_user.email}

@router.post("/sign-in", response_model= GSchemas.Token)
def sign_in(data: CSchemas.SignInData):
    user = UserO.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = UserO.create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=15))
        return {"status": "success", "access_token": access_token, "token_type": "bearer"}

@router.get("/sign-out", response_model= CSchemas.Status)
def sign_out(current_uesr: CSchemas.User = Depends(GOperations.get_current_active_user)):
    return {"status": "signout successful"}

@router.patch("/change-password")
def change_password(passwords: CSchemas.ChangePass, current_uesr: CSchemas.User = Depends(GOperations.get_current_active_user)):
    is_password = UserO.verify_password(passwords.oldPassword, current_uesr.password)
    if is_password : 
        current_uesr.password = UserO.get_password_hash(passwords.newPassword)
        current_uesr.save()
        return {"status": "success", "message": "Password changes successfully"}
    else:
        return {"status": "error", "message": "Old password is not correct"}

@router.get("/{user_id}", response_model=CSchemas.User)
def read_user(user_id: int, current_user: CSchemas.User = Depends(GOperations.get_current_active_user)):
    db_user = UserO.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != db_user.id:
        raise HTTPException(status_code=400, detail="Can't access this user")
    return db_user

@router.post("/forget-password")
async def forget_password(request: Request, background_tasks: BackgroundTasks, data: CSchemas.EmailSchema):
    db_user = UserO.get_user(email=data.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    else:
        try:
            token = UserO.reset_password_token()
            create_token = ResetPasswordToken(owner = db_user, token= token)
            create_token.save()
            message = MessageSchema(
                subject="Reset Your Password",
                recipients=[data.email],  # List of recipients, as many as you can pass 
                # body="<a href='http://127.0.0.1:8000/api/reset-password/"+token+"'>Click Here</a>",
                body="{}/api/reset-password/{}".format(request.client.host, token),
                subtype="html"
                )
            fm = FastMail(emailConf)
            background_tasks.add_task(fm.send_message,message)

            return {"status": "success", "message": "Reset password link sent to your email"}
        except: 
            return {"status": "error", "message": "Something went wrong"}

@router.patch("/reset-password/{token}")
def reset_password(data: CSchemas.ResetPassword, token: str = Path(max_length=24)):
    try:
        user_token = ResetPasswordToken.get(ResetPasswordToken.token == token)
    except:
        return {"status": "error", "message": "Invalid Token"}

    if (datetime.now() - user_token.createdAt).days >= 1 or user_token.isExpire:
        return {"status": "error", "message": "Token expires"}
    else:
        user = UserO.get_user_by_id(user_token.owner)
        user.password = UserO.get_password_hash(data.password)
        user.save()
        user_token.isExpire = True
        user_token.save()
        return {"status": "success", "message": "Password reset successfully"}