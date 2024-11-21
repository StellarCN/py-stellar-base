from typing import Sequence

from .assembled_transaction import AssembledTransaction
from .. import xdr as stellar_xdr
from ..client.base_sync_client import BaseSyncClient
from ..soroban_server import SorobanServer
from ..transaction_builder import TransactionBuilder

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
        base_fee: int = 100,
    ):
        source = self.server.load_account(self.source_account)
        tx = (
            TransactionBuilder(source, self.network_passphrase, base_fee=base_fee)
            .append_invoke_contract_function_op(
                self.contract_id, function_name, parameters
            )
            .build()
        )
        return AssembledTransaction(tx, self.server, None, parse_result_xdr).simulate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()
