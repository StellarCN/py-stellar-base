from decimal import Decimal

import pytest

from stellar_sdk import LiquidityPoolWithdraw, Operation

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

    def test_invalid_liquidity_pool_id_raise(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380facainvalid"
        )
        amount = "5"
        min_amount_a = "10"
        min_amount_b = "20"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "liquidity_pool_id" is not a valid hash: {liquidity_pool_id}',
        ):
            LiquidityPoolWithdraw(
                liquidity_pool_id, amount, min_amount_a, min_amount_b, kp1.public_key
            )

    def test_invalid_amount_raise(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        amount = "12345678902.23423324"
        min_amount_a = "10"
        min_amount_b = "20"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "amount" must have at most 7 digits after the decimal: {amount}',
        ):
            LiquidityPoolWithdraw(
                liquidity_pool_id, amount, min_amount_a, min_amount_b, kp1.public_key
            )

    def test_invalid_min_amount_a_raise(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        amount = "5"
        min_amount_a = "12345678902.23423324"
        min_amount_b = "20"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "min_amount_a" must have at most 7 digits after the decimal: {min_amount_a}',
        ):
            LiquidityPoolWithdraw(
                liquidity_pool_id, amount, min_amount_a, min_amount_b, kp1.public_key
            )

    def test_invalid_min_amount_b_raise(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        amount = "5"
        min_amount_a = "10"
        min_amount_b = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "min_amount_b" must have at most 7 digits after the decimal: {min_amount_b}',
        ):
            LiquidityPoolWithdraw(
                liquidity_pool_id, amount, min_amount_a, min_amount_b, kp1.public_key
            )
