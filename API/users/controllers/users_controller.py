from flask import request
from apiflask import APIBlueprint, abort
import flask
from kink import inject
from API.users.controllers.schemas.schemas import CreateUserTradeTreeAPISchema
from API.users.services.user_service import UserService


@inject
class UsersController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.blueprint = self.define_routes()

    def define_routes(self):
        blueprint = APIBlueprint('users', __name__)

        @blueprint.route('/api/create-user', methods=['POST'])
        @blueprint.doc(responses=[200, 201, 400])
        @blueprint.input(CreateUserTradeTreeAPISchema)
        def post_new_user(payload):
            """
            Create a new user.
            """
            try:
                self.user_service.post_user(payload)
            except Exception as exception:
                abort(exception.code, exception.data['message'])
            return flask.jsonify(result=True)

        return blueprint
