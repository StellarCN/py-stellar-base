from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class DataCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`DataCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.data`.

    See `Data for Account <https://www.stellar.org/developers/horizon/reference/endpoints/data-for-account.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
    :param data_name: Key name
    """

    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        account_id: str,
        data_name: str,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = f"/accounts/{account_id}/data/{data_name}"
