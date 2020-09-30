import base64
import binascii

from .operation import Operation
from ..xdr import Xdr
from ..xdr.StellarXDR_type import ClaimableBalanceID


class ClaimClaimableBalance(Operation):
    """The :class:`ClaimClaimableBalance` object, which represents a ClaimClaimableBalance
    operation on Stellar's network.

    Claims a ClaimableBalanceEntry and adds the amount of asset on the entry to the source account.

    See `Claim Claimable Balance Documentation
    <https://developers.stellar.org/docs/start/list-of-operations/#claim-claimable-balance>_`.

    Threshold: Low

    :param balance_id: The claimable balance id to be claimed.
    :param source: The source account (defaults to transaction source).
    """

    def __init__(self, balance_id: str, source: str = None,) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CLAIM_CLAIMABLE_BALANCE

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.CLAIM_CLAIMABLE_BALANCE

        balance_id_bytes: bytes = binascii.unhexlify(self.balance_id)
        balance_id = ClaimableBalanceID.from_xdr(base64.b64encode(balance_id_bytes))
        claim_claimable_balance_op = Xdr.types.ClaimClaimableBalanceOp(
            balanceID=balance_id
        )

        body.claimClaimableBalanceOp = claim_claimable_balance_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ClaimClaimableBalance":
        """Creates a :class:`ClaimClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        balance_id = base64.b64decode(
            operation_xdr_object.body.claimClaimableBalanceOp.to_xdr()
        )
        balance_id = binascii.hexlify(balance_id).decode()
        op = cls(balance_id=balance_id, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
