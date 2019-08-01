from .operation import Operation

from ..stellarxdr import Xdr


class BumpSequence(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.BUMP_SEQUENCE

    def __init__(self, bump_to: int, source: str = None) -> None:
        super().__init__(source)
        self.bump_to = bump_to

    def to_operation_body(self) -> Xdr.nullclass:
        bump_sequence_op = Xdr.types.BumpSequenceOp(self.bump_to)
        body = Xdr.nullclass()
        body.type = Xdr.const.BUMP_SEQUENCE
        body.bumpSequenceOp = bump_sequence_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'BumpSequence':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        bump_to = op_xdr_object.body.bumpSequenceOp.bumpTo
        return cls(source=source, bump_to=bump_to)
