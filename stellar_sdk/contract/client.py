from typing import Callable, Optional, Sequence, TypeVar, Union

from .. import Account, Keypair, MuxedAccount
from .. import xdr as stellar_xdr
from ..client.base_sync_client import BaseSyncClient
from ..soroban_server import SorobanServer
from ..transaction_builder import TransactionBuilder
from .assembled_transaction import AssembledTransaction

NULL_ACCOUNT = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"

__all__ = ["Client", "NULL_ACCOUNT"]

T = TypeVar("T")


class Client:
    """A client to interact with Soroban smart contracts.

    :param contract_id: The ID of the Soroban contract.
    :param rpc_url: The URL of the RPC server.
    :param network_passphrase: The network passphrase.
    :param request_client: The request client used to send the request.
    """

    def __init__(
        self,
        contract_id: str,
        rpc_url: str,
        network_passphrase: str,
        request_client: BaseSyncClient = None,
    ):
        self.contract_id = contract_id
        self.rpc_url = rpc_url
        self.network_passphrase = network_passphrase
        self.server = SorobanServer(rpc_url, request_client)

    def invoke(
        self,
        function_name: str,
        parameters: Sequence[stellar_xdr.SCVal],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Keypair = None,
        parse_result_xdr_fn: Optional[Callable[[stellar_xdr.SCVal], T]] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 120,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[T]:
        """Build an :py:class:`AssembledTransaction <stellar_sdk.contract.AssembledTransaction>` to invoke a contract function.

        :param function_name: The name of the function to invoke.
        :param parameters: The parameters to pass to the function.
        :param source: The source account for the transaction.
        :param signer: The signer for the transaction.
        :param parse_result_xdr_fn: The function to parse the result XDR returned by the contract function, keep the result as :py:class:`SCVal <stellar_sdk.xdr.SCVal>` if not provided.
        :param base_fee: The base fee for the transaction.
        :param transaction_timeout: The timeout for the transaction.
        :param submit_timeout: The timeout for submitting the transaction.
        :param simulate: Whether to simulate the transaction.
        :param restore: Whether to restore the transaction, only valid when simulate is True, and the signer is provided.
        :return:
        """
        builder = (
            TransactionBuilder(
                Account(source, 0), self.network_passphrase, base_fee=base_fee
            )
            .append_invoke_contract_function_op(
                self.contract_id, function_name, parameters
            )
            .set_timeout(transaction_timeout)
        )
        assembled = AssembledTransaction(
            builder, self.server, signer, parse_result_xdr_fn, submit_timeout
        )
        if simulate:
            assembled = assembled.simulate(restore)
        return assembled

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()
