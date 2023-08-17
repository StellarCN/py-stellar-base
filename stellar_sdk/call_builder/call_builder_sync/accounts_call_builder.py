from ...call_builder.base.base_accounts_call_builder import BaseAccountsCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["AccountsCallBuilder"]


class AccountsCallBuilder(BaseCallBuilder, BaseAccountsCallBuilder):
    """Creates a new :class:`AccountsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.accounts`.

    See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
