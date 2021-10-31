from decimal import Decimal

import pytest

from stellar_sdk import LiquidityPoolWithdraw, Operation, Price

from . import *


class TestLiquidityPoolWithdraw:
    @pytest.mark.parametrize(
        "amount, min_amount_a, min_amount_b, source, xdr",
        [
            pytest.param(
                "5",
                "10",
                "20",
                None,
                "AAAAAAAAABdhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAC+vCAAAAAAAX14QAAAAAAC+vCAA==",
                id="without_source",
            ),
            pytest.param(
                "5",
                "10",
                "20",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABdhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAC+vCAAAAAAAX14QAAAAAAC+vCAA==",
                id="with_source_public_key",
            ),
            pytest.param(
                "5",
                "10",
                "20",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAF2GQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAL68IAAAAAABfXhAAAAAAAL68IA",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "5",
                "10",
                "20",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAF2GQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAL68IAAAAAABfXhAAAAAAAL68IA",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("5"),
                Decimal("10"),
                Decimal("20"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABdhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAC+vCAAAAAAAX14QAAAAAAC+vCAA==",
                id="decimal",
            ),
        ],
    )
    def test_xdr(self, amount, min_amount_a, min_amount_b, source, xdr):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        op = LiquidityPoolWithdraw(
            liquidity_pool_id, amount, min_amount_a, min_amount_b, source
        )
        assert op.liquidity_pool_id == liquidity_pool_id
        assert op.amount == str(amount)
        assert op.min_amount_a == str(min_amount_a)
        assert op.min_amount_b == str(min_amount_b)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
