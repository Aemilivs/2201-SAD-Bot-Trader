from flask import request
import flask
from apiflask import APIBlueprint, abort
from marshmallow import ValidationError
from API.authentication.auth import auth
from kink import inject
from schema import SchemaError
from API.trade_trees.controllers.schemas.schemas import *
from API.trade_trees.controllers.validation.trade_tree_validator import TradeTreeValidator
from API.trade_trees.services.trade_tree_service import TradeTreeService
from API.trade_trees.dto.trade_tree_parser import TradeTreeParser
from API.trade_trees.controllers.schemas.examples import post_trade_tree_example
from API.users.services.user_service import UserService


# Design notes:
# Layer purposed for handling communication between client and API.


@inject
class TradeTreesController():
    def __init__(
            self,
            trade_tree_service: TradeTreeService,
            user_service: UserService):
        self.tree_service = trade_tree_service
        self.user_service = user_service
        self.blueprint = self.define_routes()
        self.parser = TradeTreeParser()
        self.validator = TradeTreeValidator()

    def define_routes(self):
        blueprint = APIBlueprint('trade_tree', __name__)

        @blueprint.route('/api/trade_tree/initialize', methods=['GET'])
        @blueprint.output(InitializeTradeTreeTableAPISchema, status_code=200, description='Initialize the database.')
        @blueprint.doc(hide=True)
        @auth.login_required
        def initialize_trade_tree_table():
            """
            Initialize the database.

            Hidden endpoint.
            """
            # self.tree_service.initialize_trade_tree_table()
            return flask.jsonify({"result": True}), 200

        @blueprint.route('/api/trade_tree/<id>', methods=['GET'])
        @blueprint.doc(responses=[200,400])
        @blueprint.output(GetTradeTreeAPIOutSchemaSuccess, status_code=200)
        @blueprint.auth_required(auth)
        @auth.login_required
        def get_trade_tree(id):
            """
            Fetch a trade tree by it's id.

            If user does not own the tree - response has code 401 and a corresponding error message.
            """
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id

            result = self.tree_service.get_trade_tree(id, user_id)
            return flask.jsonify(result)
            

        @blueprint.route('/api/trade_tree/user', methods=['GET'])
        @blueprint.doc(responses=[200,400])
        @blueprint.output(GetUserTradeTreeAPIOutSchemaSuccess, status_code=200)
        @blueprint.auth_required(auth)
        @auth.login_required
        def get_user_trade_trees():
            """
            Fetch trade trees that current user owns.
            """
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id

            result = self.tree_service.get_user_trade_trees(user_id)
            return flask.jsonify(result)

        @blueprint.route('/api/trade_tree', methods=['POST'])
        @blueprint.doc(responses=[201,400])
        @blueprint.auth_required(auth)
        @blueprint.input(PostTradeTreeAPIInSchemaSuccess)
        @blueprint.output(PostTradeTreeAPIOutSchemaSuccess, example=post_trade_tree_example, status_code=201)
        @auth.login_required
        def post_trade_tree(payload):
            """
            Create a new trade tree for the current user.
            """
            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                abort(400, exception.code)

            tree = self.parser.parse_args()

            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            tree.user_id = user_id
            result = self.tree_service.post_trade_tree(tree)
            return flask.jsonify(result)

        @blueprint.route('/api/trade_tree', methods=['PUT'])
        @blueprint.doc(responses=[200,400,404])
        @blueprint.auth_required(auth)
        @blueprint.input(PutTradeTreeAPIInSchemaSuccess)
        @blueprint.output(PutTradeTreeAPIOutSchemaSuccess, status_code=200)
        @auth.login_required
        def put_trade_tree(payload):
            """
            Update a trade tree that the current user owns.

            If user does not own the tree - response has code 401 and a corresponding error message.
            """
            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                abort(400, exception.code)

            tree = self.parser.parse_args()
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            tree.user_id = user_id

            result = self.tree_service.put_trade_tree(tree)
            return flask.jsonify(result)
            

        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        @blueprint.doc(responses=[200,400])
        @blueprint.output(DeleteTradeTreeAPIOutSchemaSuccess, status_code=200)
        @blueprint.auth_required(auth)
        @auth.login_required
        def delete_trade_tree(id):
            """
            Remove a trade tree by it's id.

            If user does not own the tree - response has code 401 and a corresponding error message.
            """
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id

            result = self.tree_service.delete_trade_tree(id, user_id)
            return flask.jsonify(result=result)

        @blueprint.route('/api/trade_tree/evaluate/<id>', methods=['GET'])
        @blueprint.doc(responses=[200,400])
        @blueprint.output(EvaluateTradeTreeAPIOutSchemaSuccess, status_code=200)
        @blueprint.auth_required(auth)
        @auth.login_required
        def evaluate_trade_tree(id):
            """
            Evaluate a trade tree by it's id.

            If user does not own the tree - response has code 401 and a corresponding error message.
            """
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id

            result = self.tree_service.evaluate_trade_tree(id, user_id)
            return flask.jsonify(result=result)

        return blueprint
