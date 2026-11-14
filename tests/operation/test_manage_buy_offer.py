from decimal import Decimal

import pytest

from stellar_sdk import (
    ManageBuyOffer,
    Operation,
    Price,
)
from tests.operation.helpers import (
    asset1,
    check_source,
    kp1,
    muxed1,
    native_asset,
)


class TestManageBuyOffer:
    @pytest.mark.parametrize(
        ("amount", "price", "offer_id", "source", "xdr"),
        [
            pytest.param(
                "100",
                "1",
                123456,
                None,
                "AAAAAAAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="without_source",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="with_source_public_key",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAEAAAAAAAHiQA==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "100",
                "1",
                123456,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAQAAAAEAAAAAAAHiQA==",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("100"),
                "1",
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="amount_decimal",
            ),
            pytest.param(
                "100",
                Decimal("1"),
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="price_decimal",
            ),
            pytest.param(
                "100",
                Price(1, 1),
                123456,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAB4kA=",
                id="price_object",
            ),
            pytest.param(
                "100",
                "1",
                0,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAO5rKAAAAAAEAAAABAAAAAAAAAAA=",
                id="new_offer",
            ),
            pytest.param(
                "0",
                "1",
                123456,
                None,
                "AAAAAAAAAAwAAAAAAAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAAAAAAAAAAAEAAAABAAAAAAAB4kA=",
                id="delete_offer",
            ),
        ],
    )
    def test_xdr(self, amount, price, offer_id, source, xdr):
        selling = native_asset
        buying = asset1
        op = ManageBuyOffer(selling, buying, amount, price, offer_id, source)
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
            ManageBuyOffer(native_asset, asset1, amount, "1", 0, kp1.public_key)

    @pytest.mark.parametrize(
        "offer_id",
        [-1, -12345, 2**63, 2**64, 2**64 + 12345],
    )
    def test_offer_id_out_of_range_raise(self, offer_id):
        with pytest.raises(
            ValueError,
            match=r'Value of argument "offer_id" must be an integer between 0 and 2\*\*63 - 1',
        ):
            ManageBuyOffer(native_asset, asset1, "1", "1", offer_id, kp1.public_key)

    @pytest.mark.parametrize("offer_id", [0, 1, 2**63 - 1])
    def test_offer_id_at_bounds(self, offer_id):
        op = ManageBuyOffer(native_asset, asset1, "1", "1", offer_id, kp1.public_key)
        restored = ManageBuyOffer.from_xdr_object(op.to_xdr_object())
        assert restored.offer_id == offer_id

    def test_from_xdr_object_keeps_negative_offer_id(self):
        op = ManageBuyOffer(native_asset, asset1, "1", "1", 1, kp1.public_key)
        xdr_object = op.to_xdr_object()
        assert xdr_object.body.manage_buy_offer_op is not None
        xdr_object.body.manage_buy_offer_op.offer_id.int64 = -1
        restored = ManageBuyOffer.from_xdr_object(xdr_object)
        assert restored.offer_id == -1
        assert restored.to_xdr_object().to_xdr() == xdr_object.to_xdr()
