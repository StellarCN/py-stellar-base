from typing_extensions import Generic

from .exceptions import *
from ..soroban_rpc import SendTransactionResponse, GetTransactionResponse, GetTransactionStatus, SendTransactionStatus
from ..soroban_server import SorobanServer
from ..transaction_envelope import TransactionEnvelope
from .. import xdr
import time
from typing import List, Callable, Optional, TypeVar, Union

__all__ = ["SentTransaction"]

T = TypeVar("T")


class SentTransaction(Generic[T]):
    """A transaction that has been sent to the Soroban network. This happens in two steps:

        1. send(): send the transaction to the network, and wait for it to be finalized.
        2. result(): get the result of the transaction.

    :param server: The Soroban RPC server instance
    :param transaction_envelope: The envelope containing the transaction
    :param parse_result_xdr: Function to parse XDR result, keep `None` for raw XDR
    :param timeout: Max seconds to wait for transaction completion
    """

    def __init__(
            self,
            server: SorobanServer,
            transaction_envelope: TransactionEnvelope,
            parse_result_xdr: Optional[Callable[[xdr.SCVal], T]],
            timeout: int = 300,
    ):
        self.server = server
        self.transaction_envelope = transaction_envelope
        self.send_transaction_response: Optional[SendTransactionResponse] = None
        self.get_transaction_response: Optional[GetTransactionResponse] = None
        self.parse_result_xdr = parse_result_xdr
        self.timeout = timeout
        self._get_transaction_response_all: List[GetTransactionResponse] = []

    def send(self):
        """Send transaction to network and wait for completion.

        This method only ensures that the transaction is sent to the network. It does not guarantee the final success or failure of the transaction execution.
        To get the final result of the transaction, you need to call the result() method.

        :raises: :exc:`SendTransactionFailedError <stellar_sdk.contract.exceptions.SendTransactionFailedError>`: If sending fails
        :raises: :exc:`TransactionStillPendingError <stellar_sdk.contract.exceptions.TransactionStillPendingError>`: If transaction doesn't complete within timeout
        """
        if not self.send_transaction_response:
            self.send_transaction_response = self.server.send_transaction(
                self.transaction_envelope
            )
            if self.send_transaction_response.status != SendTransactionStatus.PENDING:
                raise SendTransactionFailedError(
                    f"Sending the transaction to the network failed!\n{self.send_transaction_response.model_dump_json()}"
                )

        tx_hash = self.send_transaction_response.hash
        self._get_transaction_response_all.extend(
            with_exponential_backoff(
                lambda: self.server.get_transaction(tx_hash),
                lambda resp: resp.status == GetTransactionStatus.NOT_FOUND,
                self.timeout,
            )
        )

        self.get_transaction_response = self._get_transaction_response_all[-1]
        if self.get_transaction_response.status == GetTransactionStatus.NOT_FOUND:
            raise TransactionStillPendingError(
                f"Waited {self.timeout} seconds for transaction to complete, but it did not. "
                f"Returning anyway. You can call result() to await the result later "
                f"or check the status of the transaction manually."
            )

    def result(self) -> Union[T, xdr.SCVal]:
        """Get the result of the transaction.

        :return: Parsed transaction result if parser provided, raw XDR otherwise
        :raises: :exc:`SendTransactionFailedError <stellar_sdk.contract.exceptions.SendTransactionFailedError>`: If transaction failed during send or execution
        :raises: :exc:`TransactionStillPendingError <stellar_sdk.contract.exceptions.TransactionStillPendingError>`: If transaction was sent but not yet complete
        :raises: :exc:`TransactionNotSentError <stellar_sdk.contract.exceptions.TransactionNotSentError>`: If transaction was not sent
        """
        if self.get_transaction_response:
            if self.get_transaction_response.status == GetTransactionStatus.SUCCESS:
                transaction_meta = xdr.TransactionMeta.from_xdr(
                    self.get_transaction_response.result_meta_xdr
                )
                result_val = transaction_meta.v3.soroban_meta.return_value
                return (
                    self.parse_result_xdr(result_val)
                    if self.parse_result_xdr
                    else result_val
                )

            if self.get_transaction_response.status == GetTransactionStatus.FAILED:
                raise SendTransactionFailedError(
                    f"Send transaction failed, get_transaction_response: {self.get_transaction_response.model_dump_json()}"
                )

        if self.send_transaction_response:
            if self.send_transaction_response.error_result_xdr:
                raise SendTransactionFailedError(
                    f"Send transaction failed, get_transaction_response: {self.get_transaction_response.model_dump_json()}"
                )
            else:
                raise TransactionStillPendingError(
                    f"Transaction was sent to the network, but not yet awaited. No result to show. "
                    f"You can call send() again to await the result."
                )
        raise TransactionNotSentError(f"Transaction was not sent to the network. Call send() first.")


def with_exponential_backoff(
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
