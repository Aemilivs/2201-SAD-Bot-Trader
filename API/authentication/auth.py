from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()

# USER_DATA = {
#     "username": "password"
# }


@auth.verify_password
def authenticate(self, username, password):
    user = self.user_service.get_user(username)

    if user is not None:
        if check_password_hash(user.password, password):
            return user
    return None
