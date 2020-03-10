from .operation import Operation

from ..xdr import xdr


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
    def type_code(cls) -> xdr.OperationType:
        return xdr.OperationType.INFLATION

    def _to_operation_body(self) -> xdr.OperationBody:
        body = xdr.OperationBody(type=self.type_code())
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "Inflation":
        """Creates a :class:`Inflation` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        return cls(source)
