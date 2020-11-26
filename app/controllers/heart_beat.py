from flask import Blueprint

api_blueprint = Blueprint(name='api', import_name=__name__)


@api_blueprint.route('/heart-beat', methods=['GET'])
def heart_beat():
    return 'Hello, World!'
