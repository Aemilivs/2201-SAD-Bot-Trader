from flask import jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        return jsonify({"status": True})
