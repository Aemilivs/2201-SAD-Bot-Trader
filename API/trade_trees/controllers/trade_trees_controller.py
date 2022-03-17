from flask import Blueprint
from kink import inject
from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
import flask

trade_trees_blueprint = Blueprint('trade_tree', __name__)

@inject
def read_value(trade_tree_repository: TradeTreeRepository):
    return trade_tree_repository.get_trade_tree(1)

@trade_trees_blueprint.route('/api/trade_tree', methods=['GET'])
def get_trade_tree():
    return flask.jsonify({'result': read_value().id}), 200