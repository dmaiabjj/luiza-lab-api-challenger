import abc

import requests


class APIRepository:
    def __init__(self, base_url=None):
        self._base_url = base_url

    def __do_get(self, url):
        return requests.get(url=self._base_url + url, verify=False)

    @abc.abstractmethod
    def parser(self, response):
        return response.json()

    def get(self, url=''):
        response = self.__do_get(url=url)
        data = self.parser(response)

        return data
