import json

import pytest
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


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")


def pytest_collection_modifyitems(config, items):
    skip_integration = pytest.mark.skip(reason="need --integration option to run")
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")

    for item in items:
        # Handle slow tests
        if "slow" in item.keywords and not config.getoption("--runslow"):
            item.add_marker(skip_slow)
        # Handle integration tests
        if "integration" in item.keywords and not config.getoption("--integration"):
            item.add_marker(skip_integration)
