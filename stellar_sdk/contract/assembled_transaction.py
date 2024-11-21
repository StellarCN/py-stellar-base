import dataclasses
from typing import Optional, TypeVar, Callable, Generic, Set

from .exceptions import *
from .sent_transaction import SentTransaction
from .. import xdr, Address, Account, SorobanDataBuilder, Keypair
from ..auth import authorize_entry
from ..base_soroban_server import _assemble_transaction
from ..operation import InvokeHostFunction
from ..soroban_rpc import (
    SimulateTransactionResponse,
    SimulateHostFunctionResult,
    RestorePreamble,
    GetTransactionStatus,
)
from ..soroban_server import SorobanServer
from ..transaction_builder import TransactionBuilder
from ..transaction_envelope import TransactionEnvelope

T = TypeVar("T")

__all__ = ["AssembledTransaction"]

class AssembledTransaction(Generic[T]):
    def __init__(
        self,
        raw_transaction: TransactionBuilder,
        server: SorobanServer,
        transaction_signer: Keypair = None,
        parse_result_xdr_fn: Optional[Callable[[xdr.SCVal], T]] = None,
        timeout: int = 300,
    ):
        self.server = server
        self.timeout = timeout

        self.transaction_signer = transaction_signer
        self.parse_result_xdr_fn = parse_result_xdr_fn

        self.raw_transaction: TransactionBuilder = raw_transaction
        self.built_transaction: Optional[TransactionEnvelope] = None

        self.simulation: Optional[SimulateTransactionResponse] = None
        self._simulation_result: Optional[SimulateHostFunctionResult] = None
        self._simulation_transaction_data: Optional[xdr.SorobanTransactionData] = None

    def is_read_call(self) -> bool:
        simulation_data = self.simulation_data
        auths = simulation_data.result.auth
        writes = simulation_data.transaction_data.resources.footprint.read_write
        return not auths and not writes

    def sign_auth_entries(
        self, signer: Keypair, valid_until_ledger_sequence: int = None
    ) -> "AssembledTransaction":
        if valid_until_ledger_sequence is None:
            valid_until_ledger_sequence = self.server.get_latest_ledger().sequence + 100

        if not self.built_transaction:
            raise ValueError("Transaction has not yet been simulated.")

        op = self.built_transaction.transaction.operations[0]
        assert isinstance(op, InvokeHostFunction)
        for i, e in enumerate(op.auth):
            if (
                e.credentials.type
                == xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
            ):
                continue
            if (
                Address.from_xdr_sc_address(e.credentials.address.address).address
                != signer.public_key
            ):
                continue
            op.auth[i] = authorize_entry(
                e,
                signer,
                valid_until_ledger_sequence,
                self.raw_transaction.network_passphrase,
            )
        return self

    def sign(
        self, force: bool = False, transaction_signer: Keypair = None
    ) -> "AssembledTransaction":
        if not self.built_transaction:
            raise ValueError("Transaction has not yet been simulated.")

        if not force and self.is_read_call():
            raise NoSignatureNeededError(
                "This is a read call. It requires no signature or sending. Set force=True to sign and send anyway."
            )

        transaction_signer = transaction_signer or self.transaction_signer
        if not transaction_signer:
            raise ValueError(
                "You must provide a sign_transaction_func to sign the transaction, either here or in the constructor."
            )

        sigs_needed = [
            s for s in self.needs_non_invoker_signing_by() if not s.startswith("C")
        ]
        if sigs_needed:
            raise NeedsMoreSignaturesError(
                f"`Transaction requires signatures from {sigs_needed}`. See `needs_non_invoker_signing_by` for details."
            )

        self.built_transaction.sign(transaction_signer)
        return self

    def send(self) -> SentTransaction:
        if not self.built_transaction or not self.built_transaction.signatures:
            raise ValueError(
                "Transaction has not yet been signed. Run `sign` first or use `sign_and_send` instead."
            )
        sent = SentTransaction(
            self.server, self.built_transaction, self.parse_result_xdr_fn
        )
        sent.send()
        return sent

    def sign_and_send(
        self, force: bool = False, transaction_signer: Keypair = None
    ) -> SentTransaction:
        self.sign(force=force, transaction_signer=transaction_signer)
        return self.send()

    def needs_non_invoker_signing_by(
        self, include_already_signed: bool = False
    ) -> Set[str]:
        if not self.built_transaction:
            raise ValueError("Transaction has not yet been simulated.")

        if not self.built_transaction.transaction.is_soroban_transaction():
            raise ValueError("This is not a Soroban transaction.")

        invoke_host_function_op = self.built_transaction.transaction.operations[0]
        if not isinstance(invoke_host_function_op, InvokeHostFunction):
            raise ValueError("Unexpected operation type.")

        result = set()
        for entry in invoke_host_function_op.auth or []:
            if (
                entry.credentials.type
                == xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
                and (
                    include_already_signed
                    or entry.credentials.address.signature.type
                    == xdr.SCValType.SCV_VOID
                )
            ):
                address = Address.from_xdr_sc_address(
                    entry.credentials.address.address
                ).address
                result.add(address)
        return result

    @property
    def simulation_data(
        self,
    ) -> "SimulationData":
        if self._simulation_result and self._simulation_transaction_data:
            return SimulationData(
                self._simulation_result, self._simulation_transaction_data
            )

        if not self.simulation:
            raise NotYetSimulatedError("Transaction has not yet been simulated.")

        if self.simulation.restore_preamble:
            raise ExpiredStateError(
                "You need to restore some contract state before you can invoke this method. "
                + "You can set `restore` to true in order to "
                + "automatically restore the contract state when needed."
            )

        # SimulateHostFunctionResult(auth=[], xdr='AAAAAQ==') for no return function (void)
        self._simulation_result = self.simulation.results[0]
        self._simulation_transaction_data = xdr.SorobanTransactionData.from_xdr(
            self.simulation.transaction_data
        )
        return SimulationData(
            self._simulation_result, self._simulation_transaction_data
        )

    def result(self):
        raw_result = xdr.SCVal.from_xdr(self.simulation_data.result.xdr)
        if self.parse_result_xdr_fn:
            return self.parse_result_xdr_fn(raw_result)
        return raw_result

    def simulate(self, restore: bool = True) -> "AssembledTransaction":
        self.built_transaction = self.raw_transaction.build()
        self._simulation_result = None
        self._simulation_transaction_data = None
        self.simulation = self.server.simulate_transaction(self.built_transaction)

        if restore and self.simulation.restore_preamble:
            source = self.raw_transaction.source_account
            self.restore_footprint(self.simulation.restore_preamble, source)
            source.increment_sequence_number()
            self.simulate()

        if self.simulation.error is not None:
            raise SimulationFailedError(
                f"Transaction simulation failed: {self.simulation.error}"
            )
        self.built_transaction = _assemble_transaction(
            self.built_transaction, self.simulation
        )
        return self

    def restore_footprint(
        self, restore_preamble: RestorePreamble, account: Account = None
    ) -> None:
        if not self.transaction_signer:
            raise ValueError(
                "For automatic restore to work you must provide a transaction_signer when initializing AssembledTransaction."
            )
        restore_tx = (
            (
                TransactionBuilder(
                    account,
                    self.raw_transaction.network_passphrase,
                    int(restore_preamble.min_resource_fee),
                )
                .append_restore_footprint_op()
                .set_soroban_data(
                    SorobanDataBuilder.from_xdr(restore_preamble.transaction_data)
                )
            )
            .set_timeout(self.timeout)
            .build()
        )
        restore_assembled = AssembledTransaction(
            restore_tx,
            self.server,
            self.transaction_signer,
            None,
            timeout=self.timeout,
        )
        restore_assembled.simulate(restore=False)
        sent_tx = restore_assembled.sign_and_send()

        if (
            not sent_tx.get_transaction_response
            or sent_tx.get_transaction_response.status != GetTransactionStatus.SUCCESS
        ):
            raise RestorationFailure("The attempt at automatic restore failed.")

    def to_xdr(self):
        if not self.built_transaction:
            raise ValueError("Transaction has not yet been simulated.")

        return self.built_transaction.to_xdr()


@dataclasses.dataclass
class SimulationData:
    result: SimulateHostFunctionResult
    transaction_data: xdr.SorobanTransactionData
