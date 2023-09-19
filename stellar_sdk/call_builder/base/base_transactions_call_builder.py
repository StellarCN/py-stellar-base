from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseTransactionsCallBuilder"]


class BaseTransactionsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`TransactionsCallBuilder` pointed to server defined by horizon_url.

    See `List All Transactions <https://developers.stellar.org/api/resources/transactions/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "transactions"

    def transaction(self, transaction_hash: str):
        """The transaction details endpoint provides information on a single transaction.
        The transaction hash provided in the hash argument specifies which transaction to load.

        See `Retrieve a Transaction <https://developers.stellar.org/api/resources/transactions/single/>`__ for more information.


        :param transaction_hash: transaction hash
        :return: current TransactionsCallBuilder instance
        """
        self.endpoint = f"transactions/{transaction_hash}"
        return self

    def for_account(self, account_id: str):
        """This endpoint represents all transactions that affected a given account.

        See `Retrieve an Account's Transactions <https://developers.stellar.org/api/resources/accounts/transactions/>`__ for more information.

        :param account_id: account id
        :return: current TransactionsCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/transactions"
        return self

    def for_ledger(self, sequence: Union[str, int]):
        """This endpoint represents all transactions in a given ledger.

        See `Retrieve a Ledger's Transactions <https://developers.stellar.org/api/resources/ledgers/transactions/>`__ for more information.

        :param sequence: ledger sequence
        :return: current TransactionsCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}/transactions"
        return self

    def for_claimable_balance(self, claimable_balance_id: str):
        """This endpoint represents all transactions referencing a given claimable balance and can be used in streaming mode.

        See `Claimable Balances - Retrieve related Transactions <https://developers.stellar.org/api/resources/claimablebalances/transactions/>`__

        :param claimable_balance_id: This claimable balance’s id encoded in a hex string representation.
        :return: current TransactionsCallBuilder instance
        """
        self.endpoint = f"claimable_balances/{claimable_balance_id}/transactions"
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """This endpoint represents all transactions referencing a given liquidity pool.

        See `Liquidity Pools - Retrieve related Transactions <https://developers.stellar.org/api/resources/liquiditypools/transactions/>`__

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: this TransactionsCallBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}/transactions"
        return self

    def include_failed(self, include_failed: bool):
        """Adds a parameter defining whether to include failed transactions. By default only
        transactions of successful transactions are returned.

        :param include_failed: Set to `True` to include failed transactions.
        :return: current TransactionsCallBuilder instance
        """
        self._add_query_param("include_failed", include_failed)
        return self
