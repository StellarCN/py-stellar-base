from ...call_builder.base import BaseAssetsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient
from ...type_checked import type_checked

__all__ = ["AssetsCallBuilder"]


@type_checked
class AssetsCallBuilder(BaseCallBuilder, BaseAssetsCallBuilder):
    """Creates a new :class:`AssetsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.assets`.

    See `List All Assets <https://developers.stellar.org/api/resources/assets/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
