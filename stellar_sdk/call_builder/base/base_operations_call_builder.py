from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseOperationsCallBuilder"]


class BaseOperationsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`OperationsCallBuilder` pointed to server defined by horizon_url.

    See `List All Operations <https://developers.stellar.org/api/resources/operations/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "operations"

    def operation(self, operation_id: Union[int, str]):
        """The operation details endpoint provides information on a single operation. The operation ID provided
        in the id argument specifies which operation to load.

        See `Retrieve an Operation <https://developers.stellar.org/api/resources/operations/single/>`__ for more information.

        :param operation_id: Operation ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"operations/{operation_id}"
        return self

    def for_account(self, account_id: str):
        """This endpoint represents all operations that were included in valid transactions that
        affected a particular account.

        See `Retrieve an Account's Operations <https://developers.stellar.org/api/resources/accounts/operations/>`__ for more information.

        :param account_id: Account ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/operations"
        return self

    def for_ledger(self, sequence: Union[int, str]):
        """This endpoint returns all operations that occurred in a given ledger.

        See `Retrieve a Ledger's Operations <https://developers.stellar.org/api/resources/ledgers/operations/>`__ for more information.

        :param sequence: Sequence ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}/operations"
        return self

    def for_transaction(self, transaction_hash: str):
        """This endpoint represents all operations that are part of a given transaction.

        See `Retrieve a Transaction's Operations <https://developers.stellar.org/api/resources/transactions/operations/>`__ for more information.

        :param transaction_hash: Transaction Hash
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"transactions/{transaction_hash}/operations"
        return self

    def for_claimable_balance(self, claimable_balance_id: str):
        """This endpoint represents successful operations referencing a given
        claimable balance and can be used in streaming mode.


        See `Claimable Balances - Retrieve related Operations <https://developers.stellar.org/api/resources/claimablebalances/operations/>`__ for more information.

        :param claimable_balance_id: This claimable balance’s id encoded in a hex string representation.
        :return: this OperationCallBuilder instance
        """
        self.endpoint = f"claimable_balances/{claimable_balance_id}/operations"
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """This endpoint represents all operations that are part of a given liquidity pool.

        See `Liquidity Pools - Retrieve related Operations <https://developers.stellar.org/api/resources/liquiditypools/operations/>`__ for more information.

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
