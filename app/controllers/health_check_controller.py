from flask import Blueprint, jsonify

health_check_blueprint = Blueprint('health_check', __name__, url_prefix='/api')


@health_check_blueprint.route('/beat', methods=['GET'])
def heart_beat():
    ret = {"sample return": 10}
    return jsonify(ret), 200
