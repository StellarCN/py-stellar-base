from typing import ClassVar

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..utils import raise_if_not_valid_balance_id
from .operation import Operation

__all__ = ["ClaimClaimableBalance"]


class ClaimClaimableBalance(Operation):
    """The :class:`ClaimClaimableBalance` object, which represents a ClaimClaimableBalance
    operation on Stellar's network.

    Claims a ClaimableBalanceEntry and adds the amount of asset on the entry to the source account.

    Threshold: Low

    See `Claim Claimable Balance <https://developers.stellar.org/docs/learn/fundamentals/transactions/list-of-operations#claim-claimable-balance>`_ for more information.

    :param balance_id: The claimable balance id to be claimed.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: ClassVar[stellar_xdr.OperationType] = (
        stellar_xdr.OperationType.CLAIM_CLAIMABLE_BALANCE
    )

    def __init__(
        self,
        balance_id: str,
        source: MuxedAccount | str | None = None,
    ) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id
        raise_if_not_valid_balance_id(self.balance_id, "balance_id")

    def _to_operation_body(self) -> stellar_xdr.OperationBody.Any:
        balance_id = stellar_xdr.ClaimableBalanceID.from_xdr_bytes(
            bytes.fromhex(self.balance_id)
        )
        return stellar_xdr.OperationBody.ClaimClaimableBalance(
            stellar_xdr.ClaimClaimableBalanceOp(balance_id=balance_id)
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "ClaimClaimableBalance":
        """Creates a :class:`ClaimClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        body = xdr_object.body
        assert isinstance(body, stellar_xdr.OperationBody.ClaimClaimableBalance)
        balance_id = body.claim_claimable_balance_op.balance_id.to_xdr_bytes().hex()
        return cls(balance_id=balance_id, source=source)

    def __repr__(self):
        return f"<ClaimClaimableBalance [balance_id={self.balance_id}, source={self.source}]>"
