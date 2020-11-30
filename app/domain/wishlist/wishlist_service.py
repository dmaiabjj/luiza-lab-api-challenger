from app.presentation.base_response_exception import ResourceAlreadyExistsException, NotFoundException, \
    UnauthorizedException

NOT_FOUND_EXCEPTION = NotFoundException(message="Product not found")
UNAUTHORIZED_EXCEPTION = UnauthorizedException(message="Product not authorized")
RESOURCE_ALREADY_EXISTS_EXCEPTION = ResourceAlreadyExistsException(message="Product already exists")


class WishListService:
    def __init__(self, repository):
        self.__repository = repository

    def add(self, wishlist):
        product_already_exists = self.__repository.find_by_product_and_customer_id(product_id=wishlist.product_id,
                                                                                   customer_id=wishlist.customer_id)
        if product_already_exists:
            wishlist = self.__repository.update_from_model(product_already_exists, wishlist)
        else:
            wishlist = self.__repository.add(wishlist)

        return wishlist.to_dict()

    def delete(self, product_id, customer_id):
        wishlist = self.__repository.find_by_product_and_customer_id(product_id=product_id, customer_id=customer_id)
        if wishlist is None:
            raise NOT_FOUND_EXCEPTION

        self.__repository.delete(wishlist)

    def get_all_paginated(self, customer_id, offset=1, limit=10):
        wishlist = self.__repository.get_all_paginated_by_id(customer_id=customer_id, offset=offset - 1, limit=limit)
        return list(map(lambda item: item.to_dict(), wishlist))
