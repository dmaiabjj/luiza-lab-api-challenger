import os

from app.infrastructure.magalu.repository.magalu_product_repository import MagaluProductListRepository
from app.presentation.base_response_exception import ResourceAlreadyExistsException, NotFoundException, \
    UnauthorizedException

NOT_FOUND_EXCEPTION = NotFoundException(message="Product not found")
UNAUTHORIZED_EXCEPTION = UnauthorizedException(message="Product not authorized")
RESOURCE_ALREADY_EXISTS_EXCEPTION = ResourceAlreadyExistsException(message="Product already exists")


class ProductService:
    def __init__(self, repository=MagaluProductListRepository(base_url=os.getenv('MAGALU_API_URL'))):
        self.__repository = repository

    def find_by_id(self, id):
        product = self.__repository.find_by_id(id)
        if product is None:
            raise NOT_FOUND_EXCEPTION

        return product

    def get_all_paginated(self, offset=None):
        return self.__repository.get_all_paginated(offset)
