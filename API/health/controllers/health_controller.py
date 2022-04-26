from flask import Blueprint
import flask
#from flask_httpauth import HTTPBasicAuth
from API.authentication.app import auth

health_blueprint = Blueprint('health', __name__)
#auth = HTTPBasicAuth()

# USER_DATA = {
#     "username": "password"
# }
#
#
# @auth.verify_password
# def verify_password(username, password):
#     if username in USER_DATA and \
#             USER_DATA.get(username) == password:
#         return username


@health_blueprint.route('/api/health', methods=['GET'])
@auth.login_required
def health():
    return flask.jsonify({'healthy': True}), 200
