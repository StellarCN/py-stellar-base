from . import xdr as stellar_xdr
from .asset import Asset
from .utils import sha256

__all__ = ["LiquidityPoolAsset", "LIQUIDITY_POOL_FEE_V18"]

#: LIQUIDITY_POOL_FEE_V18 is the default liquidity pool fee in protocol v18.
#: It defaults to 30 base points (0.3%).
LIQUIDITY_POOL_FEE_V18 = stellar_xdr.LIQUIDITY_POOL_FEE_V18


class LiquidityPoolAsset:
    """The :class:`LiquidityPoolAsset` object, which represents a liquidity pool trustline change.

    :param asset_a: The first asset in the Pool, it must respect the rule asset_a < asset_b.
        See :func:`stellar_sdk.liquidity_pool_asset.LiquidityPoolAsset.is_valid_lexicographic_order`
        for more details on how assets are sorted.
    :param asset_b: The second asset in the Pool, it must respect the rule asset_a < asset_b.
        See :func:`stellar_sdk.liquidity_pool_asset.LiquidityPoolAsset.is_valid_lexicographic_order`
        for more details on how assets are sorted.
    :param fee: The liquidity pool fee. For now the only fee supported is `30`.
    :raise: :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
    """

    def __init__(
        self, asset_a: Asset, asset_b: Asset, fee: int = LIQUIDITY_POOL_FEE_V18
    ) -> None:
        if not self.is_valid_lexicographic_order(asset_a, asset_b):
            raise ValueError("`Assets are not in lexicographic order.")

        if fee != LIQUIDITY_POOL_FEE_V18:
            raise ValueError("`fee` is invalid.")

        self.type: str = "liquidity_pool_shares"
        self.asset_a: Asset = asset_a
        self.asset_b: Asset = asset_b
        self.fee: int = fee

    @property
    def liquidity_pool_id(self) -> str:
        """Computes the liquidity pool id for current instance.

        :return: Liquidity pool id.
        """
        return self._liquidity_pool_id_bytes.hex()

    @staticmethod
    def is_valid_lexicographic_order(asset_a: Asset, asset_b: Asset) -> bool:
        """Compares if asset_a < asset_b according with the criteria:

        1. First compare the type (eg. native before alphanum4 before alphanum12).
        2. If the types are equal, compare the assets codes.
        3. If the asset codes are equal, compare the issuers.

        :param asset_a: The first asset in the lexicographic order.
        :param asset_b: The second asset in the lexicographic order.
        :return: return `True` if asset_a < asset_b
        """
        if asset_a == asset_b:
            return False

        # Compare asset types.
        if asset_a.type == "native":
            return True
        elif asset_a.type == "credit_alphanum4":
            if asset_b.type == "native":
                return False
            if asset_b.type == "credit_alphanum12":
                return True
        else:
            # asset_a.type == "credit_alphanum12"
            if asset_b.type != "credit_alphanum12":
                return False

        # Compare asset codes.
        if asset_a.code != asset_b.code:
            assert asset_a.code is not None
            assert asset_b.code is not None
            return asset_a.code < asset_b.code

        # Compare asset issuer.
        assert asset_a.issuer is not None
        assert asset_b.issuer is not None
        return asset_a.issuer < asset_b.issuer

    def to_change_trust_asset_xdr_object(self) -> stellar_xdr.ChangeTrustAsset:
        """Returns the xdr object for this ChangeTrustAsset object.

        :return: XDR ChangeTrustAsset object
        """
        liquidity_pool_parameters = self._liquidity_pool_parameters()
        return stellar_xdr.ChangeTrustAsset(
            stellar_xdr.AssetType.ASSET_TYPE_POOL_SHARE,
            liquidity_pool=liquidity_pool_parameters,
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.ChangeTrustAsset
    ) -> "LiquidityPoolAsset":
        """Create a :class:`LiquidityPoolAsset` from an XDR ChangeTrustAsset object.

        :param xdr_object: The XDR ChangeTrustAsset object.
        :return: A new :class:`LiquidityPoolAsset` object from the given XDR ChangeTrustAsset object.
        """
        asset_type = xdr_object.type
        if asset_type == stellar_xdr.AssetType.ASSET_TYPE_POOL_SHARE:
            assert xdr_object.liquidity_pool is not None
            assert xdr_object.liquidity_pool.constant_product is not None
            asset_a = Asset.from_xdr_object(
                xdr_object.liquidity_pool.constant_product.asset_a
            )
            asset_b = Asset.from_xdr_object(
                xdr_object.liquidity_pool.constant_product.asset_b
            )
            fee = xdr_object.liquidity_pool.constant_product.fee.int32
            return cls(asset_a, asset_b, fee)
        else:
            raise ValueError(f"Unexpected asset type: {asset_type}")

    @property
    def _liquidity_pool_id_bytes(self) -> bytes:
        liquidity_pool_parameters = self._liquidity_pool_parameters()
        return sha256(liquidity_pool_parameters.to_xdr_bytes())

    def _liquidity_pool_parameters(self) -> stellar_xdr.LiquidityPoolParameters:
        liquidity_pool_constant_product_parameters = (
            stellar_xdr.LiquidityPoolConstantProductParameters(
                self.asset_a.to_xdr_object(),
                self.asset_b.to_xdr_object(),
                stellar_xdr.Int32(self.fee),
            )
        )
        return stellar_xdr.LiquidityPoolParameters(
            stellar_xdr.LiquidityPoolType.LIQUIDITY_POOL_CONSTANT_PRODUCT,
            liquidity_pool_constant_product_parameters,
        )

    def __hash__(self):
        return hash((self.asset_a, self.asset_b, self.fee, self.type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.asset_a == other.asset_a
            and self.asset_b == other.asset_b
            and self.fee == other.fee
        )

    def __repr__(self):
        return f"<LiquidityPoolAsset [asset_a={self.asset_a}, asset_b={self.asset_b}, fee={self.fee}, type={self.type}]>"
