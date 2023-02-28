from typing import Optional, Union, Sequence

from .operation import Operation
from .. import xdr as stellar_xdr
from stellar_sdk.soroban.contract_auth import ContractAuth
from ..muxed_account import MuxedAccount


__all__ = ["InvokeHostFunction"]


class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        function: stellar_xdr.HostFunction,
        auth: Sequence[Union[stellar_xdr.ContractAuth, ContractAuth]] = None,
        footprint: stellar_xdr.LedgerFootprint = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.footprint = (
            stellar_xdr.LedgerFootprint([], []) if footprint is None else footprint
        )
        self.function = function
        self.auth = []
        if auth:
            self.auth = [
                auth.to_xdr_object() if isinstance(auth, ContractAuth) else auth
                for auth in auth
            ]

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            function=self.function,
            # TODO: Figure out how to calculate this or get it from the user?
            footprint=self.footprint,
            auth=self.auth,
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
        auth = xdr_object.body.invoke_host_function_op.auth
        return cls(
            function=function,
            auth=auth,
            footprint=footprint,
            source=source,
        )

    def __str__(self):
        return (
            f"<InvokeHostFunction [function={self.function}, auth={self.auth}, "
            f"footprint={self.footprint}, source={self.source}]>"
        )
