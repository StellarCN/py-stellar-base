from typing import Union, TypeVar

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..response.root_response import RootResponse

T = TypeVar("T")


class RootCallBuilder(BaseCallBuilder[T]):
    """ Creates a new :class:`RootCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.root`.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)

    def _parse_response(self, raw_data: dict) -> RootResponse:
        return self._base_parse_response(raw_data, RootResponse)
