from ...call_builder.base import BaseDataCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["DataCallBuilder"]


class DataCallBuilder(BaseCallBuilder, BaseDataCallBuilder):
    """Creates a new :class:`DataCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.data`.

    See `Retrieve an Account's Data <https://developers.stellar.org/api/resources/accounts/data/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param account_id: account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
    :param data_name: Key name
    """

    def __init__(
        self,
        horizon_url: str,
        client: BaseSyncClient,
        account_id: str,
        data_name: str,
    ) -> None:
        super().__init__(  # type: ignore[call-arg]
            horizon_url=horizon_url,
            client=client,
            account_id=account_id,
            data_name=data_name,
        )
