from flask_httpauth import HTTPBasicAuth
from API.users.services.user_service import UserService
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()

# USER_DATA = {
#     "username": "password"
# }


@auth.verify_password
def authenticate(username, password):
    user = UserService.get_user(username)

    if user is not None:
        if check_password_hash(user.password, password):
            return user
    return None
