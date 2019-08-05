from typing import Union

from stellar_sdk.call_builder import BaseCallBuilder
from stellar_sdk.client.base_async_client import BaseAsyncClient
from stellar_sdk.client.base_sync_client import BaseSyncClient


class OffersCallBuilder(BaseCallBuilder):
    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        account_id: str,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "accounts/{account_id}/offers".format(account_id=account_id)
