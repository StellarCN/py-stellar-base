from .operation import Operation
from ..xdr import Xdr


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

    def __init__(self, bump_to: int, source: str = None) -> None:
        super().__init__(source)
        self.bump_to: int = bump_to

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.BUMP_SEQUENCE

    def _to_operation_body(self) -> Xdr.nullclass:
        bump_sequence_op = Xdr.types.BumpSequenceOp(self.bump_to)
        body = Xdr.nullclass()
        body.type = Xdr.const.BUMP_SEQUENCE
        body.bumpSequenceOp = bump_sequence_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "BumpSequence":
        """Creates a :class:`BumpSequence` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        bump_to = operation_xdr_object.body.bumpSequenceOp.bumpTo
        op = cls(source=source, bump_to=bump_to)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
