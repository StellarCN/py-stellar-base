from ...call_builder.base import BaseRootCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["RootCallBuilder"]


class RootCallBuilder(BaseCallBuilder, BaseRootCallBuilder):
    """Creates a new :class:`RootCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.root`.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)

    def stream(
        self,
    ):
        """This endpoint does not support streaming."""
        raise NotImplementedError("Streaming is not supported.")
