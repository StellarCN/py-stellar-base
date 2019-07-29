from abc import ABCMeta, abstractmethod
from typing import AsyncGenerator

from .response import Response


class BaseAsyncClient(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, url, params) -> Response:
        pass

    @abstractmethod
    async def post(self, url, params) -> Response:
        pass

    @abstractmethod
    async def stream(self, url) -> AsyncGenerator:
        pass
