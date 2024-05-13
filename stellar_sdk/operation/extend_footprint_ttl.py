from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["ExtendFootprintTTL"]


class ExtendFootprintTTL(Operation):
    """The :class:`ExtendFootprintTTL` object, which represents a ExtendFootprintTTL
    operation on Stellar's network.

    Threshold: Low

    See `ExtendFootprintTTLOp <https://soroban.stellar.org/docs/fundamentals-and-concepts/state-expiration#ExtendFootprintTTLop>`_.

    :param extend_to: The number of ledgers past the LCL (last closed ledger)
        by which to extend the validity of the ledger keys in this transaction.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.EXTEND_FOOTPRINT_TTL
    )

    def __init__(
        self, extend_to: int, source: Optional[Union[MuxedAccount, str]] = None
    ) -> None:
        super().__init__(source)
        if extend_to < 0 or extend_to > 2**32 - 1:
            raise ValueError(
                f"`extend_to` value must be between 0 and 2**32-1, got {extend_to}"
            )

        self.extend_to: int = extend_to

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        op = stellar_xdr.ExtendFootprintTTLOp(
            ext=stellar_xdr.ExtensionPoint(0),
            extend_to=stellar_xdr.Uint32(self.extend_to),
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, extend_footprint_ttl_op=op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "ExtendFootprintTTL":
        """Creates a :class:`ExtendFootprintTTL` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.extend_footprint_ttl_op is not None
        extend_to = xdr_object.body.extend_footprint_ttl_op.extend_to.uint32
        op = cls(source=source, extend_to=extend_to)
        return op

    def __repr__(self):
        return (
            f"<ExtendFootprintTTL [extend_to={self.extend_to}, source={self.source}]>"
        )
