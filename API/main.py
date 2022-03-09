from flask import Flask
from .health.controllers.health_controller import health_blueprint
from .trade_trees.controllers.trade_trees_controller import trade_trees_blueprint

app = Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(health_blueprint)
app.register_blueprint(trade_trees_blueprint)

app.run()
