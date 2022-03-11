from flask import Blueprint
from kink import inject
from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO
import flask

trade_trees_blueprint = Blueprint('trade_tree', __name__)

@inject
def initialize_database_via_repo(trade_tree_repository: TradeTreeRepository):
    return trade_tree_repository.initialize_database()

@inject
def read_value(trade_tree_repository: TradeTreeRepository):
    return trade_tree_repository.get_trade_tree(1)

@inject
def write_value(trade_tree_repository: TradeTreeRepository):
    dto = TradeTreeRootDTO(1)
    return trade_tree_repository.post_trade_tree(dto)

@trade_trees_blueprint.route('/api/trade_tree', methods=['GET'])
def get_trade_tree():
    return flask.jsonify({'result': len(read_value())}), 200

@trade_trees_blueprint.route('/api/trade_tree/create', methods=['GET'])
def post_trade_tree():
    write_value()
    return flask.jsonify({'result': len(read_value())}), 200

@trade_trees_blueprint.route('/api/initialize', methods=['GET'])
def initialize_database():
    initialize_database_via_repo()
    return flask.jsonify({'result': read_value().id}), 200