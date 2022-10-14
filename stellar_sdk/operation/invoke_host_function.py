import binascii
from typing import Optional, Union, List

from .operation import Operation
from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..type_checked import type_checked

__all__ = ["InvokeHostFunction"]


@type_checked
class InvokeHostFunction(Operation):
    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.INVOKE_HOST_FUNCTION
    )

    def __init__(
        self,
        contract_id: str,
        method: str,
        params: List[stellar_xdr.SCVal],
        footprint: stellar_xdr.LedgerFootprint,
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.contract_id = contract_id
        self.method = method  # TODO: method, str only?
        self.footprint = footprint
        self.params = params

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        invoke_host_function_op = stellar_xdr.InvokeHostFunctionOp(
            function=stellar_xdr.HostFunction.HOST_FN_CALL,
            parameters=stellar_xdr.SCVec(
                sc_vec=[
                    stellar_xdr.SCVal(
                        stellar_xdr.SCValType.SCV_OBJECT,
                        obj=stellar_xdr.SCObject(
                            stellar_xdr.SCObjectType.SCO_BYTES,
                            bin=binascii.unhexlify(self.contract_id),
                        ),
                    ),
                    stellar_xdr.SCVal(
                        stellar_xdr.SCValType.SCV_SYMBOL,
                        sym=stellar_xdr.SCSymbol(sc_symbol=self.method.encode("utf-8")),
                    ),
                    *self.params,
                ]
            ),
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
        assert (
            xdr_object.body.invoke_host_function_op.parameters.sc_vec[0].obj is not None
        )
        assert (
            xdr_object.body.invoke_host_function_op.parameters.sc_vec[0].obj.bin
            is not None
        )
        contract_id = binascii.hexlify(
            xdr_object.body.invoke_host_function_op.parameters.sc_vec[0].obj.bin
        ).decode("utf-8")
        assert (
            xdr_object.body.invoke_host_function_op.parameters.sc_vec[1].sym is not None
        )
        method = xdr_object.body.invoke_host_function_op.parameters.sc_vec[
            1
        ].sym.sc_symbol.decode("utf-8")
        params = xdr_object.body.invoke_host_function_op.parameters.sc_vec[2:]
        footprint = xdr_object.body.invoke_host_function_op.footprint
        return cls(
            contract_id=contract_id,
            method=method,
            params=params,
            footprint=footprint,
            source=source,
        )

    def __str__(self):
        return (
            f"<InvokeHostFunction [contract_id={self.contract_id}, method={self.method}, "
            f"params={self.params}, footprint={self.footprint}, source={self.source}]>"
        )
