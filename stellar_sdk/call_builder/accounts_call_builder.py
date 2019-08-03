from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class AccountsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "accounts"

    def account_id(self, account_id: str) -> "AccountsCallBuilder":
        self.endpoint = "accounts/{account_id}".format(account_id=account_id)
        return self
