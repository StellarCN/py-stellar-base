import pytest

from tests.mock_servers import (
    HorizonMock,
    httpbin_get_handler,
    httpbin_post_handler,
)


@pytest.fixture
def httpbin_url(httpserver):
    httpserver.expect_request("/get", method="GET").respond_with_handler(
        httpbin_get_handler
    )
    httpserver.expect_request("/post", method="POST").respond_with_handler(
        httpbin_post_handler
    )
    return httpserver.url_for("/")


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


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip_integration = pytest.mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
