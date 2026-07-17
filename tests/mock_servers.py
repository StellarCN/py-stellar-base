"""Local-HTTP-server mocks shared by the test suite.

All HTTP mocking in this suite goes through ``pytest_httpserver`` — a real
local HTTP server that both the sync (requests) and async (aiohttp) clients
can talk to. The wrappers here add domain-specific conveniences on top of the
raw ``httpserver`` fixture; the fixtures that expose them live in
``tests/conftest.py``.
"""

import json
from dataclasses import dataclass

from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response


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
