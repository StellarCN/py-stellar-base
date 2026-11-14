from stellar_sdk import (
    Operation,
    scval,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.operation import InvokeHostFunction
from tests.operation.helpers import (
    check_source,
    kp1,
)


class TestInvokeHostFunction:
    def test_xdr_without_auth(self):
        contract_id = "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"
        function_name = "increment"
        host_function = stellar_xdr.HostFunction.InvokeContract(
            stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=function_name,
                args=[scval.to_int256(234325465)],
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
        host_function = stellar_xdr.HostFunction.InvokeContract(
            stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=function_name,
                args=[scval.to_int256(234325465)],
            )
        )

        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials.SourceAccount(),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction.ContractFn(
                        stellar_xdr.InvokeContractArgs(
                            contract_address=Address(
                                "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                            ).to_xdr_sc_address(),
                            function_name=stellar_xdr.SCSymbol(b"increment"),
                            args=[],
                        )
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
