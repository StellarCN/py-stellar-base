import pytest

from stellar_sdk import Operation
from stellar_sdk.type_checked import _STELLAR_SDK_RUNTIME_TYPE_CHECKING


class TestOperation:
    @pytest.mark.parametrize(
        "origin_amount, expect_value",
        [
            ("10", 100000000),
            ("0.10", 1000000),
            ("0.1234567", 1234567),
            ("922337203685.4775807", 9223372036854775807),
        ],
    )
    def test_to_xdr_amount(self, origin_amount, expect_value):
        assert Operation.to_xdr_amount(origin_amount) == expect_value

    @pytest.mark.parametrize(
        "origin_amount, exception, reason",
        [
            pytest.param(
                10,
                TypeError,
                'type of argument "value" must be one of \\(str, decimal.Decimal\\); got int instead',
                marks=pytest.mark.skipif(
                    not _STELLAR_SDK_RUNTIME_TYPE_CHECKING,
                    reason="runtime_type_checking_disabled",
                ),
            ),
            (
                "-0.1",
                ValueError,
                "Value of '-0.1' must represent a positive number and the max valid value is 922337203685.4775807.",
            ),
            (
                "922337203685.4775808",
                ValueError,
                "Value of '922337203685.4775808' must represent a positive number and the max valid value is 922337203685.4775807.",
            ),
            (
                "0.123456789",
                ValueError,
                "Value of '0.123456789' must have at most 7 digits after the decimal.",
            ),
        ],
    )
    def test_to_xdr_amount_raise(self, origin_amount, exception, reason):
        with pytest.raises(exception, match=reason):
            Operation.to_xdr_amount(origin_amount)

    @pytest.mark.parametrize(
        "origin_amount, expect_value",
        [
            (100000000, "10"),
            (1000000, "0.1"),
            (1234567, "0.1234567"),
            (9223372036854775807, "922337203685.4775807"),
        ],
    )
    def test_from_xdr_amount(self, origin_amount, expect_value):
        assert Operation.from_xdr_amount(origin_amount) == expect_value
