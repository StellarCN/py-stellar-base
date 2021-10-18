from ...call_builder.base import BaseDataCallBuilder
from ...call_builder.call_builder_async.base_call_builder_async import (
    BaseCallBuilderAsync,
)
from ...client.base_async_client import BaseAsyncClient

__all__ = ["DataCallBuilder"]


class DataCallBuilder(BaseCallBuilderAsync, BaseDataCallBuilder):
    """Creates a new :class:`DataCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.data`.

    See `Data for Account <https://www.stellar.org/developers/horizon/reference/endpoints/data-for-account.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
    :param data_name: Key name
    """

    def __init__(
        self,
        horizon_url: str,
        client: BaseAsyncClient,
        account_id: str,
        data_name: str,
    ) -> None:
        super().__init__(
            horizon_url=horizon_url,
            client=client,
            account_id=account_id,
            data_name=data_name,
        )
