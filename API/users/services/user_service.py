from kink import inject

from API.users.dbo.user import User


@inject
class UserService():
    def __init__(self, configuration, user_repository):
        self.configuration = configuration
        self.repository = user_repository

    def post_user(self, user: User):
        return self.repository.create_user(user)

    def get_user(self, username):
        return self.repository.read_user(username)

    def put_user(self, user: User):
        return self.repository.update_user(user)

    def delete_user(self, username):
        return self.repository.delete_user(username)
