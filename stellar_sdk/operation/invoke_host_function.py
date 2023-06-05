from typing import Optional, Union, Sequence, List

from .operation import Operation
from .. import xdr as stellar_xdr
from ..soroban.contract_auth import ContractAuth
from ..muxed_account import MuxedAccount

__all__ = ["InvokeHostFunction"]


class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        functions: List[stellar_xdr.HostFunction],
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.functions = functions

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            functions=self.functions
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
        functions = xdr_object.body.invoke_host_function_op.functions
        return cls(
            functions=functions,
            source=source,
        )

    def __str__(self):
        return (
            f"<InvokeHostFunction [functions={self.functions}, source={self.source}]>"
        )
