from app.domain.product.product import Product
from app.domain.interfaces.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)
