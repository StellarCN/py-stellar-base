from decimal import Decimal

import pytest

from stellar_sdk import ChangeTrust, Operation

from . import *


class TestChangeTrust:
    @pytest.mark.parametrize(
        "asset, limit, source, xdr",
        [
            pytest.param(
                asset1,
                None,
                None,
                "AAAAAAAAAAYAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2H//////////",
                id="without_source",
            ),
            pytest.param(
                asset1,
                None,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAYAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2H//////////",
                id="with_source_public_key",
            ),
            pytest.param(
                asset1,
                None,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYf/////////8=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                asset1,
                None,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYf/////////8=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                liquidity_pool_asset,
                None,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAYAAAADAAAAAAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAB5//////////w==",
                id="liquidity_pool_asset",
            ),
            pytest.param(
                asset1,
                "0",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAYAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAAAAAAA",
                id="set_limit_to_0",
            ),
            pytest.param(
                asset1,
                "922337203685.4775807",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAYAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2H//////////",
                id="set_limit_to_max",
            ),
            pytest.param(
                asset1,
                Decimal("100.123456"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAYAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7raCA",
                id="with_limit_decimal",
            ),
        ],
    )
    def test_xdr(self, asset, limit, source, xdr):
        op = ChangeTrust(asset, limit, source)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
        assert op.asset == asset
        assert op.limit == str(limit) if limit is not None else "922337203685.4775807"

    def test_invalid_limit_raise(self):
        limit = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "limit" must have at most 7 digits after the decimal: {limit}',
        ):
            ChangeTrust(asset1, limit, kp1.public_key)
