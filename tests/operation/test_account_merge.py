import pytest

from stellar_sdk import AccountMerge, Operation

from . import *


class TestAccountMerge:
    @pytest.mark.parametrize(
        "destination, source, xdr",
        [
            pytest.param(
                kp2.public_key,
                None,
                "AAAAAAAAAAgAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rg=",
                id="without_source",
            ),
            pytest.param(
                kp2.public_key,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAgAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rg=",
                id="with_source_public_key",
            ),
            pytest.param(
                kp2.public_key,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uA==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                kp2.public_key,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uA==",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                muxed2,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAgAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQ==",
                id="with_destination_muxed_account",
            ),
            pytest.param(
                muxed2.account_muxed,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAgAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQ==",
                id="with_destination_muxed_account_strkey",
            ),
        ],
    )
    def test_xdr(self, destination, source, xdr):
        op = AccountMerge(destination, source)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

        if isinstance(destination, str):
            assert op.destination == MuxedAccount.from_account(destination)
        else:
            assert op.destination == destination
