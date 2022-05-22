from apiflask import Schema
from apiflask.fields import String, Date, Boolean, UUID, List, Nested
from apiflask.validators import Length, OneOf

class CreateUserTradeTreeAPISchema(Schema):
    name = String()
    password = String() 