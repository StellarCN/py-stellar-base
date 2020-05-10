from typing import Union

from .operation import Operation
from ..muxed_account import MuxedAccount
from ..xdr import xdr


class Inflation(Operation):
    """The :class:`Inflation` object, which represents a
    Inflation operation on Stellar's network.

    This operation runs inflation.

    Threshold: Low

    :param str source: The source account (defaults to transaction source).

    """

    TYPE_CODE = xdr.OperationType.INFLATION

    def __init__(self, source: Union[MuxedAccount, str] = None) -> None:
        super().__init__(source)

    def _to_operation_body(self) -> xdr.OperationBody:
        body = xdr.OperationBody(type=self.TYPE_CODE)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "Inflation":
        """Creates a :class:`Inflation` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        return cls(source)
