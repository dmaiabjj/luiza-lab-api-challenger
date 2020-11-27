from app.domain.interfaces.base_repository import BaseRepository
from app.domain.user.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(clazz=User)

    def find_by_email(self, email, include_deleted=False):
        filter = self.bind_filter(filter=User.email == email, include_deleted=include_deleted)
        return User.query.filter(filter).one_or_none()
