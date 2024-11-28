from typing import Callable, Optional, Sequence, TypeVar, Union

from .. import Account, Asset, Keypair, MuxedAccount, SorobanServerAsync, scval
from .. import xdr as stellar_xdr
from ..client.base_async_client import BaseAsyncClient
from ..transaction_builder import TransactionBuilder
from .assembled_transaction_async import AssembledTransactionAsync

NULL_ACCOUNT = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"

__all__ = ["ContractClientAsync"]

T = TypeVar("T")


class ContractClientAsync:
    """A client to interact with Soroban smart contracts.

    This client is a wrapper for :py:class:`TransactionBuilder <stellar_sdk.TransactionBuilder>` and :py:class:`SorobanServerAsync <stellar_sdk.SorobanServerAsync>`.
    If you need more fine-grained control, please consider using them directly.

    I strongly recommend that you do not use this client directly, but instead use `stellar-contract-bindings <https://github.com/lightsail-network/stellar-contract-bindings>`_ to
    generate contract binding code, which will make calling the contract much simpler.

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
        request_client: Optional[BaseAsyncClient] = None,
    ):
        self.contract_id = contract_id
        self.rpc_url = rpc_url
        self.network_passphrase = network_passphrase
        self.server = SorobanServerAsync(rpc_url, request_client)

    async def invoke(
        self,
        function_name: str,
        parameters: Optional[Sequence[stellar_xdr.SCVal]] = None,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        parse_result_xdr_fn: Optional[Callable[[stellar_xdr.SCVal], T]] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[T]:
        """Build an :py:class:`AssembledTransactionAsync <stellar_sdk.contract.AssembledTransactionAsync>` to invoke a contract function.

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
        assembled = AssembledTransactionAsync(
            builder, self.server, signer, parse_result_xdr_fn, submit_timeout
        )
        if simulate:
            assembled = await assembled.simulate(restore)
        return assembled

    @staticmethod
    async def upload_contract_wasm(
        contract: Union[bytes, str],
        source: Union[str, MuxedAccount],
        signer: Keypair,
        soroban_server: SorobanServerAsync,
        network_passphrase: Optional[str] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 120,
    ) -> bytes:
        """Upload a contract wasm.

        :param contract: The contract wasm.
        :param source: The source account for the transaction.
        :param signer: The signer for the transaction.
        :param soroban_server: The Soroban server.
        :param network_passphrase: The network passphrase, default to the network of the Soroban server.
        :param base_fee: The base fee for the transaction.
        :param transaction_timeout: The timeout for the transaction.
        :param submit_timeout: The timeout for submitting the transaction.
        :return: The wasm ID.
        """
        if network_passphrase is None:
            network_passphrase = (await soroban_server.get_network()).passphrase
        builder = (
            TransactionBuilder(
                Account(source, 0), network_passphrase, base_fee=base_fee
            )
            .append_upload_contract_wasm_op(contract)
            .set_timeout(transaction_timeout)
        )
        wasm_id = await (
            await AssembledTransactionAsync[bytes](
                builder,
                soroban_server,
                signer,
                lambda v: scval.from_bytes(v),
                submit_timeout,
            ).simulate()
        ).sign_and_submit(force=True)
        assert isinstance(wasm_id, bytes)
        return wasm_id

    @staticmethod
    async def create_contract(
        wasm_id: Union[bytes, str],
        source: Union[str, MuxedAccount],
        signer: Keypair,
        soroban_server: SorobanServerAsync,
        constructor_args: Optional[Sequence[stellar_xdr.SCVal]] = None,
        salt: Optional[bytes] = None,
        network_passphrase: Optional[str] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 120,
        restore: bool = True,
    ) -> str:
        """Create a contract.

        :param wasm_id: The wasm ID.
        :param source: The source account for the transaction.
        :param signer: The signer for the transaction.
        :param soroban_server: The Soroban server.
        :param constructor_args: The constructor arguments.
        :param salt: The salt.
        :param network_passphrase: The network passphrase, default to the network of the Soroban server.
        :param base_fee: The base fee for the transaction.
        :param transaction_timeout: The timeout for the transaction.
        :param submit_timeout: The timeout for submitting the transaction.
        :param restore: Whether to restore the transaction.
        :return: The contract ID.
        """
        if network_passphrase is None:
            network_passphrase = (await soroban_server.get_network()).passphrase
        address = source if isinstance(source, str) else source.account_id
        builder = (
            TransactionBuilder(
                Account(source, 0), network_passphrase, base_fee=base_fee
            )
            .append_create_contract_op(wasm_id, address, constructor_args, salt)
            .set_timeout(transaction_timeout)
        )
        contract_id = await (
            await AssembledTransactionAsync[str](
                builder,
                soroban_server,
                signer,
                lambda v: scval.from_address(v).address,
                submit_timeout,
            ).simulate(restore)
        ).sign_and_submit(force=True)
        assert isinstance(contract_id, str)
        return contract_id

    @staticmethod
    async def create_stellar_asset_contract_from_asset(
        asset: Asset,
        source: Union[str, MuxedAccount],
        signer: Keypair,
        soroban_server: SorobanServerAsync,
        network_passphrase: Optional[str] = None,
        base_fee: int = 100,
        submit_timeout: int = 120,
    ) -> str:
        """Create a Stellar asset contract from an asset.

        :param asset: The asset.
        :param source: The source account for the transaction.
        :param signer: The signer for the transaction.
        :param soroban_server: The Soroban server.
        :param network_passphrase: The network passphrase, default to the network of the Soroban server.
        :param base_fee: The base fee for the transaction.
        :param submit_timeout: The timeout for submitting the transaction.
        :return: The contract ID.
        """
        if network_passphrase is None:
            network_passphrase = (await soroban_server.get_network()).passphrase
        builder = (
            TransactionBuilder(
                Account(source, 0), network_passphrase, base_fee=base_fee
            )
            .append_create_stellar_asset_contract_from_asset_op(asset, source)
            .add_time_bounds(0, 0)
        )
        contract_id = await (
            await AssembledTransactionAsync[str](
                builder,
                soroban_server,
                signer,
                lambda v: scval.from_address(v).address,
                submit_timeout,
            ).simulate()
        ).sign_and_submit(force=True)
        assert isinstance(contract_id, str)
        return contract_id

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.server.close()
