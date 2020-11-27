from sqlalchemy import and_

from app.domain.customer.customer import Customer
from app.domain.interfaces.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(clazz=Customer)

    def find_by_email(self, email, include_deleted=False):
        filter = self.bind_filter(filter=Customer.email == email, include_deleted=include_deleted)
        return Customer.query.filter(filter).one_or_none()
