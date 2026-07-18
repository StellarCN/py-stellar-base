"""Shared test doubles for call-builder tests.

Call-builder tests only assert on endpoint/params building and must never
perform I/O — the dummy clients below raise if a request slips through.
(``test_base_call_builder.py`` is the exception: it exercises ``call()`` and
``_stream()`` against real clients and a local mock server.)
"""

from collections.abc import AsyncGenerator, Generator
from typing import Any

from stellar_sdk.client.base_async_client import BaseAsyncClient
from stellar_sdk.client.base_sync_client import BaseSyncClient
from stellar_sdk.client.response import Response

HORIZON_URL = "https://horizon.stellar.test"


class DummySyncClient(BaseSyncClient):
    def get(
        self,
        url: str,
        params: dict[str, str] | None = None,
        max_content_size: int | None = None,
    ) -> Response:
        raise AssertionError("call-builder tests must not perform I/O")

    def post(
        self,
        url: str,
        data: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> Response:
        raise AssertionError("call-builder tests must not perform I/O")

    def stream(
        self, url: str, params: dict[str, str] | None = None
    ) -> Generator[dict[str, Any], None, None]:
        raise AssertionError("call-builder tests must not perform I/O")

    def close(self) -> None:
        pass


class DummyAsyncClient(BaseAsyncClient):
    async def get(
        self,
        url: str,
        params: dict[str, str] | None = None,
        max_content_size: int | None = None,
    ) -> Response:
        raise AssertionError("call-builder tests must not perform I/O")

    async def post(
        self,
        url: str,
        data: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> Response:
        raise AssertionError("call-builder tests must not perform I/O")

    def stream(
        self, url: str, params: dict[str, str] | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        raise AssertionError("call-builder tests must not perform I/O")

    async def close(self) -> None:
        pass


SYNC_CLIENT = DummySyncClient()
ASYNC_CLIENT = DummyAsyncClient()
