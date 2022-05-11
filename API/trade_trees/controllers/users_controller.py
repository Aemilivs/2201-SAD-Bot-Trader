from flask import Blueprint, request
import flask
from kink import inject
from API.users.services.user_service import UserService


@inject
class UsersController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.blueprint = self.define_routes()

    def define_routes(self):
        blueprint = Blueprint('users', __name__)

        @blueprint.route('/api/create-user', methods=['POST'])
        def post_new_user():
            payload = request.json
            self.user_service.post_user(payload)
            # return flask.jsonify(result=response), 200
            return flask.jsonify(result=True), 204

        return blueprint
