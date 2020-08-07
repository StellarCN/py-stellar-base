from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class EffectsCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`EffectsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.effects`.

    See `All Effects <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "effects"

    def for_account(self, account_id: str) -> "EffectsCallBuilder":
        """This endpoint represents all effects that changed a given account. It will return relevant
        effects from the creation of the account to the current ledger.

        See `Effects for Account <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`_

        :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: this EffectCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/effects"
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "EffectsCallBuilder":
        """Effects are the specific ways that the ledger was changed by any operation.
        This endpoint represents all effects that occurred in the given ledger.

        See `Effects for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-account.html>`_

        :param sequence: ledger sequence
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = f"ledgers/{sequence}/effects"
        return self

    def for_transaction(self, transaction_hash: str) -> "EffectsCallBuilder":
        """This endpoint represents all effects that occurred as a result of a given transaction.

        See `Effects for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-transaction.html>`_

        :param transaction_hash: transaction hash
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = f"transactions/{transaction_hash}/effects"
        return self

    def for_operation(self, operation_id: Union[int, str]) -> "EffectsCallBuilder":
        """This endpoint represents all effects that occurred as a result of a given operation.

        See `Effects for Operation <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-operation.html>`_

        :param operation_id: operation ID
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = f"operations/{operation_id}/effects"
        return self
