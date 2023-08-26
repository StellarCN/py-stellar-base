from stellar_sdk import Operation, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.operation import InvokeHostFunction

from . import *


class TestInvokeHostFunction:
    def test_xdr_without_auth(self):
        contract_id = "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"
        function_name = "increment"
        invoke_params = [
            Address(contract_id).to_xdr_sc_val(),
            stellar_xdr.SCVal.from_scv_symbol(
                sym=stellar_xdr.SCSymbol(sc_symbol=function_name.encode("utf-8")),
            ),
            scval.to_int256(234325465),
        ]
        host_function = (
            stellar_xdr.HostFunction.from_host_function_type_invoke_contract(
                stellar_xdr.SCVec(invoke_params)
            )
        )
        op = InvokeHostFunction(host_function, [], source=kp1.public_key)
        assert op.host_function == host_function
        assert op.auth == []
        check_source(op.source, kp1.public_key)
        xdr_object = op.to_xdr_object()
        assert Operation.from_xdr_object(xdr_object) == op

    def test_xdr_auth(self):
        contract_id = "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"
        function_name = "increment"
        invoke_params = [
            Address(contract_id).to_xdr_sc_val(),
            stellar_xdr.SCVal.from_scv_symbol(
                sym=stellar_xdr.SCSymbol(sc_symbol=function_name.encode("utf-8")),
            ),
            scval.to_int256(234325465),
        ]
        host_function = (
            stellar_xdr.HostFunction.from_host_function_type_invoke_contract(
                stellar_xdr.SCVec(invoke_params)
            )
        )

        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials.from_soroban_credentials_source_account(),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction(
                        type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                        contract_fn=stellar_xdr.SorobanAuthorizedContractFunction(
                            contract_address=Address(
                                "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                            ).to_xdr_sc_address(),
                            function_name=stellar_xdr.SCSymbol(b"increment"),
                            args=stellar_xdr.SCVec([]),
                        ),
                    ),
                    sub_invocations=[],
                ),
            )
        ]
        op = InvokeHostFunction(host_function, auth, source=kp1.public_key)
        assert op.host_function == host_function
        assert op.auth == auth
        check_source(op.source, kp1.public_key)
        xdr_object = op.to_xdr_object()
        assert Operation.from_xdr_object(xdr_object) == op
