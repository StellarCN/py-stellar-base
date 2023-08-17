from typing import List, Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..soroban.authorization_entry import AuthorizationEntry
from .operation import Operation

__all__ = ["InvokeHostFunction"]


class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        host_function: stellar_xdr.HostFunction,
        auth: List[AuthorizationEntry],
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.host_function = host_function
        self._auth: List[AuthorizationEntry] = auth

    # auth setter
    @property
    def auth(self) -> List[AuthorizationEntry]:
        return self._auth

    @auth.setter
    def auth(self, value: Union[List[AuthorizationEntry], List[str]]):
        for v in value:
            if isinstance(v, str):
                self._auth.append(
                    AuthorizationEntry.from_xdr_object(
                        stellar_xdr.SorobanAuthorizationEntry.from_xdr(v)
                    )
                )
            elif isinstance(v, AuthorizationEntry):
                self._auth.append(v)
            else:
                raise TypeError("Only AuthorizationEntry or str is allowed")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            host_function=self.host_function,
            auth=[auth.to_xdr_object() for auth in self.auth],
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
        auth = [
            AuthorizationEntry.from_xdr_object(auth)
            for auth in xdr_object.body.invoke_host_function_op.auth
        ]
        return cls(
            host_function=host_function,
            auth=auth,
            source=source,
        )

    def __str__(self):
        return f"<InvokeHostFunction [host_function={self.host_function}, auth={self.auth}, source={self.source}]>"
