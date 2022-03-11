from peewee import PrimaryKeyField, DateField
from ...common.db_schema import BaseModel

class TradeTreeRoot(BaseModel):
    id = PrimaryKeyField()
    createdAt = DateField(null=False, index=False)
    updatedAt = DateField(null=False, index=False)