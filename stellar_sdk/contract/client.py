from typing import Sequence

from ..soroban_server import SorobanServer
from ..client.base_sync_client import BaseSyncClient
from .. import xdr as stellar_xdr, InvokeHostFunction, Address
from .assembled_transaction import AssembledTransaction

NULL_ACCOUNT = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"


class Client:
    def __init__(
        self,
        contract_id: str,
        source_account: str,
        rpc_url: str,
        network_passphrase: str,
        request_client: BaseSyncClient = None,
    ):
        self.contract_id = contract_id
        self.source_account = source_account
        self.rpc_url = rpc_url
        self.network_passphrase = network_passphrase
        self.server = SorobanServer(rpc_url, request_client)

    def invoke(
        self,
        function_name: str,
        parameters: Sequence[stellar_xdr.SCVal],
        parse_result_xdr,
    ):
        if parameters is None:
            parameters = []

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT,
            invoke_contract=stellar_xdr.InvokeContractArgs(
                contract_address=Address(self.contract_id).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(
                    sc_symbol=function_name.encode("utf-8")
                ),
                args=list(parameters),
            ),
        )
        op = InvokeHostFunction(host_function=host_function, auth=[])
        return AssembledTransaction.build_with_operation(
            op,
            self.server,
            self.network_passphrase,
            self.source_account,
            parse_result_xdr,
        )
