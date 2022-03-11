from kink import inject
from peewee import Model, SqliteDatabase
import configparser

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('DatabaseName')
