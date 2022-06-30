from fastapi import FastAPI

from .admin import main as admin_root
from .user import main as user_root

from .database import db
from .models import *
from .settings import settings

db.connect()
db.create_tables([User, Admin, LoginToken, MailConfig, ResetPasswordToken])
db.close()

app = FastAPI(title = settings.app_name,)

app.mount("/api", user_root.app)
app.mount("/admin", admin_root.app)