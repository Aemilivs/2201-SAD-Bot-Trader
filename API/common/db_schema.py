from kink import di, inject
from peewee import Model, SqliteDatabase

class BaseModel(Model):
    class Meta:
        database = di['db']
