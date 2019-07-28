from abc import ABCMeta, abstractmethod

from typing import AsyncGenerator


class BaseAsyncClient(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, url, params):
        pass

    @abstractmethod
    async def post(self, url, params):
        pass

    @abstractmethod
    async def stream(self, url) -> AsyncGenerator:
        pass
