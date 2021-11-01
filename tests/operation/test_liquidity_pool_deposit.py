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

    def test_invalid_liquidity_pool_id_raise(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380facainvalid"
        )
        max_amount_a = "10"
        max_amount_b = "20"
        min_price = "0.45"
        max_price = "0.55"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "liquidity_pool_id" is not a valid hash: {liquidity_pool_id}',
        ):
            LiquidityPoolDeposit(
                liquidity_pool_id,
                max_amount_a,
                max_amount_b,
                min_price,
                max_price,
                kp1.public_key,
            )

    def test_invalid_max_amount_a_raise(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        max_amount_a = "12345678902.23423324"
        max_amount_b = "20"
        min_price = "0.45"
        max_price = "0.55"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "max_amount_a" must have at most 7 digits after the decimal: {max_amount_a}',
        ):
            LiquidityPoolDeposit(
                liquidity_pool_id,
                max_amount_a,
                max_amount_b,
                min_price,
                max_price,
                kp1.public_key,
            )

    def test_invalid_max_amount_b_raise(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        max_amount_a = "10"
        max_amount_b = "12345678902.23423324"
        min_price = "0.45"
        max_price = "0.55"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "max_amount_b" must have at most 7 digits after the decimal: {max_amount_b}',
        ):
            LiquidityPoolDeposit(
                liquidity_pool_id,
                max_amount_a,
                max_amount_b,
                min_price,
                max_price,
                kp1.public_key,
            )
