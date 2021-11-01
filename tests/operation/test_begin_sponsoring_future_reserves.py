import pytest

from stellar_sdk import BeginSponsoringFutureReserves, Operation

from . import *


class TestBeginSponsoringFutureReserves:
    @pytest.mark.parametrize(
        "source, xdr",
        [
            pytest.param(
                None,
                "AAAAAAAAABAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rg=",
                id="without_source",
            ),
            pytest.param(
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rg=",
                id="with_source_public_key",
            ),
            pytest.param(
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uA==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uA==",
                id="with_source_muxed_account_strkey",
            ),
        ],
    )
    def test_xdr(self, source, xdr):
        op = BeginSponsoringFutureReserves(kp2.public_key, source)
        assert op.sponsored_id == kp2.public_key
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_sponsored_id_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "sponsored_id" is not a valid ed25519 public key: {key}',
        ):
            BeginSponsoringFutureReserves(key, kp1.public_key)
