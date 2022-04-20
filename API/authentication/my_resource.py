from flask import jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

USER_DATA = {
    "username": "password"
}


class PrivateResource(Resource):
    def get(self):
        if auth.current_user() in USER_DATA:
            return jsonify({"status": True})
