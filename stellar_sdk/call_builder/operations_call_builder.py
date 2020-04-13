from typing import Union, TypeVar, List, AsyncGenerator, Generator

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..response.operation_response import (
    OPERATION_RESPONSE_TYPE_UNION,
    OPERATION_TYPE_I_RESPONSE,
    OPERATION_TYPE_I_RESPONSE_TYPE,
)
from ..response.wrapped_response import WrappedResponse

T = TypeVar("T")


class OperationsCallBuilder(BaseCallBuilder[T]):
    """ Creates a new :class:`OperationsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.operations`.

    See `All Operations <https://www.stellar.org/developers/horizon/reference/endpoints/operations-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "operations"

    def operation(
        self, operation_id: Union[int, str]
    ) -> "OperationsCallBuilder[OPERATION_RESPONSE_TYPE_UNION]":
        """The operation details endpoint provides information on a single operation. The operation ID provided
        in the id argument specifies which operation to load.

        See `Operation Details <https://www.stellar.org/developers/horizon/reference/endpoints/operations-single.html>`_

        :param operation_id: Operation ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint = "operations/{operation_id}".format(operation_id=operation_id)
        return self

    def for_account(self, account_id: str) -> "OperationsCallBuilder[T]":
        """This endpoint represents all operations that were included in valid transactions that
        affected a particular account.

        See `Operations for Account <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-account.html>`_

        :param account_id: Account ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint: str = "accounts/{account_id}/operations".format(
            account_id=account_id
        )
        return self

    def for_ledger(self, sequence: Union[int, str]) -> "OperationsCallBuilder[T]":
        """This endpoint returns all operations that occurred in a given ledger.

        See `Operations for Ledger <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-ledger.html>`_

        :param sequence: Sequence ID
        :return: this OperationCallBuilder instance
        """
        self.endpoint: str = "ledgers/{sequence}/operations".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash: str) -> "OperationsCallBuilder[T]":
        """This endpoint represents all operations that are part of a given transaction.

        See `Operations for Transaction <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-transaction.html>`_

        :param transaction_hash:
        :return: this OperationCallBuilder instance
        """
        self.endpoint: str = "transactions/{transaction_hash}/operations".format(
            transaction_hash=transaction_hash
        )
        return self

    def include_failed(self, include_failed: bool) -> "OperationsCallBuilder[T]":
        """Adds a parameter defining whether to include failed transactions. By default only
        operations of successful transactions are returned.

        :param include_failed: Set to `True` to include operations of failed transactions.
        :return: current OperationsCallBuilder instance
        """
        self._add_query_param("include_failed", include_failed)
        return self

    def join(self, join: str) -> "OperationsCallBuilder[T]":
        """join represents `join` param in queries, currently only supports `transactions`

        :param join: join represents `join` param in queries, currently only supports `transactions`
        :return: current OperationsCallBuilder instance
        """
        self._add_query_param("join", join)
        return self

    def _get_corresponding_response_type(
        self, operation_json
    ) -> OPERATION_TYPE_I_RESPONSE_TYPE:
        operation_type = operation_json["type_i"]
        if operation_type not in OPERATION_TYPE_I_RESPONSE:
            raise NotImplementedError(
                "The type of operation is %d, which is not currently supported in the version. "
                "Please try to upgrade the SDK or raise an issue." % operation_type
            )
        return OPERATION_TYPE_I_RESPONSE[operation_type]

    def _parse_response(
        self, raw_data: dict
    ) -> Union[List[OPERATION_RESPONSE_TYPE_UNION], OPERATION_RESPONSE_TYPE_UNION]:
        return self._base_parse_response(
            raw_data, model_selector=self._get_corresponding_response_type
        )

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[WrappedResponse[OPERATION_RESPONSE_TYPE_UNION], None],
        Generator[WrappedResponse[OPERATION_RESPONSE_TYPE_UNION], None, None],
    ]:
        return self._stream()
