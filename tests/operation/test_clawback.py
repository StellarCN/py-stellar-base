from decimal import Decimal

import pytest

from stellar_sdk import Clawback, Operation

from . import *


class TestClawback:
    @pytest.mark.parametrize(
        "from_, amount, source, xdr",
        [
            pytest.param(
                kp2.public_key,
                "100",
                None,
                "AAAAAAAAABMAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAA7msoA",
                id="without_source",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABMAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAA7msoA",
                id="with_source_public_key",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEwAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAADuaygA=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEwAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAADuaygA=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                muxed2,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABMAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAQAAAAAAAAAAAmJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAADuaygA=",
                id="with_from_muxed_account",
            ),
            pytest.param(
                muxed2.account_muxed,
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABMAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAQAAAAAAAAAAAmJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAADuaygA=",
                id="with_from_muxed_account_strkey",
            ),
            pytest.param(
                kp2.public_key,
                Decimal("100"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABMAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAA7msoA",
                id="amount_decimal",
            ),
        ],
    )
    def test_xdr(self, from_, amount, source, xdr):
        op = Clawback(asset1, from_, amount, source)
        check_source(op.source, source)
        assert op.asset == asset1
        assert op.amount == str(amount)
        if isinstance(from_, str):
            assert op.from_ == MuxedAccount.from_account(from_)
        else:
            assert op.from_ == from_
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_amount_raise(self):
        amount = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "amount" must have at most 7 digits after the decimal: {amount}',
        ):
            Clawback(asset1, kp2.public_key, amount, kp1.public_key)
