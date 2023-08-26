import pytest

from stellar_sdk import Asset, LiquidityPoolId
from stellar_sdk.xdr import AssetType


class TestLiquidityPoolId:
    def test_init(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380faca"
        )
        asset = LiquidityPoolId(liquidity_pool_id)
        assert asset.liquidity_pool_id == liquidity_pool_id
        assert asset.type == "liquidity_pool_shares"

    def test_init_raise(self):
        with pytest.raises(
            ValueError,
            match=f'Value of argument "liquidity_pool_id" is not a valid hash: abc',
        ):
            LiquidityPoolId("abc")

    def test_asset_type(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380faca"
        )
        asset = LiquidityPoolId(liquidity_pool_id)
        assert asset.type == "liquidity_pool_shares"

    def test_to_trust_line_xdr_asset_object(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380faca"
        )
        asset = LiquidityPoolId(liquidity_pool_id)
        trust_line_asset_xdr_object = asset.to_trust_line_asset_xdr_object()
        assert (
            trust_line_asset_xdr_object.to_xdr()
            == "AAAAA917GrgxwnMxDdvsb5eHCqg8L714ziKt7Tfsv08zgPrK"
        )
        assert asset == LiquidityPoolId.from_xdr_object(trust_line_asset_xdr_object)

    @pytest.mark.parametrize(
        "asset_code, asset_issuer, asset_type",
        [
            ("XLM", None, AssetType.ASSET_TYPE_NATIVE),
            (
                "USD",
                "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ",
                AssetType.ASSET_TYPE_CREDIT_ALPHANUM4,
            ),
            (
                "BANANA",
                "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ",
                AssetType.ASSET_TYPE_CREDIT_ALPHANUM12,
            ),
        ],
    )
    def test_from_xdr_with_asset_xdr_raise(self, asset_code, asset_issuer, asset_type):
        asset = Asset(asset_code, asset_issuer)
        with pytest.raises(ValueError, match=f"Unexpected asset type: {asset_type}"):
            LiquidityPoolId.from_xdr_object(asset.to_trust_line_asset_xdr_object())
