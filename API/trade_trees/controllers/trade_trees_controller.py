from flask import Blueprint, abort, request
from kink import inject
from playhouse.shortcuts import model_to_dict
import flask

from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO
from API.trade_trees.services.trade_tree_service import TradeTreeService

# Design notes:
# Layer purposed for handling communication between client and API.
class TradeTreesController():
    @inject
    def __init__(self, trade_tree_service: TradeTreeService):
        self.service = trade_tree_service
        self.blueprint = self.define_routes()

    def define_routes(self):
        blueprint = Blueprint('trade_tree', __name__)
        
        @blueprint.route('/api/trade_tree/<id>', methods=['GET'])
        def get_trade_tree(id):
            # TODO: Introduce validation.
            # TODO: Introduce authorization.
            result = self.service.get_trade_tree(id)

            if (len(result) < 1):
                # TODO: Replace with a proper method designed for API response 
                return abort(404)

            raw = model_to_dict(result[0])
            return flask.jsonify(raw), 200
        
        @blueprint.route('/api/trade_tree', methods=['POST'])
        def post_trade_tree():
            # TODO: Introduce authorization.
            # TODO: Introduce validation.
            result = self.service.post_trade_tree(TradeTreeRootDTO())

            return flask.jsonify({"result": result}), 200

        @blueprint.route('/api/trade_tree', methods=['PUT'])
        def put_trade_tree():
            # TODO: Introduce authorization.
            # TODO: Introduce validation.
            payload = request.get_json()

            self.service.put_trade_tree(TradeTreeRootDTO(payload['id']))
            return flask.jsonify({"result": True}), 200
        
        @blueprint.route('/api/trade_tree/<id>', methods=['DELETE'])
        def delete_trade_tree(id):
            # TODO: Introduce authorization.
            # TODO: Introduce validation.

            self.service.delete_trade_tree(id)
            return flask.jsonify({"result": True}), 200

        return blueprint
