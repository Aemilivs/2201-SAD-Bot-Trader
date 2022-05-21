"""This module is the main runtime of the SAD Bot Trader API"""
from flask import Flask
from flask_restful import Api
from apiflask import APIFlask
import os
from .health.controllers.health_controller import health_blueprint
from .trade_trees.controllers.trade_trees_controller import TradeTreesController
from .users.controllers.users_controller import UsersController


app = APIFlask(__name__, title='Bot Trader API', version='1.0')
app.config["DEBUG"] = True
app.config['SPEC_FORMAT'] = 'json'
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
app.register_blueprint(health_blueprint)
# pylint: disable=no-value-for-parameter
app.register_blueprint(TradeTreesController().blueprint)
app.register_blueprint(UsersController().blueprint)

if __name__ == "__main__":
    Api(app.run())
