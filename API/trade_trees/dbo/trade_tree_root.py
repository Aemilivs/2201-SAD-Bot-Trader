from peewee import PrimaryKeyField, TimestampField
from ...common.db_schema import BaseModel

# Design notes:
# Layer purposed for definiton of an object representation in the database.
class TradeTreeRoot(BaseModel):
    id = PrimaryKeyField()
    createdAt = TimestampField(null=False, index=False)
    updatedAt = TimestampField(null=False, index=False)