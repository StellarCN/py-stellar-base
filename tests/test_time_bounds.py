import pytest

from stellar_sdk.time_bounds import TimeBounds


class TestTimeBounds:
    @pytest.mark.parametrize(
        "min_time, max_time, xdr",
        [
            (1560844454, 1560846000, "AAAAAF0ImKYAAAAAXQiesA=="),
            (1560844454, 0, "AAAAAF0ImKYAAAAAAAAAAA=="),
            (1583633108, 1583633108, "AAAAAF5kUtQAAAAAXmRS1A=="),
        ],
    )
    def test_to_xdr(self, min_time, max_time, xdr):
        op = TimeBounds(min_time, max_time)
        assert op.to_xdr() == xdr
        assert TimeBounds.from_xdr(xdr) == op
        from_instance = TimeBounds.from_xdr_object(op.to_xdr_object())
        assert isinstance(from_instance, TimeBounds)
        assert from_instance.max_time == max_time
        assert from_instance.min_time == min_time

    @pytest.mark.parametrize(
        "min_time, max_time, message", [
            (-1, 1560844454, "min_time cannot be negative."),
            (1560844454, -1, "max_time cannot be negative."),
            (1560844455, 156084454, "max_time must be >= min_time.")]
    )
    def test_to_xdr_with_invalid_time_raise(self, min_time, max_time, message):
        with pytest.raises(ValueError, match=message):
            TimeBounds(min_time, max_time)

    def test_equals(self):
        assert TimeBounds(1, 2) == TimeBounds(1, 2)
        assert TimeBounds(1, 2) != TimeBounds(1, 0)
