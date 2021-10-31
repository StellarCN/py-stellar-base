import pytest

from stellar_sdk import EndSponsoringFutureReserves, Operation

from . import *


class TestEndSponsoringFutureReserves:
    @pytest.mark.parametrize(
        "source, xdr",
        [
            pytest.param(
                None,
                "AAAAAAAAABE=",
                id="without_source",
            ),
            pytest.param(
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABE=",
                id="with_source_public_key",
            ),
            pytest.param(
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEQ==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEQ==",
                id="with_source_muxed_account_strkey",
            ),
        ],
    )
    def test_xdr(self, source, xdr):
        op = EndSponsoringFutureReserves(source)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
