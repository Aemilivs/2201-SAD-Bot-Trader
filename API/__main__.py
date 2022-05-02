"""This module is the main runtime of the SAD Bot Trader API"""
from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from .health.controllers.health_controller import health_blueprint
from .trade_trees.controllers.trade_trees_controller import TradeTreesController

auth = HTTPBasicAuth()
app = Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(health_blueprint)
# pylint: disable=no-value-for-parameter
app.register_blueprint(TradeTreesController().blueprint)


# TODO: Only store Hashes instead of plain text passwords
# TODO: Add endpoint to create new users, might be done with blue prints
@app.route('/create-user')
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == "__main__":
    Api(app.run())
