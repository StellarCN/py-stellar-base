import pytest

from stellar_sdk import ClaimClaimableBalance, Operation

from . import *


class TestClaimClaimableBalance:
    @pytest.mark.parametrize(
        "source, xdr",
        [
            pytest.param(
                None,
                "AAAAAAAAAA8AAAAA2g1X2n1IUOf8ENKp0OvHMfevtAV0wDOVsX1JFJuR9b4=",
                id="without_source",
            ),
            pytest.param(
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA8AAAAA2g1X2n1IUOf8ENKp0OvHMfevtAV0wDOVsX1JFJuR9b4=",
                id="with_source_public_key",
            ),
            pytest.param(
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADwAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vg==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADwAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vg==",
                id="with_source_muxed_account_strkey",
            ),
        ],
    )
    def test_xdr(self, source, xdr):
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        op = ClaimClaimableBalance(balance_id, source)
        assert op.balance_id == balance_id
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_balance_id_raise(self):
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5"
        )
        with pytest.raises(
            ValueError,
            match=f'Value of argument "balance_id" is not a valid balance id: {balance_id}',
        ):
            ClaimClaimableBalance(balance_id, kp1.public_key)
