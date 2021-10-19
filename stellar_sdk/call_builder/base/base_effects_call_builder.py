from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseEffectsCallBuilder"]


class BaseEffectsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`EffectsCallBuilder` pointed to server defined by horizon_url.

    See `All Effects <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`__

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "effects"

    def for_account(self, account_id: str):
        """This endpoint represents all effects that changed a given account. It will return relevant
        effects from the creation of the account to the current ledger.

        See `Effects for Account <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`__

        :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: this EffectCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/effects"
        return self

    def for_ledger(self, sequence: Union[int, str]):
        """Effects are the specific ways that the ledger was changed by any operation.
        This endpoint represents all effects that occurred in the given ledger.

        See `Effects for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-account.html>`__

        :param sequence: ledger sequence
        :return: this EffectCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}/effects"
        return self

    def for_transaction(self, transaction_hash: str):
        """This endpoint represents all effects that occurred as a result of a given transaction.

        See `Effects for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-transaction.html>`__

        :param transaction_hash: transaction hash
        :return: this EffectCallBuilder instance
        """
        self.endpoint = f"transactions/{transaction_hash}/effects"
        return self

    def for_operation(self, operation_id: Union[int, str]):
        """This endpoint represents all effects that occurred as a result of a given operation.

        See `Effects for Operation <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-operation.html>`__

        :param operation_id: operation ID
        :return: this EffectCallBuilder instance
        """
        self.endpoint = f"operations/{operation_id}/effects"
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """This endpoint represents all effects that occurred as a result of a given liquidity pool.

        See `Liquidity Pools - Retrieve related Effects <https://developers.stellar.org/api/resources/liquiditypools/effects/>`__

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: this EffectsCallBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}/effects"
        return self
