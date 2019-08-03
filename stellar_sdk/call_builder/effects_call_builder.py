from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class EffectsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "effects"

    def for_account(self, account_id: str) -> "EffectsCallBuilder":
        self.endpoint = "accounts/{account_id}/effects".format(account_id=account_id)
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "EffectsCallBuilder":
        self.endpoint = "ledgers/{sequence}/effects".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "EffectsCallBuilder":
        self.endpoint = "transactions/{transaction_hash}/effects".format(
            transaction_hash=transaction_hash
        )
        return self

    def for_operation(self, operation_id: Union[int, str]) -> "EffectsCallBuilder":
        self.endpoint = "operations/{operation_id}/effects".format(
            operation_id=operation_id
        )
        return self
