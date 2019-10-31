from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class AssetsCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`AssetsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.assets`.

    See `All Assets <https://www.stellar.org/developers/horizon/reference/endpoints/assets-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "assets"

    def for_code(self, asset_code: str) -> "AssetsCallBuilder":
        """ This endpoint filters all assets by the asset code.

        :param asset_code: asset code, for example: `USD`
        :return: current AssetCallBuilder instance
        """
        self._add_query_param("asset_code", asset_code)
        return self

    def for_issuer(self, asset_issuer: str) -> "AssetsCallBuilder":
        """ This endpoint filters all assets by the asset issuer.

        :param asset_issuer: asset issuer,
            for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: current AssetCallBuilder instance
        """
        self._add_query_param("asset_issuer", asset_issuer)
        return self
