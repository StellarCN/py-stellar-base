from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class LedgersCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "ledgers"

    def ledger(self, sequence: Union[int, str]) -> "LedgersCallBuilder":
        self.endpoint = "ledgers/{sequence}".format(sequence=sequence)
        return self
