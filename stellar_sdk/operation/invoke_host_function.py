from typing import List, Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["InvokeHostFunction"]


class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        host_function: stellar_xdr.HostFunction,
        auth: List[stellar_xdr.SorobanAuthorizationEntry],
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.host_function = host_function
        self._auth: List[stellar_xdr.SorobanAuthorizationEntry] = auth

    # auth setter
    @property
    def auth(self) -> List[stellar_xdr.SorobanAuthorizationEntry]:
        return self._auth

    @auth.setter
    def auth(
        self, value: Union[List[stellar_xdr.SorobanAuthorizationEntry], List[str]]
    ):
        for v in value:
            if isinstance(v, str):
                self._auth.append(stellar_xdr.SorobanAuthorizationEntry.from_xdr(v))
            elif isinstance(
                v,
                stellar_xdr.SorobanAuthorizationEntry,
            ):
                self._auth.append(v)
            else:
                raise TypeError("Only SorobanAuthorizationEntry or str is allowed")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            host_function=self.host_function, auth=self.auth
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
        host_function = xdr_object.body.invoke_host_function_op.host_function
        auth = xdr_object.body.invoke_host_function_op.auth
        return cls(
            host_function=host_function,
            auth=auth,
            source=source,
        )

    def __str__(self):
        return f"<InvokeHostFunction [host_function={self.host_function}, auth={self.auth}, source={self.source}]>"
