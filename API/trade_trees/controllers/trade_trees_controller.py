from flask import Blueprint, request
import flask
from API.authentication.auth import auth
from kink import inject
from schema import SchemaError
from API.trade_trees.controllers.validation.trade_tree_validator import TradeTreeValidator
from API.trade_trees.services.trade_tree_service import TradeTreeService
from API.trade_trees.dto.trade_tree_parser import TradeTreeParser
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
        blueprint = Blueprint('trade_tree', __name__)

        @blueprint.route('/api/trade_tree/initialize', methods=['GET'])
        @auth.login_required
        def initialize_trade_tree_table():
            self.tree_service.initialize_trade_tree_table()
            return flask.jsonify({"result": True}), 200

        @blueprint.route('/api/trade_tree/<id>', methods=['GET'])
        @auth.login_required
        def get_trade_tree(id):
            # TODO: Introduce authorization.
            result = self.tree_service.get_trade_tree(id)
            return flask.jsonify(result), 200

        @blueprint.route('/api/trade_tree', methods=['POST'])
        @auth.login_required
        def post_trade_tree():
            # TODO: Introduce authorization.
            payload = request.json

            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                result = {
                    "error_message": exception.code
                }
                return flask.jsonify(result), 400

            tree = self.parser.parse_args()

            result = self.tree_service.post_trade_tree(tree)
            return flask.jsonify(result), 201

        @blueprint.route('/api/trade_tree', methods=['PUT'])
        @auth.login_required
        def put_trade_tree():
            # TODO: Introduce authorization.
            payload = request.json

            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                result = {
                    "error_message": exception.code
                }
                return flask.jsonify(result), 400

            tree = self.parser.parse_args()
            result = self.tree_service.put_trade_tree(tree)
            return flask.jsonify(result), 204

        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        @auth.login_required
        def delete_trade_tree(id):
            result = self.tree_service.delete_trade_tree(id)
            return flask.jsonify(result=result), 200

        @blueprint.route('/api/trade_tree/evaluate/<id>', methods=['GET'])
        @auth.login_required
        def evaluate_trade_tree(id):
            # TODO: Introduce authorization.
            result = self.tree_service.evaluate_trade_tree(id)
            return flask.jsonify(result=result), 200

        @blueprint.route('/api/create-user', methods=['POST'])
        def post_new_user():
            payload = request.json
            # Todo: format data to be passed to database
            response = self.user_service.post_user(payload)
            # return flask.jsonify(result=response), 200
            return flask.jsonify(result=True), 204

        return blueprint
