from datetime import datetime
import uuid
from flask import Blueprint, abort, request
import flask
from kink import inject
from playhouse.shortcuts import model_to_dict
from trade_trees.services.trade_tree_service import TradeTreeService
from trade_trees.dto.trade_tree_parser import TradeTreeParser


# Design notes:
# Layer purposed for handling communication between client and API.
class TradeTreesController():
    @inject
    def __init__(self, trade_tree_service: TradeTreeService):
        self.service = trade_tree_service
        self.blueprint = self.define_routes()
        self.parser = TradeTreeParser()

    def define_routes(self):
        blueprint = Blueprint('trade_tree', __name__)

        @blueprint.route('/api/trade_tree/initialize', methods=['GET'])
        def initialize_trade_tree_table():
            self.service.initialize_trade_tree_table()
            return flask.jsonify({"result": True}), 200
        
        @blueprint.route('/api/trade_tree/<id>', methods=['GET'])
        def get_trade_tree(id):
            # TODO: Introduce validation.
            # TODO: Introduce authorization.
            result = self.service.get_trade_tree(id)
            return flask.jsonify(result), 200
        
        @blueprint.route('/api/trade_tree', methods=['POST'])
        def post_trade_tree():
            # TODO: Introduce authorization.
            # TODO: Introduce validation.
            # TODO: Introduce a mapping of DTO into DBO in order to decouple database definition from a user contract.
            tree = self.parser.parse_args()
            result = self.service.post_trade_tree(tree)
            return flask.jsonify(result), 201

        @blueprint.route('/api/trade_tree', methods=['PUT'])
        def put_trade_tree():
            # TODO: Introduce authorization.
            # TODO: Introduce validation.
            # TODO: Introduce a mapping of DTO into DBO in order to decouple database definition from a user contract.
            tree = self.parser.parse_args()
            result = self.service.put_trade_tree(tree)
            return flask.jsonify(result), 204
        
        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        def delete_trade_tree(id):
            # TODO: Introduce authorization.
            # TODO: Introduce validation.

            result = self.service.delete_trade_tree(id)
            return flask.jsonify(result=result), 200

        return blueprint
