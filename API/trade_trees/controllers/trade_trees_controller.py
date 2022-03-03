from flask import Blueprint
import flask

trade_trees_blueprint = Blueprint('trade_tree', __name__)

@trade_trees_blueprint.route('/api/trade_tree', methods=['GET'])
def get_trade_tree():
    return flask.jsonify({}), 200