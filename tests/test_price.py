import pytest

from stellar_sdk import Price
from stellar_sdk import xdr as stellar_xdr


class TestPrice:
    def test_xdr(self):
        n, d = 1, 2
        price_obj = Price(n, d).to_xdr_object()
        assert price_obj.to_xdr_base64() == "AAAAAQAAAAI="
        from_instance = Price.from_xdr_object(price_obj)
        assert isinstance(from_instance, Price)
        assert from_instance.n == n
        assert from_instance.d == d

    def test_from_raw_price(self):
        raw_price = "2.93850088"
        price = Price.from_raw_price(raw_price)
        assert price.n == 36731261
        assert price.d == 12500000

    def test_cmp(self):
        assert Price(1, 2) == Price(1, 2)
        assert Price(1, 2) != Price(3, 4)
        assert Price(1, 2) != "BAD TYPE"
        assert Price(2, 5) > Price(3, 100)
        assert Price(2, 5) >= Price(3, 100)
        assert Price(1, 2) >= Price(1, 2)
        assert Price(3, 100) < Price(2, 5)
        assert Price(3, 100) <= Price(2, 5)
        assert Price(1, 2) <= Price(1, 2)

    def test_equal_prices_have_equal_hashes(self):
        a, b = Price(1, 2), Price(2, 4)
        assert hash(a) == hash(b)
        assert {a: "order"}.get(b) == "order"
        assert len({a, b}) == 1

    @pytest.mark.parametrize(("n", "d"), [(0, 1), (1, 0), (0, 0), (-1, 2), (1, -2)])
    def test_not_positive_raise(self, n, d):
        # The network takes only positive prices.
        with pytest.raises(ValueError, match="positive"):
            Price(n, d)
        with pytest.raises(ValueError, match="positive"):
            Price.from_xdr_object(stellar_xdr.Price(n=n, d=d))
