from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseDataCallBuilder"]


class BaseDataCallBuilder(BaseCallBuilder):
    """Creates a new :class:`DataCallBuilder` pointed to server defined by horizon_url.

    See `Retrieve an Account's Data <https://developers.stellar.org/api/resources/accounts/data/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param account_id: account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
    :param data_name: Key name
    """

    def __init__(self, account_id: str, data_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.endpoint: str = f"/accounts/{account_id}/data/{data_name}"
