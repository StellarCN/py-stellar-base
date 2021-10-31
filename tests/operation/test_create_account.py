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
