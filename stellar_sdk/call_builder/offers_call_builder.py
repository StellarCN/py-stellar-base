from typing import Union

from ..call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class OffersCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`OffersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.offers`.

    See `Offers for Account <https://www.stellar.org/developers/horizon/reference/endpoints/offers-for-account.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param account_id: Account ID.
    """

    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        account_id: str,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "accounts/{account_id}/offers".format(
            account_id=account_id
        )
