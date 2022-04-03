from flask import Blueprint
import flask

health_blueprint = Blueprint('health', __name__)


@health_blueprint .route('/api/health', methods=['GET'])
def health():
    return flask.jsonify({'healthy': True}), 200
