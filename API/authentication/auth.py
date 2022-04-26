from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

# TODO: Create database
# TODO: Only store Hashes instead of plain text passwords
USER_DATA = {
    "username": "password"
}


@auth.verify_password
def verify_password(username, password):
    if username in USER_DATA and \
            USER_DATA.get(username) == password:
        return username
