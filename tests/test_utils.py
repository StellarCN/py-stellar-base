import pytest

from stellar_sdk.exceptions import NoApproximationError
from stellar_sdk.utils import best_rational_approximation


class TestUtils:
    @pytest.mark.parametrize(
        "n, d, v",
        [
            (1, 10, "0.1"),
            (1, 100, "0.01"),
            (1, 1000, "0.001"),
            (54301793, 100000, "543.017930"),
            (31969983, 100000, "319.69983"),
            (93, 100, "0.93"),
            (1, 2, "0.5"),
            (173, 100, "1.730"),
            (5333399, 6250000, "0.85334384"),
            (11, 2, "5.5"),
            (272783, 100000, "2.72783"),
            (638082, 1, "638082.0"),
            (36731261, 12500000, "2.93850088"),
            (1451, 25, "58.04"),
            (8253, 200, "41.265"),
            (12869, 2500, "5.1476"),
            (4757, 50, "95.14"),
            (3729, 5000, "0.74580"),
            (4119, 1, "4119.0"),
        ],
    )
    def test_best_rational_approximation(self, v, n, d):
        assert best_rational_approximation(v) == {"n": n, "d": d}

    @pytest.mark.parametrize("v", ["0.0000000003", 2147483648])
    def test_best_rational_approximation_raise(self, v):
        with pytest.raises(NoApproximationError, match="Couldn't find approximation."):
            best_rational_approximation(v)
