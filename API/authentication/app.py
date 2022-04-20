from flask import Flask, jsonify
from flask_restful import Api
from my_resource import PrivateResource
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()

#TODO: Create database
#TODO: Only store Hashes instead of plain text passwords
USER_DATA = {
    "username": "password"
}


@auth.verify_password
def verify_password(username, password):
    if username in USER_DATA and \
            USER_DATA.get(username) == password:
        return username


# add all resources here
api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
