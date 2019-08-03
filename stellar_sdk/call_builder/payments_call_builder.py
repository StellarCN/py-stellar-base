from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class PaymentsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "payments"

    def for_account(self, account_id: str) -> "PaymentsCallBuilder":
        self.endpoint = "accounts/{account_id}/payments".format(account_id=account_id)
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "PaymentsCallBuilder":
        self.endpoint = "ledgers/{sequence}/payments".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "PaymentsCallBuilder":
        self.endpoint = "transactions/{transaction_hash}/payments".format(
            transaction_hash=transaction_hash
        )
        return self
