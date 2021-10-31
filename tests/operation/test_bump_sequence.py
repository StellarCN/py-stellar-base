import pytest

from stellar_sdk import BumpSequence, Operation

from . import *


class TestBumpSequence:
    @pytest.mark.parametrize(
        "bump_to, source, xdr",
        [
            pytest.param(
                1234567890, None, "AAAAAAAAAAsAAAAASZYC0g==", id="without_source"
            ),
            pytest.param(
                1234567890,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAsAAAAASZYC0g==",
                id="with_source_public_key",
            ),
            pytest.param(
                1234567890,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACwAAAABJlgLS",
                id="with_source_muxed_account",
            ),
            pytest.param(
                1234567890,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACwAAAABJlgLS",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                0,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAsAAAAAAAAAAA==",
                id="bump_to_0",
            ),
        ],
    )
    def test_xdr(self, bump_to, source, xdr):
        op = BumpSequence(bump_to, source)
        assert op.bump_to == bump_to
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
