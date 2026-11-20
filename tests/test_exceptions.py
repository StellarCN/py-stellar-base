import pytest

from stellar_sdk.client.response import Response
from stellar_sdk.exceptions import BadRequestError


@pytest.mark.parametrize(
    "body", ['{"title": "Bad"}', '{"title": "Bad", "extras": null}']
)
def test_horizon_error_without_extras(body):
    error = BadRequestError(Response(400, body, {}, "https://example.org/"))
    assert error.title == "Bad"
    assert error.extras is None
    assert error.result_xdr is None


def test_horizon_error_with_extras():
    body = '{"title": "Bad", "extras": {"result_xdr": "AAAAAAAAAGT////7AAAAAA=="}}'
    error = BadRequestError(Response(400, body, {}, "https://example.org/"))
    assert error.result_xdr == "AAAAAAAAAGT////7AAAAAA=="
