from typing import ClassVar

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..utils import raise_if_not_valid_balance_id
from .operation import Operation

__all__ = ["ClawbackClaimableBalance"]


class ClawbackClaimableBalance(Operation):
    """The :class:`ClawbackClaimableBalance` object, which represents a ClawbackClaimableBalance operation on
    Stellar's network.

    Claws back a claimable balance

    Threshold: Medium

    See `Clawback Claimable Balance <https://developers.stellar.org/docs/learn/fundamentals/transactions/list-of-operations#clawback-claimable-balance>`_ for more information.

    :param balance_id: The claimable balance ID to be clawed back.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: ClassVar[stellar_xdr.OperationType] = (
        stellar_xdr.OperationType.CLAWBACK_CLAIMABLE_BALANCE
    )

    def __init__(
        self, balance_id: str, source: MuxedAccount | str | None = None
    ) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id
        raise_if_not_valid_balance_id(self.balance_id, "balance_id")

    def _to_operation_body(self) -> stellar_xdr.OperationBody.Any:
        balance_id = stellar_xdr.ClaimableBalanceID.from_xdr_bytes(
            bytes.fromhex(self.balance_id)
        )
        return stellar_xdr.OperationBody.ClawbackClaimableBalance(
            stellar_xdr.ClawbackClaimableBalanceOp(balance_id=balance_id)
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "ClawbackClaimableBalance":
        """Creates a :class:`ClawbackClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        body = xdr_object.body
        assert isinstance(body, stellar_xdr.OperationBody.ClawbackClaimableBalance)
        balance_id = body.clawback_claimable_balance_op.balance_id.to_xdr_bytes().hex()
        return cls(balance_id=balance_id, source=source)

    def __repr__(self):
        return f"<ClawbackClaimableBalance [balance_id={self.balance_id}, source={self.source}]>"
