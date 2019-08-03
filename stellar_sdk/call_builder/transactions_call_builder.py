from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class TransactionsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "transactions"

    def transaction(self, transaction_hash: str) -> "TransactionsCallBuilder":
        self.endpoint = "transactions/{transaction_hash}".format(
            transaction_hash=transaction_hash
        )
        return self

    def for_account(self, account_id: str) -> "TransactionsCallBuilder":
        self.endpoint = "accounts/{account_id}/transactions".format(
            account_id=account_id
        )
        return self

    def for_ledger(self, sequence: Union[str, int]) -> "TransactionsCallBuilder":
        self.endpoint = "ledgers/{sequence}/transactions".format(sequence=sequence)
        return self

    def include_failed(self, include_failed: bool) -> "TransactionsCallBuilder":
        self._add_query_param("include_failed", include_failed)
        return self
