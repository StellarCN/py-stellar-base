from typing import ClassVar

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["RestoreFootprint"]


class RestoreFootprint(Operation):
    """The :class:`RestoreFootprint` object, which represents a RestoreFootprint
    operation on Stellar's network.

    Threshold: Low

    See `Restore Footprint <https://developers.stellar.org/docs/learn/fundamentals/transactions/list-of-operations#restore-footprint>`_.

    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: ClassVar[stellar_xdr.OperationType] = (
        stellar_xdr.OperationType.RESTORE_FOOTPRINT
    )

    def __init__(self, source: MuxedAccount | str | None = None) -> None:
        super().__init__(source)

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        op = stellar_xdr.RestoreFootprintOp(
            ext=stellar_xdr.ExtensionPoint(0),
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, restore_footprint_op=op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "RestoreFootprint":
        """Creates a :class:`RestoreFootprint` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        op = cls(source=source)
        return op

    def __repr__(self):
        return f"<RestoreFootprint [source={self.source}]>"
