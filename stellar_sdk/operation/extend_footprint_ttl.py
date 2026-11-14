from typing import ClassVar

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["ExtendFootprintTTL"]


class ExtendFootprintTTL(Operation):
    """The :class:`ExtendFootprintTTL` object, which represents a ExtendFootprintTTL
    operation on Stellar's network.

    Threshold: Low

    See `Extend Footprint TTL <https://developers.stellar.org/docs/learn/fundamentals/transactions/list-of-operations#extend-footprint-ttl>`_.

    :param extend_to: The number of ledgers past the LCL (last closed ledger)
        by which to extend the validity of the ledger keys in this transaction.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: ClassVar[stellar_xdr.OperationType] = (
        stellar_xdr.OperationType.EXTEND_FOOTPRINT_TTL
    )

    def __init__(
        self, extend_to: int, source: MuxedAccount | str | None = None
    ) -> None:
        super().__init__(source)
        if extend_to < 0 or extend_to > 2**32 - 1:
            raise ValueError(
                f"`extend_to` value must be between 0 and 2**32-1, got {extend_to}"
            )

        self.extend_to: int = extend_to

    def _to_operation_body(self) -> stellar_xdr.OperationBody.Any:
        op = stellar_xdr.ExtendFootprintTTLOp(
            ext=stellar_xdr.ExtensionPoint.V0(),
            extend_to=self.extend_to,
        )
        body = stellar_xdr.OperationBody.ExtendFootprintTTL(op)
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "ExtendFootprintTTL":
        """Creates a :class:`ExtendFootprintTTL` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        body = xdr_object.body
        assert isinstance(body, stellar_xdr.OperationBody.ExtendFootprintTTL)
        extend_to = body.extend_footprint_ttl_op.extend_to
        op = cls(source=source, extend_to=extend_to)
        return op

    def __repr__(self):
        return (
            f"<ExtendFootprintTTL [extend_to={self.extend_to}, source={self.source}]>"
        )
