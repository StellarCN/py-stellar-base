from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BasePaymentsCallBuilder"]


class BasePaymentsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`PaymentsCallBuilder` pointed to server defined by horizon_url.

    See `All Payments <https://www.stellar.org/developers/horizon/reference/endpoints/payments-all.html>`__

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "payments"

    def for_account(self, account_id: str):
        """This endpoint responds with a collection of Payment operations where the given account
        was either the sender or receiver.

        See `Payments for Account <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-account.html>`__

        :param account_id: Account ID
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/payments"
        return self

    def for_ledger(self, sequence: Union[int, str]):
        """This endpoint represents all payment operations that are part of a valid transactions in a given ledger.

        See `Payments for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-ledger.html>`__

        :param sequence: Ledger sequence
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}/payments"
        return self

    def for_transaction(self, transaction_hash: str):
        """This endpoint represents all payment operations that are part of a given transaction.

        See `Payments for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-transaction.html>`__

        :param transaction_hash: Transaction hash
        :return: current PaymentsCallBuilder instance
        """
        self.endpoint = f"transactions/{transaction_hash}/payments"
        return self

    def include_failed(self, include_failed: bool):
        """Adds a parameter defining whether to include failed transactions. By default only
        payments of successful transactions are returned.

        :param include_failed: Set to ``True`` to include payments of failed transactions.
        :return: current PaymentsCallBuilder instance
        """
        self._add_query_param("include_failed", include_failed)
        return self

    def join(self, join: str):
        """join represents `join` param in queries, currently only supports `transactions`

        :param join: join represents `join` param in queries, currently only supports `transactions`
        :return: current OperationsCallBuilder instance
        """
        self._add_query_param("join", join)
        return self
