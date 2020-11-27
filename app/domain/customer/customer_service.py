from app.presentation.base_response_exception import ResourceAlreadyExistsException, NotFoundException, \
    UnauthorizedException, BadRequestException

NOT_FOUND_EXCEPTION = NotFoundException(message="Customer not found")
UNAUTHORIZED_EXCEPTION = UnauthorizedException(message="Customer not authorized")
RESOURCE_ALREADY_EXISTS_EXCEPTION = ResourceAlreadyExistsException(message="Email already in use")
BAD_REQUEST_EXCEPTION = BadRequestException(message="Password mismatch")


class CustomerService:
    def __init__(self, repository):
        self.__repository = repository

    def add(self, customer):
        customer_already_exists = self.__repository.find_by_email(customer.email)
        if customer_already_exists:
            raise RESOURCE_ALREADY_EXISTS_EXCEPTION

        customer = self.__repository.add(customer)

        return customer.to_dict()

    def update(self, customer_updated):
        customer = self.__repository.find_by_id(id=customer_updated['id'])
        if customer is None:
            raise NOT_FOUND_EXCEPTION

        customer_exists = self.__repository.find_by_email(customer_updated['email'])
        if customer_exists and customer_exists.id != customer_updated['id']:
            raise RESOURCE_ALREADY_EXISTS_EXCEPTION

        self.__repository.update_from_dict(customer, customer_updated)

        return customer.to_dict()

    def delete(self, id):
        customer = self.__repository.find_by_id(id=id)
        if customer is None:
            raise NOT_FOUND_EXCEPTION

        self.__repository.delete(customer)

    def find_by_id(self, id):
        customer = self.__repository.find_by_id(id=id)
        if customer is None:
            raise NOT_FOUND_EXCEPTION

        return customer.to_dict()

    def find_by_email(self, email):
        customer = self.__repository.find_by_email(email=email)
        if customer is None:
            raise NOT_FOUND_EXCEPTION

        return customer.to_dict()

    def get_all_paginated(self, offset=1, limit=10):
        customers = self.__repository.get_all_paginated(offset=offset - 1, limit=limit)
        return list(map(lambda customer: customer.to_dict(), customers))

    def login(self, email, password):
        customer = self.__repository.find_by_email(email)

        if customer is None:
            raise NOT_FOUND_EXCEPTION
        elif not customer.verify_password(password):
            raise UNAUTHORIZED_EXCEPTION

        return customer.to_dict()

    def change_password(self, customer_updated, password):

        customer = self.__repository.find_by_id(customer_updated.id)

        if customer is None:
            raise NOT_FOUND_EXCEPTION
        elif not customer.verify_password(password):
            raise BAD_REQUEST_EXCEPTION

        self.__repository.update_from_model(customer, customer_updated)

        return customer.to_dict()
