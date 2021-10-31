from decimal import Decimal

import pytest

from stellar_sdk import LiquidityPoolDeposit, Operation, Price

from . import *


class TestLiquidityPoolDeposit:
    @pytest.mark.parametrize(
        "max_amount_a, max_amount_b, min_price, max_price, source, xdr",
        [
            pytest.param(
                "10",
                "20",
                "0.45",
                "0.55",
                None,
                "AAAAAAAAABZhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU",
                id="without_source",
            ),
            pytest.param(
                "10",
                "20",
                "0.45",
                "0.55",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABZhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU",
                id="with_source_public_key",
            ),
            pytest.param(
                "10",
                "20",
                "0.45",
                "0.55",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFmGQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAX14QAAAAAAC+vCAAAAAAkAAAAUAAAACwAAABQ=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "10",
                "20",
                "0.45",
                "0.55",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFmGQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAX14QAAAAAAC+vCAAAAAAkAAAAUAAAACwAAABQ=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("10"),
                Decimal("20"),
                Decimal("0.45"),
                Decimal("0.55"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABZhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU",
                id="decimal",
            ),
            pytest.param(
                Decimal("10"),
                Decimal("20"),
                Price.from_raw_price("0.45"),
                Price.from_raw_price("0.55"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABZhkAmY8Wp5fhwduy6yGgFlfaWObMLyutxMHveQ8XoiygAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU",
                id="price",
            ),
        ],
    )
    def test_xdr(self, max_amount_a, max_amount_b, min_price, max_price, source, xdr):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        op = LiquidityPoolDeposit(
            liquidity_pool_id, max_amount_a, max_amount_b, min_price, max_price, source
        )
        assert op.liquidity_pool_id == liquidity_pool_id
        assert op.max_amount_a == str(max_amount_a)
        assert op.max_amount_b == str(max_amount_b)
        assert (
            op.max_price == max_price
            if isinstance(max_price, Price)
            else Price.from_raw_price(max_price)
        )
        assert (
            op.min_price == min_price
            if isinstance(min_price, Price)
            else Price.from_raw_price(min_price)
        )
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
