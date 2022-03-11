from kink import inject
from peewee import Model, SqliteDatabase

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('DatabaseName')
