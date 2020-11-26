from app.domain.wishlist.wishlist import WishList
from app.domain.interfaces.base_repository import BaseRepository


class WishListRepository(BaseRepository):
    def __init__(self):
        super().__init__(WishList)
