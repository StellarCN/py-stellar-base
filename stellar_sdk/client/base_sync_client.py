from abc import ABCMeta, abstractmethod

from .response import Response


class BaseSyncClient(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url, params) -> Response:
        pass

    @abstractmethod
    def post(self, url, data) -> Response:
        pass

    @abstractmethod
    def stream(self, url, params):
        pass

    @abstractmethod
    def close(self):
        pass
