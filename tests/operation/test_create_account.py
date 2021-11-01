from decimal import Decimal

import pytest

from stellar_sdk import CreateAccount, Operation

from . import *


class TestCreateAccount:
    @pytest.mark.parametrize(
        "starting_balance, source, xdr",
        [
            pytest.param(
                "100",
                None,
                "AAAAAAAAAAAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAAO5rKAA==",
                id="without_source",
            ),
            pytest.param(
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAAO5rKAA==",
                id="with_source_public_key",
            ),
            pytest.param(
                "100",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAA7msoA",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "100",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAA7msoA",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("100"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAAO5rKAA==",
                id="starting_balance_decimal",
            ),
        ],
    )
    def test_xdr(self, starting_balance, source, xdr):
        op = CreateAccount(kp2.public_key, starting_balance, source)
        assert op.destination == kp2.public_key
        assert op.starting_balance == str(starting_balance)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_destination_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "destination" is not a valid ed25519 public key: {key}',
        ):
            CreateAccount(key, "20", kp1.public_key)

    def test_invalid_limit_raise(self):
        starting_balance = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "starting_balance" must have at most 7 digits after the decimal: {starting_balance}',
        ):
            CreateAccount(kp2.public_key, starting_balance, kp1.public_key)
