from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseOperationsCallBuilder"]


class BaseOperationsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`OperationsCallBuilder` pointed to server defined by horizon_url.

    See `All Operations <https://www.stellar.org/developers/horizon/reference/endpoints/operations-all.html>`__

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "operations"

    def operation(self, operation_id: Union[int, str]):
        """The operation details endpoint provides information on a single operation. The operation ID provided
        in the id argument specifies which operation to load.

        See `Operation Details <https://www.stellar.org/developers/horizon/reference/endpoints/operations-single.html>`__

        :param operation_id: Operation ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"operations/{operation_id}"
        return self

    def for_account(self, account_id: str):
        """This endpoint represents all operations that were included in valid transactions that
        affected a particular account.

        See `Operations for Account <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-account.html>`__

        :param account_id: Account ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/operations"
        return self

    def for_ledger(self, sequence: Union[int, str]):
        """This endpoint returns all operations that occurred in a given ledger.

        See `Operations for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-ledger.html>`__

        :param sequence: Sequence ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}/operations"
        return self

    def for_transaction(self, transaction_hash: str):
        """This endpoint represents all operations that are part of a given transaction.

        See `Operations for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-transaction.html>`__

        :param transaction_hash: Transaction Hash
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"transactions/{transaction_hash}/operations"
        return self

    def for_claimable_balance(self, claimable_balance_id: str):
        """This endpoint represents successful operations referencing a given
        claimable balance and can be used in streaming mode.


        See `Claimable Balances - Retrieve related Operations <https://developers.stellar.org/api/resources/claimablebalances/operations/>`__

        :param claimable_balance_id: This claimable balance’s id encoded in a hex string representation.
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"claimable_balances/{claimable_balance_id}/operations"
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """This endpoint represents all operations that are part of a given liquidity pool.

        See `Liquidity Pools - Retrieve related Operations <https://developers.stellar.org/api/resources/liquiditypools/operations/>`__

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}/operations"
        return self

    def include_failed(self, include_failed: bool):
        """Adds a parameter defining whether to include failed transactions. By default only
        operations of successful transactions are returned.

        :param include_failed: Set to `True` to include operations of failed transactions.
        :return: current OperationsCallBuilder instance
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
