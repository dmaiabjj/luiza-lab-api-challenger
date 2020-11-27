from flask import jsonify

from app.controllers.site.authentication_controller import authentication_site_blueprint
from app.controllers.site.customer_controller import customer_site_blueprint

from app.controllers.admin.authentication_controller import authentication_admin_blueprint
from app.controllers.admin.user_controller import user_admin_blueprint
from app.controllers.admin.customer_controller import customer_admin_blueprint
from ..presentation.base_response_exception import NotFoundException, BadRequestException, UnauthorizedException, \
    ResourceAlreadyExistsException, BaseResponseException


@authentication_site_blueprint.errorhandler(NotFoundException)
@authentication_admin_blueprint.errorhandler(NotFoundException)
@customer_admin_blueprint.errorhandler(NotFoundException)
@customer_site_blueprint.errorhandler(NotFoundException)
@user_admin_blueprint.errorhandler(NotFoundException)
def handle_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_site_blueprint.errorhandler(BadRequestException)
@authentication_admin_blueprint.errorhandler(BadRequestException)
@customer_admin_blueprint.errorhandler(BadRequestException)
@customer_site_blueprint.errorhandler(BadRequestException)
@user_admin_blueprint.errorhandler(BadRequestException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_site_blueprint.errorhandler(UnauthorizedException)
@authentication_admin_blueprint.errorhandler(UnauthorizedException)
@customer_admin_blueprint.errorhandler(UnauthorizedException)
@customer_site_blueprint.errorhandler(UnauthorizedException)
@user_admin_blueprint.errorhandler(UnauthorizedException)
def handle_unauthorized_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_site_blueprint.errorhandler(ResourceAlreadyExistsException)
@authentication_admin_blueprint.errorhandler(ResourceAlreadyExistsException)
@customer_admin_blueprint.errorhandler(ResourceAlreadyExistsException)
@customer_site_blueprint.errorhandler(ResourceAlreadyExistsException)
@user_admin_blueprint.errorhandler(ResourceAlreadyExistsException)
def handle_conflict_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@authentication_site_blueprint.errorhandler(500)
@authentication_admin_blueprint.errorhandler(500)
@customer_admin_blueprint.errorhandler(500)
@customer_site_blueprint.errorhandler(500)
@user_admin_blueprint.errorhandler(500)
def handle_server_error_request(error):
    response = jsonify(BaseResponseException(payload=error.message, message="An unexpected error happened sorry"))
    response.status_code = error.status_code
    return response
