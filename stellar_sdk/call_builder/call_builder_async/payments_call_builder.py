from ...call_builder.base import BasePaymentsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient
from ...type_checked import type_checked

__all__ = ["PaymentsCallBuilder"]


@type_checked
class PaymentsCallBuilder(BaseCallBuilder, BasePaymentsCallBuilder):
    """Creates a new :class:`PaymentsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.payments`.

    See `List All Payments <https://developers.stellar.org/api/resources/operations/list-payments/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
