from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class LedgersCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`LedgersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.ledgers`.

    See `All Ledgers <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "ledgers"

    def ledger(self, sequence: Union[int, str]) -> "LedgersCallBuilder":
        """Provides information on a single ledger.

        See `Ledger Details <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-single.html>`_

        :param sequence: Ledger sequence
        :return: current LedgerCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}"
        return self
