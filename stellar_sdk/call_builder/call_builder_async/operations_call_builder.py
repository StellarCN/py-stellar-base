from ...call_builder.base import BaseOperationsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient

__all__ = ["OperationsCallBuilder"]


class OperationsCallBuilder(BaseCallBuilder, BaseOperationsCallBuilder):
    """Creates a new :class:`OperationsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.operations`.

    See `List All Operations <https://developers.stellar.org/api/resources/operations/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
