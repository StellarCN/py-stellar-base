from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class OperationsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "operations"

    def operation(self, operation_id: Union[int, str]) -> "OperationsCallBuilder":
        self.endpoint = "operations/{operation_id}".format(operation_id=operation_id)
        return self

    def for_account(self, account_id: str) -> "OperationsCallBuilder":
        self.endpoint = "accounts/{account_id}/operations".format(account_id=account_id)
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "OperationsCallBuilder":
        self.endpoint = "ledgers/{sequence}/operations".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "OperationsCallBuilder":
        self.endpoint = "transactions/{transaction_hash}/operations".format(
            transaction_hash=transaction_hash
        )
        return self

    def include_failed(self, include_failed: bool) -> "OperationsCallBuilder":
        self._add_query_param("include_failed", include_failed)
        return self
