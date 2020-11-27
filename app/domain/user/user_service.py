from app.presentation.base_response_exception import ResourceAlreadyExistsException, NotFoundException, \
    UnauthorizedException, BadRequestException

NOT_FOUND_EXCEPTION = NotFoundException(message="User not found")
UNAUTHORIZED_EXCEPTION = UnauthorizedException(message="User not authorized")
RESOURCE_ALREADY_EXISTS_EXCEPTION = ResourceAlreadyExistsException(message="Email already in use")
BAD_REQUEST_EXCEPTION = BadRequestException(message="Password mismatch")


class UserService:
    def __init__(self, repository):
        self.__repository = repository

    def add(self, user):
        user_already_exists = self.__repository.find_by_email(user.email)
        if user_already_exists:
            raise RESOURCE_ALREADY_EXISTS_EXCEPTION

        user = self.__repository.add(user)

        return user.to_dict()

    def update(self, user_updated):
        user = self.__repository.find_by_id(id=user_updated.id)
        if user is None:
            raise NOT_FOUND_EXCEPTION

        customer_exists = self.__repository.find_by_email(user_updated.email)
        if customer_exists and customer_exists.id != user_updated.id:
            raise RESOURCE_ALREADY_EXISTS_EXCEPTION

        self.__repository.update_from_model(user, user_updated)

        return user.to_dict()

    def delete(self, id):
        user = self.__repository.find_by_id(id=id)
        if user is None:
            raise NOT_FOUND_EXCEPTION

        self.__repository.delete(user)

    def find_by_id(self, id):
        user = self.__repository.find_by_id(id=id)
        if user is None:
            raise NOT_FOUND_EXCEPTION

        return user.to_dict()

    def find_by_email(self, email):
        user = self.__repository.find_by_email(email=email)
        if user is None:
            raise NOT_FOUND_EXCEPTION

        return user.to_dict()

    def get_all_paginated(self, offset=1, limit=10):
        users = self.__repository.get_all_paginated(offset=offset - 1, limit=limit)
        return list(map(lambda user: user.to_dict(), users))

    def login(self, email, password):
        user = self.__repository.find_by_email(email)

        if user is None:
            raise NOT_FOUND_EXCEPTION
        elif not user.verify_password(password):
            raise UNAUTHORIZED_EXCEPTION

        return user.to_dict()

    def change_password(self, user_updated, password):

        user = self.__repository.find_by_id(user_updated.id)

        if user is None:
            raise NOT_FOUND_EXCEPTION
        elif not user.verify_password(password):
            raise BAD_REQUEST_EXCEPTION

        self.__repository.update_from_model(user, user_updated)

        return user.to_dict()
