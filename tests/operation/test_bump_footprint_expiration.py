from typing import Optional, Union

import pytest

from stellar_sdk import Operation
from stellar_sdk.operation import BumpFootprintExpiration

from . import *


class TestBumpFootprintExpiration:
    @pytest.mark.parametrize(
        "ledgers_to_expire, source, xdr",
        [
            pytest.param(
                1234567890, None, "AAAAAAAAABkAAAAASZYC0g==", id="without_source"
            ),
            pytest.param(
                1234567890,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABkAAAAASZYC0g==",
                id="with_source_public_key",
            ),
            pytest.param(
                1234567890,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAGQAAAABJlgLS",
                id="with_source_muxed_account",
            ),
            pytest.param(
                1234567890,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAGQAAAABJlgLS",
                id="with_source_muxed_account_strkey",
            ),
        ],
    )
    def test_xdr(
        self,
        ledgers_to_expire: int,
        source: Optional[Union[MuxedAccount, str]],
        xdr: str,
    ):
        op = BumpFootprintExpiration(ledgers_to_expire, source)
        assert op.ledgers_to_expire == ledgers_to_expire
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    @pytest.mark.parametrize("ledgers_to_expire", [-1, 2**32])
    def test_invalid_ledgers_to_expire(self, ledgers_to_expire):
        with pytest.raises(ValueError):
            BumpFootprintExpiration(ledgers_to_expire)
