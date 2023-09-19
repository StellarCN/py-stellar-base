from ...call_builder.base import BasePaymentsCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["PaymentsCallBuilder"]


class PaymentsCallBuilder(BaseCallBuilder, BasePaymentsCallBuilder):
    """Creates a new :class:`PaymentsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.payments`.

    See `List All Payments <https://developers.stellar.org/api/resources/operations/list-payments/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
