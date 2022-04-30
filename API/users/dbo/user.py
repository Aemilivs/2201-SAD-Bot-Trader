import uuid
from peewee import UUIDField, TimestampField, CharField, BooleanField, ForeignKeyField, IntegerField, BooleanField, TextField
from API.common.db_schema import BaseModel


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(max_length=100, null=False, index=False)
    password = CharField(max_length=100, null=False, index=False)
    isActive = BooleanField(null=False, index=False)
    createdAt = TimestampField(null=False, index=False)
    updatedAt = TimestampField(null=False, index=False)