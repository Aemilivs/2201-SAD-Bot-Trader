from flask import Blueprint
import flask
from flask_httpauth import HTTPBasicAuth

health_blueprint = Blueprint('health', __name__)
auth = HTTPBasicAuth()


@health_blueprint.route('/api/health', methods=['GET'])
@auth.login_required
def health():
    return flask.jsonify({'healthy': True}), 200
