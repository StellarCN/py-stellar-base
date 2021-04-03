import base64
import binascii

from .operation import Operation
from ..xdr import Xdr
from ..xdr.StellarXDR_type import ClaimableBalanceID


class ClawbackClaimableBalance(Operation):
    """The :class:`ClawbackClaimableBalance` object, which represents a ClawbackClaimableBalance operation on
    Stellar's network.

    Claws back a claimable balance

    Threshold: Medium

    :param balance_id: The claimable balance ID to be clawed back.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    def __init__(self, balance_id: str, source: str = None) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CLAWBACK_CLAIMABLE_BALANCE

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.CLAWBACK_CLAIMABLE_BALANCE

        balance_id_bytes: bytes = binascii.unhexlify(self.balance_id)
        balance_id = ClaimableBalanceID.from_xdr(base64.b64encode(balance_id_bytes))
        clawback_claimable_balance_op = Xdr.types.ClawbackClaimableBalanceOp(
            balanceID=balance_id
        )

        body.clawbackClaimableBalanceOp = clawback_claimable_balance_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ClawbackClaimableBalance":
        """Creates a :class:`ClawbackClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        balance_id = base64.b64decode(
            operation_xdr_object.body.clawbackClaimableBalanceOp.to_xdr()
        )
        balance_id = binascii.hexlify(balance_id).decode()
        op = cls(balance_id=balance_id, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
