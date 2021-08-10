import base64
import binascii
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["ClawbackClaimableBalance"]


class ClawbackClaimableBalance(Operation):
    """The :class:`ClawbackClaimableBalance` object, which represents a ClawbackClaimableBalance operation on
    Stellar's network.

    Claws back a claimable balance

    Threshold: Medium

    :param balance_id: The claimable balance ID to be clawed back.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.CLAWBACK_CLAIMABLE_BALANCE
    )

    def __init__(
        self, balance_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        balance_id_bytes: bytes = binascii.unhexlify(self.balance_id)
        balance_id = stellar_xdr.ClaimableBalanceID.from_xdr_bytes(balance_id_bytes)
        clawback_claimable_balance_op = stellar_xdr.ClawbackClaimableBalanceOp(
            balance_id=balance_id
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            clawback_claimable_balance_op=clawback_claimable_balance_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "ClawbackClaimableBalance":
        """Creates a :class:`ClawbackClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.clawback_claimable_balance_op is not None
        balance_id_bytes = base64.b64decode(
            xdr_object.body.clawback_claimable_balance_op.to_xdr()
        )
        balance_id = binascii.hexlify(balance_id_bytes).decode()
        op = cls(balance_id=balance_id, source=source)
        return op

    def __str__(self):
        return f"<ClawbackClaimableBalance [balance_id={self.balance_id}, source={self.source}]>"
