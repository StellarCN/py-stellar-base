from ...call_builder.base import BaseAssetsCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["AssetsCallBuilder"]


class AssetsCallBuilder(BaseCallBuilder, BaseAssetsCallBuilder):
    """Creates a new :class:`AssetsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.assets`.

    See `All Assets <https://www.stellar.org/developers/horizon/reference/endpoints/assets-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
