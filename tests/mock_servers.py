"""Local-HTTP-server mocks shared by the test suite.

All HTTP mocking in this suite goes through ``pytest_httpserver`` — a real
local HTTP server that both the sync (requests) and async (aiohttp) clients
can talk to. The wrappers here add domain-specific conveniences on top of the
raw ``httpserver`` fixture; the fixtures that expose them live in
``tests/conftest.py``.
"""

import json
from dataclasses import dataclass
from typing import Any

from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response

RPC_PATH = "/rpc"


def _httpbin_headers(request):
    return dict(request.headers)


def _json_response(payload):
    return Response(json.dumps(payload), content_type="application/json")


def httpbin_get_handler(request):
    """Emulate httpbin.org/get: echo query args, headers and url."""
    return _json_response(
        {
            "args": request.args.to_dict(flat=True),
            "headers": _httpbin_headers(request),
            "url": request.url,
        }
    )


def httpbin_post_handler(request):
    """Emulate httpbin.org/post: echo form data, headers and url."""
    return _json_response(
        {
            "form": request.form.to_dict(flat=True),
            "headers": _httpbin_headers(request),
            "url": request.url,
        }
    )


@dataclass(frozen=True)
class HorizonMock:
    httpserver: HTTPServer

    @property
    def url(self) -> str:
        return self.httpserver.url_for("/")

    def expect(
        self,
        path: str,
        *,
        method: str = "GET",
        json=None,
        status: int = 200,
        query_string: str | None = None,
        body: str | None = None,
        content_type: str | None = None,
    ) -> None:
        request = self.httpserver.expect_request(
            path, method=method, query_string=query_string
        )
        if body is not None:
            request.respond_with_response(
                Response(body, status=status, content_type=content_type or "text/plain")
            )
        else:
            request.respond_with_json(json, status=status)


@dataclass(frozen=True)
class RpcMock:
    """JSON-RPC mock for Stellar RPC (Soroban) server tests.

    Responses are queued with one-shot handlers, so calling an ``expect_*``
    method twice serves two sequential RPC calls in FIFO order.
    """

    httpserver: HTTPServer

    @property
    def url(self) -> str:
        return self.httpserver.url_for(RPC_PATH)

    def expect_response(self, data: dict[str, Any], *, status: int = 200) -> None:
        """Queue one JSON-RPC response envelope, served as-is."""
        self.httpserver.expect_oneshot_request(
            RPC_PATH, method="POST"
        ).respond_with_json(data, status=status)

    def expect_raw(self, body: str, *, status: int = 200) -> None:
        """Queue one non-JSON response (e.g. a proxy error page)."""
        self.httpserver.expect_oneshot_request(
            RPC_PATH, method="POST"
        ).respond_with_response(
            Response(body, status=status, content_type="text/plain")
        )

    @property
    def requests(self) -> list[dict[str, Any]]:
        """Parsed JSON bodies of all RPC POSTs received, in order."""
        return [
            request.get_json()
            for request, _ in self.httpserver.log
            if request.method == "POST"
        ]

    def assert_request(self, method: str, params: Any, *, index: int = -1) -> None:
        """Assert the JSON-RPC envelope of the *index*-th request received."""
        body = self.requests[index]
        assert len(body["id"]) == 32  # uuid4 hex
        assert body["jsonrpc"] == "2.0"
        assert body["method"] == method
        assert body["params"] == params
