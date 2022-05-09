from flask_httpauth import HTTPBasicAuth
from API.users.services.user_service import UserService
from werkzeug.security import check_password_hash
from playhouse.shortcuts import model_to_dict
auth = HTTPBasicAuth()

# USER_DATA = {
#     "username": "password"
# }


@auth.verify_password
def authenticate(username, password):
    result = UserService().get_user(username)
    if len(result) > 0:
        if check_password_hash(result[0].password, password):
            return result
    return None
