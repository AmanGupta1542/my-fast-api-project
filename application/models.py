from datetime import datetime
from h11 import Data
import peewee
from .database import db

class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    isActive = peewee.BooleanField(default=False)
    role = peewee.BooleanField()
    accessType = peewee.IntegerField()
    createdAt = peewee.DateTimeField(default=datetime.now())
    class Meta:
        database = db

class LoginToken(peewee.Model):
    owner = peewee.ForeignKeyField(User,on_delete="CASCADE", backref="token")
    token = peewee.CharField(index=True)
    createdAt = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = db
    
class ResetPasswordToken(peewee.Model):
    owner = peewee.ForeignKeyField(User, on_delete="CASCADE")
    token = peewee.CharField(index=True)
    createdAt = peewee.DateTimeField(default=datetime.now())
    isExpire = peewee.BooleanField(default=False)

    class Meta:
        database = db

class MailConfig(peewee.Model):
    username= peewee.CharField()
    password= peewee.CharField()
    fromEmail = peewee.CharField()
    port= peewee.IntegerField()
    server= peewee.CharField()
    tls= peewee.BooleanField()
    ssl= peewee.BooleanField()
    use_credentials = peewee.BooleanField()
    validate_certs = peewee.BooleanField()
    class Meta:
        database = db