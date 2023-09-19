from typing import Optional, Union

import pytest

from stellar_sdk import Operation
from stellar_sdk.operation import RestoreFootprint

from . import *


class TestRestoreFootprint:
    @pytest.mark.parametrize(
        "source, xdr",
        [
            pytest.param(None, "AAAAAAAAABoAAAAA", id="without_source"),
            pytest.param(
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAGgAAAAA=",
                id="with_source_muxed_account",
            ),
        ],
    )
    def test_xdr(self, source: Optional[Union[MuxedAccount, str]], xdr: str):
        op = RestoreFootprint(source)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
