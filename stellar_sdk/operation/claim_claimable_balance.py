from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount
from ..asset import Asset
from ..xdr import Xdr


class ClaimClaimableBalance(Operation):
    def __init__(self, balance_id: str, source: str = None,) -> None:
        super().__init__(source)
        self.balance_id = balance_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CLAIM_CLAIMABLE_BALANCE

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.CLAIM_CLAIMABLE_BALANCE

        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ClaimClaimableBalance":
        """Creates a :class:`ClaimClaimableBalance` object from an XDR Operation
        object.

        """
        pass