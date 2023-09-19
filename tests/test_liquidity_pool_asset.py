import pytest

from stellar_sdk import LIQUIDITY_POOL_FEE_V18, Asset, LiquidityPoolAsset
from stellar_sdk.xdr import AssetType, ChangeTrustAsset, LiquidityPoolType


class TestLiquidityPoolAsset:
    asset_a = Asset("ARST", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO")
    asset_b = Asset("USD", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ")
    fee = LIQUIDITY_POOL_FEE_V18

    def test_init(self):
        asset = LiquidityPoolAsset(self.asset_a, self.asset_b, fee=self.fee)
        assert asset.asset_a == self.asset_a
        assert asset.asset_b == self.asset_b
        assert asset.fee == self.fee
        assert asset.type == "liquidity_pool_shares"

    @pytest.mark.parametrize(
        "asset_a, asset_b, fee, msg",
        [
            (asset_b, asset_a, fee, "Assets are not in lexicographic order."),
            (asset_a, asset_b, fee + 10, "`fee` is invalid."),
        ],
    )
    def test_init_value_error_raise(self, asset_a, asset_b, fee, msg):
        with pytest.raises(ValueError, match=msg):
            LiquidityPoolAsset(asset_a, asset_b, fee)

    def test_to_change_trust_asset_xdr_object(self):
        asset = LiquidityPoolAsset(self.asset_a, self.asset_b, fee=self.fee)
        xdr_object = asset.to_change_trust_asset_xdr_object()
        assert isinstance(xdr_object, ChangeTrustAsset)
        assert xdr_object.type == AssetType.ASSET_TYPE_POOL_SHARE
        assert (
            xdr_object.liquidity_pool.type
            == LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT
        )
        assert (
            xdr_object.liquidity_pool.constant_product.asset_a
            == self.asset_a.to_xdr_object()
        )
        assert (
            xdr_object.liquidity_pool.constant_product.asset_b
            == self.asset_b.to_xdr_object()
        )
        assert xdr_object.liquidity_pool.constant_product.fee.int32 == self.fee
        assert asset == LiquidityPoolAsset.from_xdr_object(xdr_object)
        assert (
            xdr_object.to_xdr()
            == "AAAAAwAAAAAAAAABQVJTVAAAAAB/MGI0yYnp1n9p39kxGYtgDz1s5rZMIkBwH7YrCIMrhwAAAAFVU0QAAAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAHg=="
        )

    def test_liquidity_pool_id(self):
        asset = LiquidityPoolAsset(self.asset_a, self.asset_b, fee=self.fee)
        assert (
            asset.liquidity_pool_id
            == "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )

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
            LiquidityPoolAsset.from_xdr_object(asset.to_change_trust_asset_xdr_object())

    xlm = Asset.native()
    anum4 = Asset("USD", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ")
    anum12 = Asset("BANANA", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ")

    @pytest.mark.parametrize(
        "asset_a, asset_b, result",
        [
            (xlm, xlm, False),
            (xlm, anum4, True),
            (xlm, anum12, True),
            (anum4, xlm, False),
            (anum4, anum4, False),
            (anum4, anum12, True),
            (anum12, xlm, False),
            (anum12, anum4, False),
            (anum12, anum12, False),
        ],
    )
    def test_is_valid_lexicographic_order_asset_types(self, asset_a, asset_b, result):
        assert (
            LiquidityPoolAsset.is_valid_lexicographic_order(asset_a, asset_b) is result
        )

    asset_arst = Asset(
        "ARST", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO"
    )
    asset_usdx = Asset(
        "USDX", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO"
    )

    @pytest.mark.parametrize(
        "asset_a, asset_b, result",
        [
            (asset_arst, asset_arst, False),
            (asset_arst, asset_usdx, True),
            (asset_usdx, asset_arst, False),
            (asset_usdx, asset_usdx, False),
        ],
    )
    def test_is_valid_lexicographic_order_asset_code(self, asset_a, asset_b, result):
        assert (
            LiquidityPoolAsset.is_valid_lexicographic_order(asset_a, asset_b) == result
        )

    asset_issuer_a = Asset(
        "ARST", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO"
    )
    asset_issuer_b = Asset(
        "ARST", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
    )

    @pytest.mark.parametrize(
        "asset_a, asset_b, result",
        [
            (asset_issuer_a, asset_issuer_b, True),
            (asset_issuer_a, asset_issuer_a, False),
            (asset_issuer_b, asset_issuer_a, False),
            (asset_issuer_b, asset_issuer_b, False),
        ],
    )
    def test_is_valid_lexicographic_order_asset_issuer(self, asset_a, asset_b, result):
        assert (
            LiquidityPoolAsset.is_valid_lexicographic_order(asset_a, asset_b) == result
        )
