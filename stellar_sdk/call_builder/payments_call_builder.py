from typing import Union, TypeVar, List, AsyncGenerator, Generator

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..response.operation_response import (
    OPERATION_TYPE_I_RESPONSE,
    PAYMENT_RESPONSE_TYPE_UNION,
    OPERATION_TYPE_I_RESPONSE_TYPE,
)
from ..response.wrapped_response import WrappedResponse

T = TypeVar("T")


class PaymentsCallBuilder(BaseCallBuilder[T]):
    """ Creates a new :class:`PaymentsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.payments`.

    See `All Payments <https://www.stellar.org/developers/horizon/reference/endpoints/payments-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "payments"

    def for_account(self, account_id: str) -> "PaymentsCallBuilder[T]":
        """This endpoint responds with a collection of Payment operations where the given account
        was either the sender or receiver.

        See `Payments for Account <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-account.html>`_

        :param account_id: Account ID
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint = "accounts/{account_id}/payments".format(account_id=account_id)
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "PaymentsCallBuilder[T]":
        """This endpoint represents all payment operations that are part of a valid transactions in a given ledger.

        See `Payments for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-ledger.html>`_

        :param sequence: Ledger sequence
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint: str = "ledgers/{sequence}/payments".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "PaymentsCallBuilder[T]":
        """This endpoint represents all payment operations that are part of a given transaction.

        See `Payments for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-transaction.html>`_

        :param transaction_hash: Transaction hash
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint: str = "transactions/{transaction_hash}/payments".format(
            transaction_hash=transaction_hash
        )
        return self

    def include_failed(self, include_failed: bool) -> "PaymentsCallBuilder[T]":
        """Adds a parameter defining whether to include failed transactions. By default only
        payments of successful transactions are returned.

        :param include_failed: Set to ``True`` to include payments of failed transactions.
        :return: current PaymentsCallBuilder instance
        """
        self._add_query_param("include_failed", include_failed)
        return self

    def _get_corresponding_response_type(
        self, operation_json
    ) -> OPERATION_TYPE_I_RESPONSE_TYPE:
        operation_type = operation_json["type_i"]
        if operation_type not in OPERATION_TYPE_I_RESPONSE:
            raise NotImplementedError(
                "The type of operation is %d, which is not currently supported in the version. "
                "Please try to upgrade the SDK or raise an issue." % operation_type
            )
        return OPERATION_TYPE_I_RESPONSE[operation_type]

    def _parse_response(
        self, raw_data: dict
    ) -> Union[List[PAYMENT_RESPONSE_TYPE_UNION], PAYMENT_RESPONSE_TYPE_UNION]:
        return self._base_parse_response(
            raw_data, model_selector=self._get_corresponding_response_type
        )

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[WrappedResponse[PAYMENT_RESPONSE_TYPE_UNION], None],
        Generator[WrappedResponse[PAYMENT_RESPONSE_TYPE_UNION], None, None],
    ]:
        return self._stream()
