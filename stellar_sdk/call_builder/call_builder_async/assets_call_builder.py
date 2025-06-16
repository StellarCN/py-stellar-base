from ...call_builder.base import BaseAssetsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient

__all__ = ["AssetsCallBuilder"]


class AssetsCallBuilder(BaseCallBuilder, BaseAssetsCallBuilder):
    """Creates a new :class:`AssetsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.assets`.

    See `Assets <https://developers.stellar.org/docs/data/apis/horizon/api-reference/resources/assets>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
