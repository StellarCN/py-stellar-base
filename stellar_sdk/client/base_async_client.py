from abc import ABCMeta, abstractmethod
from typing import AsyncGenerator, Dict, Union, Any

from .response import Response


class BaseAsyncClient(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, url: str, params: Dict[str, str] = None) -> Response:
        pass

    @abstractmethod
    async def post(self, url: str, data: Dict[str, str]) -> Response:
        pass

    @abstractmethod
    async def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
