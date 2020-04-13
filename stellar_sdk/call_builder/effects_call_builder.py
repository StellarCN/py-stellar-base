from typing import Union, TypeVar, List, AsyncGenerator, Generator

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..response.effect_response import (
    EFFECT_RESPONSE_TYPE_UNION,
    EFFECT_RESPONSE_TYPE_UNION_TYPE,
    EFFECT_TYPE_I_RESPONSE,
)
from ..response.wrapped_response import WrappedResponse

T = TypeVar("T")


class EffectsCallBuilder(BaseCallBuilder[T]):
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

    def for_account(self, account_id: str) -> "EffectsCallBuilder[T]":
        """This endpoint represents all effects that changed a given account. It will return relevant
        effects from the creation of the account to the current ledger.

        See `Effects for Account <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`_

        :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: this EffectCallBuilder instance
        """
        self.endpoint = "accounts/{account_id}/effects".format(account_id=account_id)
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "EffectsCallBuilder[T]":
        """Effects are the specific ways that the ledger was changed by any operation.
        This endpoint represents all effects that occurred in the given ledger.

        See `Effects for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-account.html>`_

        :param sequence: ledger sequence
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = "ledgers/{sequence}/effects".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "EffectsCallBuilder[T]":
        """This endpoint represents all effects that occurred as a result of a given transaction.

        See `Effects for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-transaction.html>`_

        :param transaction_hash: transaction hash
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = "transactions/{transaction_hash}/effects".format(
            transaction_hash=transaction_hash
        )
        return self

    def for_operation(self, operation_id: Union[int, str]) -> "EffectsCallBuilder[T]":
        """This endpoint represents all effects that occurred as a result of a given operation.

        See `Effects for Operation <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-operation.html>`_

        :param operation_id: operation ID
        :return: this EffectCallBuilder instance
        """
        self.endpoint: str = "operations/{operation_id}/effects".format(
            operation_id=operation_id
        )
        return self

    def _get_corresponding_response_type(
        self, operation_json
    ) -> EFFECT_RESPONSE_TYPE_UNION_TYPE:
        operation_type = operation_json["type_i"]
        if operation_type not in EFFECT_TYPE_I_RESPONSE:
            raise NotImplementedError(
                "The type of effect is %d, which is not currently supported in the version. "
                "Please try to upgrade the SDK or raise an issue." % operation_type
            )
        return EFFECT_TYPE_I_RESPONSE[operation_type]

    def _parse_response(
        self, raw_data: dict
    ) -> Union[List[EFFECT_RESPONSE_TYPE_UNION], EFFECT_RESPONSE_TYPE_UNION]:
        return self._base_parse_response(
            raw_data, model_selector=self._get_corresponding_response_type
        )

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[WrappedResponse[EFFECT_RESPONSE_TYPE_UNION], None],
        Generator[WrappedResponse[EFFECT_RESPONSE_TYPE_UNION], None, None],
    ]:
        return self._stream()
