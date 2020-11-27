from flask import jsonify

from app.controllers.site.customer_controller import customer_blueprint
from app.controllers.site.customer_authentication_controller import customer_authentication_blueprint
from ..presentation.base_response_exception import NotFoundException, BadRequestException, UnauthorizedException, \
    ResourceAlreadyExistsException, BaseResponseException


@customer_blueprint.errorhandler(NotFoundException)
@customer_authentication_blueprint.errorhandler(NotFoundException)
def handle_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(BadRequestException)
@customer_authentication_blueprint.errorhandler(BadRequestException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(UnauthorizedException)
@customer_authentication_blueprint.errorhandler(UnauthorizedException)
def handle_unauthorized_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(ResourceAlreadyExistsException)
def handle_conflict_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(500)
@customer_authentication_blueprint.errorhandler(500)
def handle_server_error_request(error):
    response = jsonify(BaseResponseException(payload=error.message, message="An unexpected error happened sorry"))
    response.status_code = error.status_code
    return response
