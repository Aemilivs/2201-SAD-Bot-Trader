import kink
from peewee import Model, SqliteDatabase


class BaseModel(Model):
    class Meta:
        database = kink.di['db']
