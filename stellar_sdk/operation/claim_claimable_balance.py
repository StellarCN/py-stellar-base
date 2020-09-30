import binascii

from .operation import Operation
from ..xdr import Xdr


class ClaimClaimableBalance(Operation):
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
        balance_id = Xdr.nullclass()
        balance_id.type = Xdr.const.CLAIMABLE_BALANCE_ID_TYPE_V0  # int32
        balance_id.v0 = balance_id_bytes[4:]
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
        balance_id = b"\x00" * 4 + operation_xdr_object.body.claimClaimableBalanceOp.v0
        balance_id = binascii.hexlify(balance_id).decode()
        op = cls(balance_id=balance_id, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
