from operator import index
import uuid
from peewee import UUIDField, TimestampField, CharField, BooleanField, ForeignKeyField, IntegerField, BooleanField, TextField
from API.common.db_schema import BaseModel

# Design notes:
# Layer purposed for definiton of an object representation in the database.
# TODO Introduce a valid child/branch hierarchy to the root.


class TradeTreeRoot(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    title = CharField(max_length=100, null=False, index=False)
    isActive = BooleanField(null=False, index=False)
    createdAt = TimestampField(null=False, index=False)
    updatedAt = TimestampField(null=False, index=False)

# TODO Introduce a separated class for schema branches.
# class TradeTreeSchemaDiscriminator(BaseModel):
#     id = UUIDField(primary_key=True, default=uuid.uuid4)
#     schemaPath = TextField(null=False, index=False)


class TradeTreeBranch(BaseModel):
    id = UUIDField(primary_key=True)
    discriminator = CharField(max_length=10)
    parent = ForeignKeyField('self', backref='children', null=True)
    # TODO Make root an indexed field to optimize branch building process.
    root = ForeignKeyField(TradeTreeRoot, backref='root')
    schema_path = CharField(max_length=100, null=True)
    operation = CharField(max_length=100, null=True)
    discriminant = CharField(max_length=100, null=True)


class TradeTreeOutcome(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    operation = CharField(max_length=25)
    operand = IntegerField()
    target = TextField()
    root = ForeignKeyField(TradeTreeRoot)
