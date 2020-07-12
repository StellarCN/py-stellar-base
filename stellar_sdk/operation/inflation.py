from .operation import Operation
from ..xdr import Xdr


class Inflation(Operation):
    """The :class:`Inflation` object, which represents a
    Inflation operation on Stellar's network.

    This operation runs inflation.

    Threshold: Low

    :param str source: The source account (defaults to transaction source).

    """

    def __init__(self, source: str = None) -> None:
        super().__init__(source)

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.INFLATION

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.INFLATION
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "Inflation":
        """Creates a :class:`Inflation` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        op = cls(source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
