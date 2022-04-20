from flask import Flask
from flask_restful import Api
from my_resource import PrivateResource
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()

USER_DATA = {
    "Username": "password"
}


@auth.verify_password
def verify_password(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

# add all resources here
api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
