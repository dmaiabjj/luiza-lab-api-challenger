from sqlalchemy import and_

from app.domain.wishlist.wishlist import WishList
from app.infrastructure.repository.data_base_repository import DataBaseRepository


class WishListRepository(DataBaseRepository):
    def __init__(self):
        super().__init__(WishList)

    def find_by_product_and_customer_id(self, customer_id, product_id):
        return WishList.query.filter(and_(WishList.product_id == product_id,
                                          WishList.customer_id == customer_id)).one_or_none()
