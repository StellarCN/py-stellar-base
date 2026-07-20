from collections.abc import AsyncIterator

import pytest
from pytest_httpserver import HTTPServer

from stellar_sdk import (
    AiohttpClient,
    Server,
    ServerAsync,
    SorobanServer,
    SorobanServerAsync,
)
from tests.mock_servers import (
    HorizonMock,
    RpcMock,
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


@pytest.fixture
def rpc_mock(httpserver: HTTPServer) -> RpcMock:
    return RpcMock(httpserver)


@pytest.fixture(params=["sync", "async"])
async def soroban_server(
    request: pytest.FixtureRequest, rpc_mock: RpcMock
) -> AsyncIterator[SorobanServer | SorobanServerAsync]:
    """One test body, both flavors: a SorobanServer against the local rpc_mock.

    Use ``await resolve(...)`` (tests.helpers) around server calls so the same
    test drives the sync and async implementation.
    """
    if request.param == "sync":
        with SorobanServer(rpc_mock.url) as server:
            yield server
    else:
        async with SorobanServerAsync(rpc_mock.url) as server:
            yield server


@pytest.fixture(params=["sync", "async"])
async def horizon_server(
    request: pytest.FixtureRequest, horizon_mock: HorizonMock
) -> AsyncIterator[Server | ServerAsync]:
    """One test body, both flavors: a Horizon Server against horizon_mock."""
    if request.param == "sync":
        with Server(horizon_mock.url) as server:
            yield server
    else:
        async with ServerAsync(horizon_mock.url, AiohttpClient()) as server:
            yield server


def pytest_runtest_teardown(item):
    """Fail a test that issued a request no handler matched.

    ``requests_mock``/``aioresponses``, which this suite used before
    standardizing on ``pytest_httpserver``, raised on an unmatched request.
    ``pytest_httpserver`` instead answers 500 and records the mismatch, which
    only fails a test if that 500 happens to reach an assertion. Checking here
    restores the old behavior: a misrouted or unexpected request is an error,
    not a silent pass.

    This is a hook rather than an autouse fixture so that tests which never
    touch HTTP do not pull in the server at all.
    """
    server = getattr(item, "funcargs", {}).get("httpserver")
    if server is not None:
        server.check()


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
