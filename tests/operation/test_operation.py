from decimal import Inexact, Rounded, getcontext, localcontext

import pytest

from stellar_sdk import Operation


class TestOperation:
    @pytest.mark.parametrize(
        ("origin_amount", "expect_value"),
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
        ("origin_amount", "exception", "reason"),
        [
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
            ("abc", ValueError, "Value of 'abc' is not a number."),
            ("", ValueError, "Value of '' is not a number."),
            ("Infinity", ValueError, "Value of 'Infinity' is not a number."),
        ],
    )
    def test_to_xdr_amount_raise(self, origin_amount, exception, reason):
        with pytest.raises(exception, match=reason):
            Operation.to_xdr_amount(origin_amount)

    @pytest.mark.parametrize(
        ("origin_amount", "expect_value"),
        [
            (100000000, "10"),
            (1000000, "0.1"),
            (1234567, "0.1234567"),
            (1, "0.0000001"),
            (9223372036854775807, "922337203685.4775807"),
        ],
    )
    def test_from_xdr_amount(self, origin_amount, expect_value):
        assert Operation.from_xdr_amount(origin_amount) == expect_value

    @pytest.mark.parametrize(
        ("precision", "trap_rounding"), [(7, False), (9, False), (18, False), (7, True)]
    )
    def test_amount_does_not_depend_on_the_decimal_context(
        self, precision, trap_rounding
    ):
        # An application may lower its own precision below the 19 digits an amount
        # can have, or trap rounding.
        with localcontext() as ctx:
            ctx.prec = precision
            ctx.traps[Inexact] = ctx.traps[Rounded] = trap_rounding
            assert Operation.to_xdr_amount("1234.5678901") == 12345678901
            assert Operation.from_xdr_amount(12345678901) == "1234.5678901"
            largest = "922337203685.4775807"
            assert Operation.to_xdr_amount(largest) == 9223372036854775807
            assert Operation.from_xdr_amount(9223372036854775807) == largest
            with pytest.raises(ValueError, match="at most 7 digits"):
                Operation.to_xdr_amount("0.12345678")

    def test_amount_conversion_leaves_the_decimal_context_alone(self):
        with localcontext() as ctx:
            ctx.prec = 9
            ctx.clear_flags()
            Operation.to_xdr_amount("1234.5678901")
            Operation.from_xdr_amount(12345678901)
            with pytest.raises(ValueError, match="is not a number"):
                Operation.to_xdr_amount("abc")
            assert getcontext() is ctx
            assert ctx.prec == 9
            assert not any(ctx.flags.values())
