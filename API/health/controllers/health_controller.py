from apiflask import APIBlueprint
import flask
from API.authentication.auth import auth

health_blueprint = APIBlueprint('health', __name__)

@health_blueprint.route('/api/health', methods=['GET'])
@auth.login_required
def health():
    return flask.jsonify({'healthy': True}), 200
