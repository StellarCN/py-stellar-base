import pytest


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
