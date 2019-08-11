from abc import ABCMeta, abstractmethod
from typing import Union, Dict, Any, Generator

from .response import Response


class BaseSyncClient(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str, params: Dict[str, str] = None) -> Response:
        pass

    @abstractmethod
    def post(self, url: str, data: Dict[str, str]) -> Response:
        pass

    @abstractmethod
    def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        pass

    @abstractmethod
    def close(self):
        pass
