import copy
import dataclasses
import time
from typing import Callable, Generic, TypeVar, cast

from .. import Address, AddressType, Keypair, SorobanDataBuilder, xdr
from ..auth import (
    AuthorizationSigner,
    _resolve_account_or_contract_address,
    authorize_entry,
)
from ..base_soroban_server import ResourceLeeway, _assemble_transaction
from ..operation import InvokeHostFunction
from ..soroban_rpc import (
    AuthMode,
    GetTransactionResponse,
    GetTransactionStatus,
    RestorePreamble,
    SendTransactionResponse,
    SendTransactionStatus,
    SimulateHostFunctionResult,
    SimulateTransactionResponse,
)
from ..soroban_server import SorobanServer
from ..transaction_builder import TransactionBuilder
from ..transaction_envelope import TransactionEnvelope
from ..xdr import TransactionMeta
from .exceptions import *

T = TypeVar("T")

__all__ = ["AssembledTransaction"]


class AssembledTransaction(Generic[T]):
    """A class representing an assembled Soroban transaction that can be simulated and sent.

    The lifecycle of a transaction typically follows these steps:
        1. Construct the transaction (usually via a Client)
        2. Simulate the transaction
        3. Sign the transaction
        4. Submit the transaction

    :param transaction_builder: The transaction builder including the operation to invoke
    :param server: The Soroban server instance to use
    :param transaction_signer: Optional keypair for signing transactions, if you don't need to submit the transaction, you can set this to `None`.
    :param parse_result_xdr_fn: Optional function to parse XDR results, keep `None` for raw XDR
    :param submit_timeout: Timeout in seconds for transaction submission (default: 180s)
    :param addl_resources: Additional resource leeway forwarded to every internal
        simulation call (initial simulate, prepare, and the post-restore
        re-simulation). Not applied to the inner ``RestoreFootprint`` transaction
        created by automatic state restoration.
    :param auth_mode: Authorization mode forwarded to every internal simulation
        call. Use :class:`AuthMode.RECORD_ALL_NOROOT <stellar_sdk.soroban_rpc.AuthMode>`
        to opt into non-root authorization in recording mode.
    """

    def __init__(
        self,
        transaction_builder: TransactionBuilder,
        server: SorobanServer,
        transaction_signer: Keypair | None = None,
        parse_result_xdr_fn: Callable[[xdr.SCVal], T] | None = None,
        submit_timeout: int = 180,
        addl_resources: ResourceLeeway | None = None,
        auth_mode: AuthMode | None = None,
    ):
        self.server = server
        self.submit_timeout = submit_timeout

        self.transaction_signer = transaction_signer
        self.parse_result_xdr_fn = parse_result_xdr_fn

        self.transaction_builder: TransactionBuilder = transaction_builder
        self.built_transaction: TransactionEnvelope | None = None

        self.addl_resources = addl_resources
        self.auth_mode = auth_mode

        self.simulation: SimulateTransactionResponse | None = None
        self._simulation_result: SimulateHostFunctionResult | None = None
        self._simulation_transaction_data: xdr.SorobanTransactionData | None = None
        self._needs_preparation: bool = False
        self._preparation_reason: str | None = None

        self.send_transaction_response: SendTransactionResponse | None = None
        self.get_transaction_response: GetTransactionResponse | None = None

    def simulate(self, restore: bool = True) -> "AssembledTransaction":
        """Simulates the transaction on the network.

        Must be called before signing or submitting the transaction.
        Will automatically restore required contract state if restore to True.

        :param restore: Whether to automatically restore contract state if needed, defaults to True
        :return: Self for chaining
        :raises: :exc:`SimulationFailedError <stellar_sdk.contract.exceptions.SimulationFailedError>`: If the simulation fails
        :raises: :exc:`ExpiredStateError <stellar_sdk.contract.exceptions.ExpiredStateError>`: If state restoration failed
        """
        self._simulation_result = None
        self._simulation_transaction_data = None

        source = self.server.load_account(
            self.transaction_builder.source_account.account.account_id
        )
        self.transaction_builder.source_account.sequence = source.sequence

        built_tx = self.transaction_builder.build()
        self.simulation = self.server.simulate_transaction(
            built_tx,
            addl_resources=self.addl_resources,
            auth_mode=self.auth_mode,
        )

        if (
            restore
            and self.simulation.restore_preamble
            and not self._is_current_simulation_read_call()
        ):
            try:
                self.restore_footprint(self.simulation.restore_preamble)
            except (
                SimulationFailedError,
                TransactionStillPendingError,
                SendTransactionFailedError,
                TransactionFailedError,
            ) as e:
                raise RestorationFailureError(
                    "Failed to restore contract data.", self
                ) from e
            return self.simulate()

        if self.simulation.error is not None:
            raise SimulationFailedError(
                f"Transaction simulation failed: {self.simulation.error}", self
            )
        self.built_transaction = _assemble_transaction(built_tx, self.simulation)
        self._needs_preparation = False
        self._preparation_reason = None
        return self

    def prepare(self, restore: bool = True) -> "AssembledTransaction":
        """Prepare the current built transaction for signing and submission.

        Unlike :meth:`simulate`, this method simulates ``built_transaction`` as it
        currently exists, including any authorization entries that were signed
        after the initial simulation.

        :param restore: Whether to automatically restore contract state if needed, defaults to True
        :return: Self for chaining
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        :raises: :exc:`NeedsMoreSignaturesError <stellar_sdk.contract.exceptions.NeedsMoreSignaturesError>`: If authorization entries still require signatures
        :raises: :exc:`SimulationFailedError <stellar_sdk.contract.exceptions.SimulationFailedError>`: If the simulation fails
        """
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        if self.built_transaction.signatures:
            raise ValueError("Prepare must happen before transaction signing.")

        sigs_needed = list(self.needs_non_invoker_signing_by())
        if sigs_needed:
            raise NeedsMoreSignaturesError(
                f"`Transaction requires signatures from {sigs_needed}`. See `needs_non_invoker_signing_by` for details.",
                self,
            )

        simulation_tx = self._transaction_for_simulation()
        self.simulation = self.server.simulate_transaction(
            simulation_tx,
            addl_resources=self.addl_resources,
            auth_mode=self.auth_mode,
        )
        self._simulation_result = None
        self._simulation_transaction_data = None

        if (
            restore
            and self.simulation.restore_preamble
            and not self._is_current_simulation_read_call()
        ):
            try:
                self.restore_footprint(self.simulation.restore_preamble)
            except (
                SimulationFailedError,
                TransactionStillPendingError,
                SendTransactionFailedError,
                TransactionFailedError,
            ) as e:
                raise RestorationFailureError(
                    "Failed to restore contract data.", self
                ) from e
            return self.prepare(restore)

        if self.simulation.error is not None:
            raise SimulationFailedError(
                f"Transaction simulation failed: {self.simulation.error}", self
            )

        self.built_transaction = _assemble_transaction(simulation_tx, self.simulation)
        self._needs_preparation = False
        self._preparation_reason = None
        return self

    def sign_and_submit(
        self, transaction_signer: Keypair | None = None, force: bool = False
    ) -> T | xdr.SCVal:
        """Signs and submits the transaction in one step.

        A convenience method combining sign() and submit().

        :param transaction_signer: Optional keypair to sign with (overrides instance signer)
        :param force: Whether to sign and submit even if the transaction is a read call
        :return: The value returned by the invoked function, parsed if parse_result_xdr_fn was set, otherwise raw XDR
        """
        if self._needs_preparation:
            self.prepare()
        self.sign(force=force, transaction_signer=transaction_signer)
        return self.submit()

    def sign(
        self, transaction_signer: Keypair | None = None, force: bool = False
    ) -> "AssembledTransaction":
        """Signs the transaction.

        :param transaction_signer: Optional keypair to sign with (overrides instance signer)
        :param force: Whether to sign even if the transaction is a read call
        :return: Self for chaining
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        :raises: :exc:`NoSignatureNeededError <stellar_sdk.contract.exceptions.NoSignatureNeededError>`: If the transaction is a read call
        :raises: :exc:`NeedsMoreSignaturesError <stellar_sdk.contract.exceptions.NeedsMoreSignaturesError>`: If the transaction requires more signatures for authorization entries.
        """
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        if self._needs_preparation:
            raise NeedsPreparationError(
                self._preparation_reason
                or "Transaction must be prepared before signing.",
                self,
            )

        if not force and self.is_read_call():
            raise NoSignatureNeededError(
                "This is a read call. It requires no signature or submitting. Set force=True to sign and submit anyway.",
                self,
            )

        if self.simulation and self.simulation.restore_preamble:
            raise ExpiredStateError(
                "You need to restore some contract state before you can invoke this method. "
                + "You can set `restore` to true in order to "
                + "automatically restore the contract state when needed.",
                self,
            )

        transaction_signer = transaction_signer or self.transaction_signer
        if not transaction_signer:
            raise ValueError(
                "You must provide a transaction_signer to sign the transaction, either here or in the constructor."
            )

        sigs_needed = list(self.needs_non_invoker_signing_by())
        if sigs_needed:
            raise NeedsMoreSignaturesError(
                f"`Transaction requires signatures from {sigs_needed}`. See `needs_non_invoker_signing_by` for details.",
                self,
            )

        self.built_transaction.sign(transaction_signer)
        return self

    def authorize(
        self,
        address: Address | str | Keypair | AuthorizationSigner | None = None,
        signer: Keypair | AuthorizationSigner | None = None,
        valid_until_ledger_sequence: int | None = None,
        *,
        valid_for_ledger_count: int | None = None,
    ) -> "AssembledTransaction":
        """Authorize matching Soroban authorization entries.

        :param address: Classic account (``G...``) or contract (``C...``) address whose authorization entries should be signed. Required when ``signer`` is not a :class:`Keypair`; otherwise inferred from the keypair's public key. For convenience, a :class:`Keypair` or custom signer may be passed as the first positional argument when the address can be inferred.
        :param signer: A :class:`Keypair`, or any custom :data:`AuthorizationSigner <stellar_sdk.auth.AuthorizationSigner>` for non-default account contracts (BLS, WebAuthn, ...).
        :param valid_until_ledger_sequence: Optional ledger sequence until which the authorization is valid.
        :param valid_for_ledger_count: Optional number of ledgers from the latest simulation ledger for which the authorization remains valid. Defaults to 100 when ``valid_until_ledger_sequence`` is not provided.
        :return: Self for chaining
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        """
        address, signer = self._normalize_authorize_args(address, signer)
        valid_until_ledger_sequence = self._resolve_valid_until_ledger_sequence(
            valid_until_ledger_sequence, valid_for_ledger_count
        )
        self._authorize_entries(signer, address, valid_until_ledger_sequence)
        return self

    def sign_auth_entries(
        self,
        auth_entries_signer: Keypair | AuthorizationSigner,
        address: Address | str | None = None,
        valid_until_ledger_sequence: int | None = None,
        *,
        valid_for_ledger_count: int | None = None,
    ) -> "AssembledTransaction":
        """Signs the transaction's authorization entries.

        This method is kept for backwards compatibility. New code can use
        :meth:`authorize`, which also supports relative expiration via
        ``valid_for_ledger_count``.

        :param auth_entries_signer: A :class:`Keypair`, or any custom :data:`AuthorizationSigner <stellar_sdk.auth.AuthorizationSigner>` for non-default account contracts (BLS, WebAuthn, ...).
        :param address: Classic account (``G...``) or contract (``C...``) address whose authorization entries should be signed. Required when ``auth_entries_signer`` is not a :class:`Keypair`; otherwise inferred from the keypair's public key.
        :param valid_until_ledger_sequence: Optional ledger sequence until which the authorization is valid, if not set, defaults to 100 ledgers from the current ledger.
        :param valid_for_ledger_count: Optional number of ledgers from the latest simulation ledger for which the authorization remains valid.
        :return: Self for chaining
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        """
        if valid_until_ledger_sequence is None and valid_for_ledger_count is None:
            # Preserve the legacy default for sign_auth_entries(); authorize()
            # defaults relative expiration to the latest simulation ledger.
            valid_until_ledger_sequence = self.server.get_latest_ledger().sequence + 100

        return self.authorize(
            address=address,
            signer=auth_entries_signer,
            valid_until_ledger_sequence=valid_until_ledger_sequence,
            valid_for_ledger_count=valid_for_ledger_count,
        )

    def _normalize_authorize_args(
        self,
        address: Address | str | Keypair | AuthorizationSigner | None,
        signer: Keypair | AuthorizationSigner | None,
    ) -> tuple[Address | str | None, Keypair | AuthorizationSigner]:
        if signer is None and address is not None:
            if isinstance(address, Keypair) or callable(address):
                signer = cast(Keypair | AuthorizationSigner, address)
                address = None

        if signer is None:
            raise ValueError("`signer` is required.")
        return cast(Address | str | None, address), signer

    def _resolve_valid_until_ledger_sequence(
        self,
        valid_until_ledger_sequence: int | None,
        valid_for_ledger_count: int | None,
    ) -> int:
        if (
            valid_until_ledger_sequence is not None
            and valid_for_ledger_count is not None
        ):
            raise ValueError(
                "`valid_until_ledger_sequence` and `valid_for_ledger_count` are mutually exclusive."
            )
        if valid_until_ledger_sequence is not None:
            return valid_until_ledger_sequence

        valid_for_ledger_count = (
            100 if valid_for_ledger_count is None else valid_for_ledger_count
        )
        if self.simulation is not None:
            latest_ledger = self.simulation.latest_ledger
        else:
            latest_ledger = self.server.get_latest_ledger().sequence
        return latest_ledger + valid_for_ledger_count

    def _authorize_entries(
        self,
        signer: Keypair | AuthorizationSigner,
        address: Address | str | None,
        valid_until_ledger_sequence: int,
    ) -> None:
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        if address is None:
            if isinstance(signer, Keypair):
                address = signer.public_key
            else:
                raise ValueError(
                    "`address` is required when `signer` is not a Keypair."
                )

        target_address = _resolve_account_or_contract_address(address)

        if self.built_transaction.signatures:
            raise ValueError(
                "Authorization entries must be signed before transaction signing."
            )

        op = self.built_transaction.transaction.operations[0]
        assert isinstance(op, InvokeHostFunction)

        signed_any = False
        for i, e in enumerate(op.auth):
            if (
                e.credentials.type
                == xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
            ):
                continue
            assert e.credentials.address is not None
            entry_address = Address.from_xdr_sc_address(
                e.credentials.address.address
            ).address
            if entry_address != target_address.address:
                continue
            op.auth[i] = authorize_entry(
                e,
                signer,
                valid_until_ledger_sequence,
                self.built_transaction.network_passphrase,
            )
            signed_any = True

        if signed_any and self._authorization_requires_preparation(target_address):
            self._mark_needs_preparation(
                "Authorization entries changed in a way that may affect Soroban "
                "resources; call prepare() before signing or exporting XDR."
            )

    def _authorization_requires_preparation(self, address: Address) -> bool:
        return address.type == AddressType.CONTRACT

    def _mark_needs_preparation(self, reason: str) -> None:
        self._needs_preparation = True
        self._preparation_reason = reason

    def _transaction_for_simulation(self) -> TransactionEnvelope:
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        transaction = copy.deepcopy(self.built_transaction)
        transaction.signatures = []
        if transaction.transaction.soroban_data:
            transaction.transaction.fee -= (
                transaction.transaction.soroban_data.resource_fee.int64
            )
            transaction.transaction.soroban_data = None
        return transaction

    def submit(self) -> T | xdr.SCVal:
        """Submits the transaction to the network.

        It will send the transaction to the network and wait for the result.

        :return: The value returned by the invoked function, parsed if parse_result_xdr_fn was set, otherwise raw XDR
        :raises: :exc:`SendTransactionFailedError <stellar_sdk.contract.exceptions.SendTransactionFailedError>`: If sending the transaction fails
        :raises: :exc:`TransactionStillPendingError <stellar_sdk.contract.exceptions.TransactionStillPendingError>`: If the transaction is still pending after the timeout, you can re-call this method to wait longer
        :raises: :exc:`TransactionFailedError <stellar_sdk.contract.exceptions.TransactionFailedError>`: If the transaction fails
        """
        response = self._submit()
        assert response.result_meta_xdr is not None
        transaction_meta = TransactionMeta.from_xdr(response.result_meta_xdr)
        transaction_meta_body = (
            transaction_meta.v4 or transaction_meta.v3
        )  # v4 introduced in protocol 23
        assert transaction_meta_body is not None
        assert transaction_meta_body.soroban_meta is not None
        result_val = transaction_meta_body.soroban_meta.return_value
        assert (
            result_val is not None
        )  # In SorobanTransactionMetaV2, it is defined as possibly null.
        return (
            self.parse_result_xdr_fn(result_val)
            if self.parse_result_xdr_fn
            else result_val
        )

    def _submit(self) -> GetTransactionResponse:
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        if not self.send_transaction_response:
            self.send_transaction_response = self.server.send_transaction(
                self.built_transaction
            )
            if self.send_transaction_response.status != SendTransactionStatus.PENDING:
                raise SendTransactionFailedError(
                    f"Sending the transaction to the network failed!\n{self.send_transaction_response.model_dump_json()}",
                    self,
                )

        tx_hash = self.send_transaction_response.hash
        self.get_transaction_response = _with_exponential_backoff(
            lambda: self.server.get_transaction(tx_hash),
            lambda resp: resp.status == GetTransactionStatus.NOT_FOUND,
            self.submit_timeout,
        )[-1]

        assert self.get_transaction_response is not None
        if self.get_transaction_response.status == GetTransactionStatus.SUCCESS:
            return self.get_transaction_response
        if self.get_transaction_response.status == GetTransactionStatus.NOT_FOUND:
            raise TransactionStillPendingError(
                f"Waited {self.submit_timeout} seconds for transaction to complete, but it did not. "
                f"Returning anyway. You can call result() to await the result later "
                f"or check the status of the transaction manually.",
                self,
            )
        elif self.get_transaction_response.status == GetTransactionStatus.FAILED:
            raise TransactionFailedError(f"Transaction failed.", self)
        else:
            raise ValueError("Unexpected transaction status.")

    def needs_non_invoker_signing_by(
        self, include_already_signed: bool = False
    ) -> set[str]:
        """Get the addresses that need to sign the authorization entries.

        :param include_already_signed: Whether to include addresses that have already signed the authorization entries.
        :return: The addresses that need to sign the authorization entries.
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        """
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        invoke_host_function_op = self.built_transaction.transaction.operations[0]
        if not isinstance(invoke_host_function_op, InvokeHostFunction):
            return set()

        result = set()
        for entry in invoke_host_function_op.auth or []:
            if (
                entry.credentials.type
                == xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
            ):
                assert entry.credentials.address is not None

                if (
                    include_already_signed
                    or entry.credentials.address.signature.type
                    == xdr.SCValType.SCV_VOID
                ):
                    address = Address.from_xdr_sc_address(
                        entry.credentials.address.address
                    ).address
                    result.add(address)
        return result

    def result(self) -> T | xdr.SCVal:
        """Get the result of the function invocation from the simulation.

        :return: The value returned by the invoked function, parsed if parse_result_xdr_fn was set, otherwise raw XDR
        """
        if self._needs_preparation:
            raise NeedsPreparationError(
                self._preparation_reason
                or "Transaction must be prepared before reading the result.",
                self,
            )

        raw_result = xdr.SCVal.from_xdr(self._simulation_data().result.xdr)
        if self.parse_result_xdr_fn:
            return self.parse_result_xdr_fn(raw_result)
        return raw_result

    def is_read_call(self) -> bool:
        """Check if the transaction is a read call.

        :return: True if the transaction is a read call, False otherwise
        :raises: :exc:`NotYetSimulatedError <stellar_sdk.contract.exceptions.NotYetSimulatedError>`: If the transaction has not been simulated
        """
        if self._needs_preparation:
            raise NeedsPreparationError(
                self._preparation_reason
                or "Transaction must be prepared before checking read-call status.",
                self,
            )

        return self._is_current_simulation_read_call()

    def to_xdr(self):
        """Get the XDR representation of the transaction envelope.

        :return: The XDR representation of the transaction envelope
        """
        if not self.built_transaction:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        if self._needs_preparation:
            raise NeedsPreparationError(
                self._preparation_reason
                or "Transaction must be prepared before exporting XDR.",
                self,
            )

        return self.built_transaction.to_xdr()

    def restore_footprint(self, restore_preamble: RestorePreamble) -> None:
        if not self.transaction_signer:
            raise ValueError(
                "For automatic restore to work you must provide a transaction_signer when initializing AssembledTransaction."
            )
        restore_tx = (
            TransactionBuilder(
                self.transaction_builder.source_account,
                self.transaction_builder.network_passphrase,
                self.transaction_builder.base_fee,
            )
            .append_restore_footprint_op()
            .set_soroban_data(
                SorobanDataBuilder.from_xdr(restore_preamble.transaction_data).build()
            )
            .add_time_bounds(0, 0)
        )
        restore_assembled: AssembledTransaction = AssembledTransaction(
            restore_tx,
            self.server,
            self.transaction_signer,
            None,
            submit_timeout=self.submit_timeout,
        )
        restore_assembled.simulate(restore=False).sign(force=True)._submit()

    def _simulation_data(
        self,
    ) -> "SimulationData":
        if self._simulation_result and self._simulation_transaction_data:
            return SimulationData(
                self._simulation_result, self._simulation_transaction_data
            )

        if not self.simulation:
            raise NotYetSimulatedError("Transaction has not yet been simulated.", self)

        # SimulateHostFunctionResult(auth=[], xdr='AAAAAQ==') for no return function (void)
        assert self.simulation.results is not None
        assert self.simulation.transaction_data is not None
        self._simulation_result = self.simulation.results[0]
        self._simulation_transaction_data = xdr.SorobanTransactionData.from_xdr(
            self.simulation.transaction_data
        )
        return SimulationData(
            self._simulation_result, self._simulation_transaction_data
        )

    def _is_current_simulation_read_call(self) -> bool:
        simulation_data = self._simulation_data()
        auths = simulation_data.result.auth
        writes = simulation_data.transaction_data.resources.footprint.read_write
        return not auths and not writes


