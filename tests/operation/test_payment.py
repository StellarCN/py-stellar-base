from decimal import Decimal

import pytest

from stellar_sdk import Operation, Payment

from . import *


class TestPayment:
    @pytest.mark.parametrize(
        "destination, amount, source, xdr",
        [
            pytest.param(
                kp2.public_key,
                "100",
                None,
                "AAAAAAAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoA",
                id="without_source",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoA",
                id="with_source_public_key",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygA=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygA=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                muxed2,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAEAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygA=",
                id="with_destination_muxed_account",
            ),
            pytest.param(
                muxed2.account_muxed,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAEAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygA=",
                id="with_destination_muxed_account_strkey",
            ),
            pytest.param(
                kp2.public_key,
                Decimal("100"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoA",
                id="amount_decimal",
            ),
        ],
    )
    def test_xdr(self, destination, amount, source, xdr):
        op = Payment(destination, asset1, amount, source)
        assert (
            op.destination == destination
            if isinstance(destination, MuxedAccount)
            else MuxedAccount.from_account(destination)
        )
        assert op.amount == str(amount)
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
            Payment(kp2.public_key, native_asset, amount, kp1.public_key)
