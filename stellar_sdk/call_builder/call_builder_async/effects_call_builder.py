from ...call_builder.base import BaseEffectsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient
from ...type_checked import type_checked

__all__ = ["EffectsCallBuilder"]


@type_checked
class EffectsCallBuilder(BaseCallBuilder, BaseEffectsCallBuilder):
    """Creates a new :class:`EffectsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.effects`.

    See `List All Effects <https://developers.stellar.org/api/resources/effects/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
