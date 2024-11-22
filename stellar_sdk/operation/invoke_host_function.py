from typing import List, Optional, Sequence, Union

from .. import xdr as stellar_xdr
from ..address import Address
from ..muxed_account import MuxedAccount
from ..strkey import StrKey
from .operation import Operation

__all__ = ["InvokeHostFunction"]


class InvokeHostFunction(Operation):
    """The :class:`InvokeHostFunction` object, which represents a InvokeHostFunction
    operation on Stellar's network.

    Threshold: Medium

    See `Interacting with Soroban via Stellar <https://soroban.stellar.org/docs/fundamentals-and-concepts/invoking-contracts-with-transactions>`_.

    :param host_function: The host function to invoke.
    :param auth: The authorizations required to execute the host function.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        host_function: stellar_xdr.HostFunction,
        auth: Sequence[stellar_xdr.SorobanAuthorizationEntry] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.host_function = host_function
        self.auth: List[stellar_xdr.SorobanAuthorizationEntry] = (
            list(auth) if auth else []
        )

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

    @classmethod
    def invoke_contract_function(
        cls,
        contract_id: str,
        function_name: str,
        parameters: Sequence[stellar_xdr.SCVal] = None,
        auth: Sequence[stellar_xdr.SorobanAuthorizationEntry] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "InvokeHostFunction":
        """Create a new :class:`InvokeHostFunction` operation.

        :param contract_id: The ID of the contract to invoke.
        :param function_name: The name of the function to invoke.
        :param parameters: The parameters to pass to the method.
        :param auth: The authorizations required to execute the host function.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        """
        if not StrKey.is_valid_contract(contract_id):
            raise ValueError("`contract_id` is invalid.")

        if parameters is None:
            parameters = []

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT,
            invoke_contract=stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(
                    sc_symbol=function_name.encode("utf-8")
                ),
                args=list(parameters),
            ),
        )
        return cls(host_function=host_function, auth=auth, source=source)

    def __repr__(self):
        return f"<InvokeHostFunction [host_function={self.host_function}, auth={self.auth}, source={self.source}]>"
