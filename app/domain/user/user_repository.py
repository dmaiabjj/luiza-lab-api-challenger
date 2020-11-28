from app.domain.user.user import User
from app.infrastructure.repository.data_base_repository import DataBaseRepository


class UserRepository(DataBaseRepository):
    def __init__(self):
        super().__init__(clazz=User)

    def find_by_email(self, email, include_deleted=False):
        filter = self.bind_filter(filter=User.email == email, include_deleted=include_deleted)
        return User.query.filter(filter).one_or_none()
