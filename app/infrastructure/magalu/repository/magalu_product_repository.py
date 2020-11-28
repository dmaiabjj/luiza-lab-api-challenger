from app.infrastructure.repository.api_base_repository import APIRepository
from app.presentation.base_response_exception import NotFoundException


class MagaluProductListRepository(APIRepository):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def parser(self, response):
        result = response.json()

        if 'error_message' in result:
            raise NotFoundException(message=result['error_message'])

        return result

    def find_by_id(self, id):
        return self.get(url=f"{id}/")

    def get_all_paginated(self, offset=1):
        return self.get(url=f"?page={offset}")