@dataclasses.dataclass
class SimulationData:
    result: SimulateHostFunctionResult
    transaction_data: xdr.SorobanTransactionData


def _with_exponential_backoff(
    fn,
    keep_waiting_if,
    timeout: float,
    exponential_factor: float = 1.5,
    verbose: bool = False,
):
    """Keep calling a function for timeout seconds if keep_waiting_if is true.
    Returns an array of all attempts to call the function.

    :param fn: Function to call repeatedly
    :param keep_waiting_if: Condition to check when deciding whether to call fn again
    :param timeout: How long to wait between first and second call
    :param exponential_factor: What to multiply timeout by each subsequent attempt
    :param verbose: Whether to log extra info, for debug only
    """
    attempts = []

    count = 0
    attempts.append(fn())
    if not keep_waiting_if(attempts[-1]):
        return attempts

    wait_until = time.time() + timeout
    wait_time = 1.0  # seconds
    total_wait_time = wait_time

    while time.time() < wait_until and keep_waiting_if(attempts[-1]):
        count += 1

        # Log waiting time if verbose
        if verbose:
            print(
                f"Waiting {wait_time * 1000} ms before trying again "
                f"(bringing the total wait time to {total_wait_time * 1000} ms "
                f"so far, of total {timeout * 1000} ms)"
            )

        time.sleep(wait_time)

        wait_time *= exponential_factor
        if wait_time >= 6:
            wait_time = 6

        if time.time() + wait_time > wait_until:
            wait_time = wait_until - time.time()
            if verbose:
                print(f"was gonna wait too long; new waitTime: {wait_time * 1000} ms")

        total_wait_time += wait_time
        attempts.append(fn())

        if verbose and keep_waiting_if(attempts[-1]):
            print(
                f"{count}. Called fn; "
                f"{len(attempts)} prev attempts. "
                f"Most recent: {attempts[-1].model_dump_json()}"
            )

    return attempts
