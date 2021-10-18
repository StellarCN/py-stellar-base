from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseDataCallBuilder"]


class BaseDataCallBuilder(BaseCallBuilder):
    """Creates a new :class:`DataCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.data`.

    See `Data for Account <https://www.stellar.org/developers/horizon/reference/endpoints/data-for-account.html>`_

    :param horizon_url: Horizon server URL.
    :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
    :param data_name: Key name
    """

    def __init__(
        self,
        horizon_url: str,
        account_id: str,
        data_name: str,
    ) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = f"/accounts/{account_id}/data/{data_name}"
