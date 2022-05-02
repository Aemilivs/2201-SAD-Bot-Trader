import uuid
from peewee import UUIDField, TimestampField, CharField, BooleanField, ForeignKeyField, IntegerField, BooleanField, TextField
from API.common.db_schema import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(max_length=100, null=False, index=False)
    pwd_hash = CharField(max_length=100, null=False, index=False)
    isActive = BooleanField(null=False, index=False)
    createdAt = TimestampField(null=False, index=False)
    updatedAt = TimestampField(null=False, index=False)

    def hash_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
