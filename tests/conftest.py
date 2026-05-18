import json
from dataclasses import dataclass

import pytest
from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response


def _httpbin_headers(request):
    return {key: value for key, value in request.headers.items()}


def _json_response(payload):
    return Response(json.dumps(payload), content_type="application/json")


def _httpbin_get(request):
    return _json_response(
        {
            "args": request.args.to_dict(flat=True),
            "headers": _httpbin_headers(request),
            "url": request.url,
        }
    )


def _httpbin_post(request):
    return _json_response(
        {
            "form": request.form.to_dict(flat=True),
            "headers": _httpbin_headers(request),
            "url": request.url,
        }
    )


@pytest.fixture
def httpbin_url(httpserver):
    httpserver.expect_request("/get", method="GET").respond_with_handler(_httpbin_get)
    httpserver.expect_request("/post", method="POST").respond_with_handler(
        _httpbin_post
    )
    return httpserver.url_for("/")


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
                Response(body, content_type=content_type or "text/plain")
            )
        else:
            request.respond_with_json(json, status=status)


@pytest.fixture
def horizon_mock(httpserver):
    return HorizonMock(httpserver)


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marks tests as integration tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip_integration = pytest.mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
