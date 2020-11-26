from flask import jsonify

from .customer import customer_blueprint
from ..presentation.base_response_exception import NotFoundException, BadRequestException


@customer_blueprint.errorhandler(NotFoundException)
def handle_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(BadRequestException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
