from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class AccountsCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`AccountsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.accounts`.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "accounts"

    def account_id(self, account_id: str) -> "AccountsCallBuilder":
        """Returns information and links relating to a single account.
        The balances section in the returned JSON will also list all the trust lines this account has set up.

        See `Account Details <https://www.stellar.org/developers/horizon/reference/endpoints/accounts-single.html>`_

        :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: current AccountCallBuilder instance
        """
        self.endpoint = "accounts/{account_id}".format(account_id=account_id)
        return self
