from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class PaymentsCallBuilder(BaseCallBuilder):
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

    def for_account(self, account_id: str) -> "PaymentsCallBuilder":
        """This endpoint responds with a collection of Payment operations where the given account
        was either the sender or receiver.

        See `Payments for Account <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-account.html>`_

        :param account_id: Account ID
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/payments"
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "PaymentsCallBuilder":
        """This endpoint represents all payment operations that are part of a valid transactions in a given ledger.

        See `Payments for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-ledger.html>`_

        :param sequence: Ledger sequence
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint: str = f"ledgers/{sequence}/payments"
        return self

    def for_transaction(self, transaction_hash: str) -> "PaymentsCallBuilder":
        """This endpoint represents all payment operations that are part of a given transaction.

        See `Payments for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-transaction.html>`_

        :param transaction_hash: Transaction hash
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint: str = f"transactions/{transaction_hash}/payments"
        return self

    def include_failed(self, include_failed: bool) -> "PaymentsCallBuilder":
        """Adds a parameter defining whether to include failed transactions. By default only
        payments of successful transactions are returned.

        :param include_failed: Set to ``True`` to include payments of failed transactions.
        :return: current PaymentsCallBuilder instance
        """
        self._add_query_param("include_failed", include_failed)
        return self

    def join(self, join: str) -> "PaymentsCallBuilder":
        """join represents `join` param in queries, currently only supports `transactions`

        :param join: join represents `join` param in queries, currently only supports `transactions`
        :return: current OperationsCallBuilder instance
        """
        self._add_query_param("join", join)
        return self
