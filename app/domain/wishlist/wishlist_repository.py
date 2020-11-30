from sqlalchemy import and_

from app.domain.wishlist.wishlist import WishList
from app.infrastructure.repository.data_base_repository import DataBaseRepository


class WishListRepository(DataBaseRepository):
    def __init__(self):
        super().__init__(WishList)

    def find_by_product_and_customer_id(self, customer_id, product_id):
        return WishList.query.filter(and_(WishList.product_id == product_id,
                                          WishList.customer_id == customer_id)).one_or_none()

    def get_all_paginated_by_id(self, customer_id, offset=None, limit=None, include_deleted=False):
        filter = self.bind_filter(filter=WishList.customer_id == customer_id, include_deleted=include_deleted)
        query = WishList.query.filter(filter).order_by(WishList.id)
        query = query.offset(offset) if offset else query
        query = query.limit(limit) if limit else query
        return query.all()
