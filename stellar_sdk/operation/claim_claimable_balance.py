import base64
import binascii
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..type_checked import type_checked
from ..utils import raise_if_not_valid_balance_id
from .operation import Operation

__all__ = ["ClaimClaimableBalance"]


@type_checked
class ClaimClaimableBalance(Operation):
    """The :class:`ClaimClaimableBalance` object, which represents a ClaimClaimableBalance
    operation on Stellar's network.

    Claims a ClaimableBalanceEntry and adds the amount of asset on the entry to the source account.

    Threshold: Low

    See `Claim Claimable Balance <https://developers.stellar.org/docs/start/list-of-operations/#claim-claimable-balance>`_ for more information.

    :param balance_id: The claimable balance id to be claimed.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.CLAIM_CLAIMABLE_BALANCE
    )

    def __init__(
        self,
        balance_id: str,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        self.balance_id: str = balance_id
        raise_if_not_valid_balance_id(self.balance_id, "balance_id")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        balance_id_bytes: bytes = binascii.unhexlify(self.balance_id)
        balance_id = stellar_xdr.ClaimableBalanceID.from_xdr_bytes(balance_id_bytes)
        claim_claimable_balance_op = stellar_xdr.ClaimClaimableBalanceOp(
            balance_id=balance_id
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            claim_claimable_balance_op=claim_claimable_balance_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "ClaimClaimableBalance":
        """Creates a :class:`ClaimClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.claim_claimable_balance_op is not None
        balance_id_bytes = base64.b64decode(
            xdr_object.body.claim_claimable_balance_op.to_xdr()
        )
        balance_id = binascii.hexlify(balance_id_bytes).decode()
        op = cls(balance_id=balance_id, source=source)
        return op

    def __str__(self):
        return f"<ClaimClaimableBalance [balance_id={self.balance_id}, source={self.source}]>"
