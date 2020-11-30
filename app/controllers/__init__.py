from flask import jsonify

from app.controllers.authentication_controller import authentication_blueprint
from app.controllers.user_controller import user_blueprint
from app.controllers.customer_controller import customer_blueprint
from app.controllers.product_controller import product_blueprint
from app.controllers.wishlist_controller import wishlist_blueprint

from ..presentation.base_response_exception import NotFoundException, BadRequestException, UnauthorizedException, \
    ResourceAlreadyExistsException, BaseResponseException


@authentication_blueprint.errorhandler(NotFoundException)
@user_blueprint.errorhandler(NotFoundException)
@customer_blueprint.errorhandler(NotFoundException)
@product_blueprint.errorhandler(NotFoundException)
@wishlist_blueprint.errorhandler(NotFoundException)
def handle_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_blueprint.errorhandler(BadRequestException)
@user_blueprint.errorhandler(BadRequestException)
@customer_blueprint.errorhandler(BadRequestException)
@product_blueprint.errorhandler(BadRequestException)
@wishlist_blueprint.errorhandler(BadRequestException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_blueprint.errorhandler(UnauthorizedException)
@user_blueprint.errorhandler(UnauthorizedException)
@customer_blueprint.errorhandler(UnauthorizedException)
@product_blueprint.errorhandler(UnauthorizedException)
@wishlist_blueprint.errorhandler(UnauthorizedException)
def handle_unauthorized_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_blueprint.errorhandler(ResourceAlreadyExistsException)
@user_blueprint.errorhandler(ResourceAlreadyExistsException)
@customer_blueprint.errorhandler(ResourceAlreadyExistsException)
@product_blueprint.errorhandler(ResourceAlreadyExistsException)
@wishlist_blueprint.errorhandler(ResourceAlreadyExistsException)
def handle_conflict_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_blueprint.errorhandler(500)
@user_blueprint.errorhandler(500)
@customer_blueprint.errorhandler(500)
@product_blueprint.errorhandler(500)
@wishlist_blueprint.errorhandler(500)
def handle_server_error_request(error):
    response = jsonify(BaseResponseException(payload=error.message, message="An unexpected error happened sorry"))
    response.status_code = error.status_code
    return response
