from decimal import Decimal

import pytest

from stellar_sdk import ManageSellOffer, Operation, Price

from . import *


class TestManageSellOffer:
    @pytest.mark.parametrize(
        "amount, price, offer_id, source, xdr",
        [
            pytest.param(
                "100",
                "1",
                123456,
                None,
                "AAAAAAAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="without_source",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="with_source_public_key",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAwAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAEAAAAAAAHiQA==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAwAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAEAAAAAAAHiQA==",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("100"),
                "1",
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="amount_decimal",
            ),
            pytest.param(
                "100",
                Decimal("1"),
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="price_decimal",
            ),
            pytest.param(
                "100",
                Price(1, 1),
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="price_object",
            ),
            pytest.param(
                "100",
                "1",
                0,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAAAAA=",
                id="new_offer",
            ),
            pytest.param(
                "0",
                "1",
                123456,
                None,
                "AAAAAAAAAAMAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAAAAAAAAAAAEAAAABAAAAAAAB4kA=",
                id="delete_offer",
            ),
        ],
    )
    def test_xdr(self, amount, price, offer_id, source, xdr):
        selling = native_asset
        buying = asset1
        op = ManageSellOffer(selling, buying, amount, price, offer_id, source)
        assert op.buying == buying
        assert op.selling == selling
        assert op.amount == str(amount)
        assert (
            op.price == price
            if isinstance(price, Price)
            else Price.from_raw_price(str(price))
        )
        assert op.offer_id == offer_id
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_amount_raise(self):
        amount = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "amount" must have at most 7 digits after the decimal: {amount}',
        ):
            ManageSellOffer(native_asset, asset1, amount, "1", 0, kp1.public_key)
