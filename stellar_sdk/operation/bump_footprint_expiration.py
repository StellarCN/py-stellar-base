from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["BumpFootprintExpiration"]


class BumpFootprintExpiration(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.BUMP_FOOTPRINT_EXPIRATION
    )

    def __init__(
        self, ledgers_to_expire: int, source: Optional[Union[MuxedAccount, str]] = None
    ) -> None:
        super().__init__(source)
        if ledgers_to_expire < 0 or ledgers_to_expire > 2**32 - 1:
            raise ValueError(
                f"`ledgers_to_expire` value must be between 0 and 2**32-1, got {ledgers_to_expire}"
            )

        self.ledgers_to_expire: int = ledgers_to_expire

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        op = stellar_xdr.BumpFootprintExpirationOp(
            ext=stellar_xdr.ExtensionPoint(0),
            ledgers_to_expire=stellar_xdr.Uint32(self.ledgers_to_expire),
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, bump_footprint_expiration_op=op
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "BumpFootprintExpiration":
        """Creates a :class:`BumpFootprintExpiration` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.bump_footprint_expiration_op is not None
        ledgers_to_expire = (
            xdr_object.body.bump_footprint_expiration_op.ledgers_to_expire.uint32
        )
        op = cls(source=source, ledgers_to_expire=ledgers_to_expire)
        return op

    def __str__(self):
        return f"<BumpFootprintExpiration [ledgers_to_expire={self.ledgers_to_expire}, source={self.source}]>"
