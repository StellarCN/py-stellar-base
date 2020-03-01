from stellar_sdk.price import Price


class TestPrice:
    def test_to_xdr(self):
        n, d = 1, 2
        price = Price(n, d)
        assert price.to_xdr() == "AAAAAQAAAAI="
        assert Price.from_xdr("AAAAAQAAAAI=") == price
        from_instance = Price.from_xdr_object(price.to_xdr_object())
        assert isinstance(from_instance, Price)
        assert from_instance.n == n
        assert from_instance.d == d

    def test_from_raw_price(self):
        raw_price = "2.93850088"
        price = Price.from_raw_price(raw_price)
        assert price.n == 36731261
        assert price.d == 12500000

    def test_equals(self):
        assert Price(1, 2) == Price(1, 2)
        assert Price(1, 2) != Price(3, 4)
        assert Price(1, 2) != "BAD TYPE"
