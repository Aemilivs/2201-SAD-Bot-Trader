from datetime import datetime
from kink import inject

from API.users.dbo.user import User


@inject()
class TradeTreeRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        self.db.connect()
        # TODO: Eventually come up with a resolution of whether we should call
        # it or not.
        self.db.create_tables(
            [User])

    def create_user(self, user: User):
        return User.create(
            id = user.id,
            name = user.name,
            password = user.password,
            isActive = True,
            createdAt = datetime.utcnow(),
            updatedAt = datetime.utcnow()
        )

    def read_user(self, username):
        return User.select().where(User.username == username)

