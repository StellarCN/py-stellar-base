import pytest

from stellar_sdk.time_bounds import TimeBounds


class TestTimeBounds:

    @pytest.mark.parametrize('min_time, max_time, xdr', [
        (1560844454, 1560846000, 'AAAAAF0ImKYAAAAAXQiesA=='),
        (1560844454, 0, 'AAAAAF0ImKYAAAAAAAAAAA==')
    ])
    def test_to_xdr(self, min_time, max_time, xdr):
        op_xdr_object = TimeBounds(min_time, max_time).to_xdr_object()
        assert op_xdr_object.to_xdr() == xdr
        from_instance = TimeBounds.from_xdr_object(op_xdr_object)
        assert isinstance(from_instance, TimeBounds)
        assert from_instance.max_time == max_time
        assert from_instance.min_time == min_time

    @pytest.mark.parametrize('min_time, max_time', [
        (1560844454, 1560844454),
        (1560844454, 1),
    ])
    def test_to_xdr_with_invalid_time_raise(self, min_time, max_time):
        with pytest.raises(ValueError, match="max_time must be >= min_time."):
            TimeBounds(min_time, max_time)

    def test_equals(self):
        assert TimeBounds(1, 2) == TimeBounds(1, 2)
        assert TimeBounds(1, 2) != TimeBounds(1, 0)
