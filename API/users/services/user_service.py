from kink import inject

from API.users.dbo.user import User
from playhouse.shortcuts import model_to_dict

@inject
class UserService():
    def __init__(self, configuration, user_repository):
        self.configuration = configuration
        self.repository = user_repository

    def post_user(self, user: User):
        raw = self.repository.create_user(user)
        return model_to_dict(raw, backrefs=True)

    def get_user(self, username):
        return self.repository.read_user(username)

    def put_user(self, user: User):
        return self.repository.update_user(user)

    def delete_user(self, username):
        return self.repository.delete_user(username)
