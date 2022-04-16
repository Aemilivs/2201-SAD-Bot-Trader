from kink import di
from peewee import Model


class BaseModel(Model):
    class Meta:
        database = di['db']
