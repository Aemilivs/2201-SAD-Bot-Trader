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
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            
            try:
                result = self.tree_service.get_trade_tree(id, user_id)
                return flask.jsonify(result), 200
            except Exception as exception:
                return flask.jsonify(error_message=exception.data['message']), exception.code
            

        @blueprint.route('/api/trade_tree', methods=['POST'])
        @auth.login_required
        def post_trade_tree():
            payload = request.json

            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                result = {
                    "error_message": exception.code
                }
                return flask.jsonify(result), 400

            tree = self.parser.parse_args()

            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            tree.user_id = user_id
            try:
                result = self.tree_service.post_trade_tree(tree)
                return flask.jsonify(result), 201
            except Exception as exception:
                return flask.jsonify(error_message=exception.data['message']), exception.code

        @blueprint.route('/api/trade_tree', methods=['PUT'])
        @auth.login_required
        def put_trade_tree():
            payload = request.json

            try:
                self.validator.validate(payload)
            except SchemaError as exception:
                result = {
                    "error_message": exception.code
                }
                return flask.jsonify(result), 400

            tree = self.parser.parse_args()
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            tree.user_id = user_id
            
            try:
                result = self.tree_service.put_trade_tree(tree)
                return flask.jsonify(result), 200
            except Exception as exception:
                return flask.jsonify(error_message=exception.data['message']), exception.code

        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        @auth.login_required
        def delete_trade_tree(id):
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            
            try:
                result = self.tree_service.delete_trade_tree(id, user_id)
                return flask.jsonify(result=result), 200
            except Exception as exception:
                return flask.jsonify(error_message=exception.data['message']), exception.code
            
        @blueprint.route('/api/trade_tree/evaluate/<id>', methods=['GET'])
        @auth.login_required
        def evaluate_trade_tree(id):
            username = auth.get_auth().username
            user_id = self.user_service.get_user(username).id
            
            try:
                result = self.tree_service.evaluate_trade_tree(id, user_id)
                return flask.jsonify(result=result), 200
            except Exception as exception:
                return flask.jsonify(error_message=exception.data['message']), exception.code

        return blueprint
