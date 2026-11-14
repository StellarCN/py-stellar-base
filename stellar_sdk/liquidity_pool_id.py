import binascii

from . import xdr as stellar_xdr
from .utils import raise_if_not_valid_hash

__all__ = ["LiquidityPoolId"]


class LiquidityPoolId:
    """The :class:`LiquidityPoolId` object, which represents the asset referenced by a trustline to a liquidity pool.

    :param liquidity_pool_id: The ID of the liquidity pool in hex string.
    :raise: :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
    """

    def __init__(self, liquidity_pool_id: str) -> None:
        self.liquidity_pool_id: str = liquidity_pool_id
        self.type: str = "liquidity_pool_shares"
        raise_if_not_valid_hash(self.liquidity_pool_id, "liquidity_pool_id")

    def to_trust_line_asset_xdr_object(self) -> stellar_xdr.TrustLineAsset.Any:
        """Returns the xdr object for this LiquidityPoolId object.

        :return: XDR TrustLineAsset object
        """
        liquidity_pool_id_bytes = binascii.unhexlify(self.liquidity_pool_id)
        liquidity_pool_id = stellar_xdr.PoolID.from_xdr_bytes(liquidity_pool_id_bytes)
        return stellar_xdr.TrustLineAsset.PoolShare(liquidity_pool_id)

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.TrustLineAsset.Any
    ) -> "LiquidityPoolId":
        """Create a :class:`LiquidityPoolId` from an XDR Asset object.

        :param xdr_object: The XDR TrustLineAsset object.
        :return: A new :class:`LiquidityPoolId` object from the given XDR TrustLineAsset object.
        """
        if not isinstance(xdr_object, stellar_xdr.TrustLineAsset.PoolShare):
            raise ValueError(f"Unexpected asset type: {xdr_object.type}")
        liquidity_pool_id = xdr_object.liquidity_pool_id.hex()
        return cls(liquidity_pool_id)

    def __hash__(self):
        return hash((self.liquidity_pool_id, self.type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liquidity_pool_id == other.liquidity_pool_id

    def __repr__(self):
        return f"<LiquidityPoolId [liquidity_pool_id={self.liquidity_pool_id}]>"
