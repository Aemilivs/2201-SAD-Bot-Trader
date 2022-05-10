from datetime import datetime
import uuid
from kink import inject
from werkzeug.security import generate_password_hash
from API.users.dbo.user import User


@inject
class UserRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        # The line below commented due to error
        # peewee.OperationalError: Connection already opened.
        # self.db.connect()
        # TODO: Eventually come up with a resolution of whether we should call
        # it or not.
        self.db.create_tables([User])

    def create_user(self, entity: User):
        return User.create(
            id=uuid.uuid4(),
            name=entity['name'],
            password_hash=generate_password_hash(entity['password']),
            isActive=True,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )

    def read_user(self, username):
        return User.select().where(User.name == username)

    def update_user(self, entity: User):
        return User.update(
            name=entity.name,
            isActive=entity.isActive,
            updatedAt=datetime.utcnow()
        ).where(entity.name == entity.name).execute()

    def delete_user(self, username):
        return User.delete().where(User.name == username).execute()
