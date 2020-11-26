from app.domain.customer.customer import Customer
from app.domain.interfaces.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(clazz=Customer)
