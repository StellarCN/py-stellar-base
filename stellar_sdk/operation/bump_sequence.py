from typing import Union

from .operation import Operation
from ..muxed_account import MuxedAccount
from ..xdr import xdr


class BumpSequence(Operation):
    """The :class:`BumpSequence` object, which represents a
    BumpSequence operation on Stellar's network.

    Bump sequence allows to bump forward the sequence number of the source account of the
    operation, allowing to invalidate any transactions with a smaller sequence number.
    If the specified bumpTo sequence number is greater than the source account’s sequence number,
    the account’s sequence number is updated with that value, otherwise it’s not modified.

    Threshold: Low

    :param bump_to: Sequence number to bump to.
    :param source: The optional source account.

    """

    TYPE_CODE = xdr.OperationType.BUMP_SEQUENCE

    def __init__(self, bump_to: int, source: Union[MuxedAccount, str] = None) -> None:
        super().__init__(source)
        self.bump_to: int = bump_to

    def _to_operation_body(self) -> xdr.OperationBody:
        sequence = xdr.SequenceNumber(xdr.Int64(self.bump_to))
        bump_sequence_op = xdr.BumpSequenceOp(sequence)
        body = xdr.OperationBody(type=self.TYPE_CODE, bump_sequence_op=bump_sequence_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "BumpSequence":
        """Creates a :class:`BumpSequence` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        bump_to = (
            operation_xdr_object.body.bump_sequence_op.bump_to.sequence_number.int64
        )
        return cls(source=source, bump_to=bump_to)
