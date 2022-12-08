from typing import Optional, Union, Sequence

from .operation import Operation
from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from stellar_sdk.soroban_types.base import BaseScValAlias
from ..type_checked import type_checked

__all__ = ["InvokeHostFunction"]


@type_checked
class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        function: stellar_xdr.HostFunction,
        footprint: stellar_xdr.LedgerFootprint = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.footprint = (
            stellar_xdr.LedgerFootprint([], []) if footprint is None else footprint
        )
        self.function = function

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            function=self.function,
            # TODO: Figure out how to calculate this or get it from the user?
            footprint=self.footprint,
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            invoke_host_function_op=invoke_host_function_op,
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "InvokeHostFunction":
        """Creates a :class:`InvokeHostFunction` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.invoke_host_function_op is not None
        function = xdr_object.body.invoke_host_function_op.function
        footprint = xdr_object.body.invoke_host_function_op.footprint
        return cls(
            function=function,
            footprint=footprint,
            source=source,
        )

    def __str__(self):
        return (
            f"<InvokeHostFunction [function={self.function}, "
            f"footprint={self.footprint}, source={self.source}]>"
        )
