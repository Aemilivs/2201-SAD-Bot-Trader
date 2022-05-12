from flask_httpauth import HTTPBasicAuth
from API.users.services.user_service import UserService
from werkzeug.security import check_password_hash
from playhouse.shortcuts import model_to_dict
auth = HTTPBasicAuth()

# USER_DATA = {
#     "username": "password"
# }


def get_auth():
    return auth.get_auth()


@auth.verify_password
def authenticate(username, password):
    user = UserService().get_user(username)

    if user is not None:
        if check_password_hash(user.password_hash, password):
            return user.name
    return None
