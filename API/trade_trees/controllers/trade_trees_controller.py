from flask import Blueprint, request
import flask
from kink import inject
from schema import SchemaError
from api.trade_trees.controllers.validation.trade_tree_validator import TradeTreeValidator
from api.trade_trees.services.trade_tree_service import TradeTreeService
from api.trade_trees.dto.trade_tree_parser import TradeTreeParser


# Design notes:
# Layer purposed for handling communication between client and api.
@inject
class TradeTreesController():
    def __init__(self, trade_tree_service: TradeTreeService):
        self.service = trade_tree_service
        self.blueprint = self.define_routes()
        self.parser = TradeTreeParser()
        self.validator = TradeTreeValidator()

    def define_routes(self):
        blueprint = Blueprint('trade_tree', __name__)

        @blueprint.route('/api/trade_tree/initialize', methods=['GET'])
        def initialize_trade_tree_table():
            self.service.initialize_trade_tree_table()
            return flask.jsonify({"result": True}), 200

        @blueprint.route('/api/trade_tree/<id>', methods=['GET'])
        def get_trade_tree(id):
            # TODO: Introduce authorization.
            result = self.service.get_trade_tree(id)
            return flask.jsonify(result), 200

        @blueprint.route('/api/trade_tree', methods=['POST'])
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

            result = self.service.post_trade_tree(tree)
            return flask.jsonify(result), 201

        @blueprint.route('/api/trade_tree', methods=['PUT'])
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
            result = self.service.put_trade_tree(tree)
            return flask.jsonify(result), 204

        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        def delete_trade_tree(id):
            # TODO: Introduce authorization.

            result = self.service.delete_trade_tree(id)
            return flask.jsonify(result=result), 200

        @blueprint.route('/api/trade_tree/evaluate/<id>', methods=['GET'])
        def evaluate_trade_tree(id):
            # TODO: Introduce authorization.
            result = self.service.evaluate_trade_tree(id)
            return flask.jsonify(result=result), 200

        return blueprint
