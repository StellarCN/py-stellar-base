from decimal import Decimal
from typing import Any, Coroutine, Dict, Generator, List, Tuple, Union

from .account import Account
from .asset import Asset
from .base_transaction_envelope import BaseTransactionEnvelope
from .call_builder.base import (
    BaseAccountsCallBuilder,
    BaseAssetsCallBuilder,
    BaseClaimableBalancesCallBuilder,
    BaseDataCallBuilder,
    BaseEffectsCallBuilder,
    BaseFeeStatsCallBuilder,
    BaseLedgersCallBuilder,
    BaseLiquidityPoolsBuilder,
    BaseOffersCallBuilder,
    BaseOperationsCallBuilder,
    BaseOrderbookCallBuilder,
    BasePaymentsCallBuilder,
    BaseRootCallBuilder,
    BaseStrictReceivePathsCallBuilder,
    BaseStrictSendPathsCallBuilder,
    BaseTradeAggregationsCallBuilder,
    BaseTradesCallBuilder,
    BaseTransactionsCallBuilder,
)
from .fee_bump_transaction import FeeBumpTransaction
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .helpers import parse_transaction_envelope_from_xdr
from .keypair import Keypair
from .muxed_account import MuxedAccount
from .operation import (
    AccountMerge,
    PathPaymentStrictReceive,
    PathPaymentStrictSend,
    Payment,
)
from .sep.exceptions import AccountRequiresMemoError
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope

__all__ = ["BaseServer"]


class BaseServer:
    def submit_transaction(
        self,
        transaction_envelope: Union[
            TransactionEnvelope, FeeBumpTransactionEnvelope, str
        ],
        skip_memo_required_check: bool = False,
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        """Submits a transaction to the network.

        :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object
            or base64 encoded xdr
        :param skip_memo_required_check: Allow skipping memo
        :return: the response from horizon
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
            :exc:`AccountRequiresMemoError <stellar_sdk.sep.exceptions.AccountRequiresMemoError>`
        """
        raise NotImplementedError

    def _get_xdr_and_transaction_from_transaction_envelope(
        self,
        transaction_envelope: Union[
            TransactionEnvelope, FeeBumpTransactionEnvelope, str
        ],
    ) -> Tuple[str, Union[Transaction, FeeBumpTransaction]]:
        if isinstance(transaction_envelope, BaseTransactionEnvelope):
            xdr = transaction_envelope.to_xdr()
            tx = transaction_envelope.transaction
        else:
            xdr = transaction_envelope
            tx = parse_transaction_envelope_from_xdr(
                transaction_envelope, ""
            ).transaction
        return xdr, tx

    def root(self) -> BaseRootCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.RootCallBuilder` object configured
            by a current Horizon server configuration.
        """
        raise NotImplementedError

    def accounts(self) -> BaseAccountsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.AccountsCallBuilder` object configured
            by a current Horizon server configuration.
        """
        raise NotImplementedError

    def assets(self) -> BaseAssetsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.AssetsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def claimable_balances(self) -> BaseClaimableBalancesCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.ClaimableBalancesCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def data(self, account_id: str, data_name: str) -> BaseDataCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.DataCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def effects(self) -> BaseEffectsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.EffectsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def fee_stats(self) -> BaseFeeStatsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.FeeStatsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def ledgers(self) -> BaseLedgersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.LedgersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def liquidity_pools(self) -> BaseLiquidityPoolsBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.LiquidityPoolsBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def offers(self) -> BaseOffersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.OffersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def operations(self) -> BaseOperationsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.OperationsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def orderbook(self, selling: Asset, buying: Asset) -> BaseOrderbookCallBuilder:
        """
        :param selling: Asset being sold
        :param buying: Asset being bought
        :return: New :class:`stellar_sdk.call_builder.OrderbookCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def strict_receive_paths(
        self,
        source: Union[str, List[Asset]],
        destination_asset: Asset,
        destination_amount: Union[str, Decimal],
    ) -> BaseStrictReceivePathsCallBuilder:
        """
        :param source: The sender's account ID or a list of Assets. Any returned path must use a source that the sender can hold.
        :param destination_asset: The destination asset.
        :param destination_amount: The amount, denominated in the destination asset, that any returned path should be able to satisfy.
        :return: New :class:`stellar_sdk.call_builder.StrictReceivePathsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def strict_send_paths(
        self,
        source_asset: Asset,
        source_amount: Union[str, Decimal],
        destination: Union[str, List[Asset]],
    ) -> BaseStrictSendPathsCallBuilder:
        """
        :param source_asset: The asset to be sent.
        :param source_amount: The amount, denominated in the source asset, that any returned path should be able to satisfy.
        :param destination: The destination account or the destination assets.
        :return: New :class:`stellar_sdk.call_builder.StrictReceivePathsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def payments(self) -> BasePaymentsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.PaymentsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def trade_aggregations(
        self,
        base: Asset,
        counter: Asset,
        resolution: int,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
    ) -> BaseTradeAggregationsCallBuilder:
        """
        :param base: base asset
        :param counter: counter asset
        :param resolution: segment duration as millis since epoch. *Supported values
            are 1 minute (60000), 5 minutes (300000), 15 minutes (900000),
            1 hour (3600000), 1 day (86400000) and 1 week (604800000).*
        :param start_time: lower time boundary represented as millis since epoch
        :param end_time: upper time boundary represented as millis since epoch
        :param offset: segments can be offset using this parameter.
            Expressed in milliseconds. *Can only be used if the resolution is greater than 1 hour.
            Value must be in whole hours, less than the provided resolution, and less than 24 hours.*
        :return: New :class:`stellar_sdk.call_builder.TradeAggregationsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def trades(self) -> BaseTradesCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.TradesCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def transactions(self) -> BaseTransactionsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.TransactionsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        raise NotImplementedError

    def load_account(
        self, account_id: Union[MuxedAccount, Keypair, str]
    ) -> Union[Account, Coroutine[Any, Any, Account]]:
        """Fetches an account's most current base state (like sequence) in the ledger and then creates
        and returns an :class:`stellar_sdk.account.Account` object.

        If you want to get complete account information, please
        use :func:`stellar_sdk.server.Server.accounts`.

        :param account_id: The account to load.
        :return: an :class:`stellar_sdk.account.Account` object.
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
        """
        raise NotImplementedError

    def _check_destination_memo(
        self, account_resp: dict, index: int, destination: str
    ) -> None:
        memo_required_config_key = "config.memo_required"
        memo_required_config_value = "MQ=="
        data = account_resp["data"]
        if data.get(memo_required_config_key) == memo_required_config_value:
            raise AccountRequiresMemoError(
                "Destination account requires a memo in the transaction.",
                destination,
                index,
            )

    def _get_check_memo_required_destinations(
        self, transaction: Transaction
    ) -> Generator[Tuple[int, str], Any, Any]:
        destinations = set()
        for index, operation in enumerate(transaction.operations):
            if isinstance(
                operation,
                (
                    Payment,
                    AccountMerge,
                    PathPaymentStrictSend,
                    PathPaymentStrictReceive,
                ),
            ):
                destination: str = operation.destination.account_id
            else:
                continue
            if destination in destinations:
                continue
            destinations.add(destination)
            yield index, destination

    def fetch_base_fee(self) -> Union[int, Coroutine[Any, Any, int]]:
        """Fetch the base fee. Since this hits the server, if the server call fails,
        you might get an error. You should be prepared to use a default value if that happens.

        :return: the base fee
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
        """
        raise NotImplementedError

    def _handle_base_fee(self, latest_ledger: dict) -> int:
        base_fee = 100
        if (
            latest_ledger["_embedded"]
            and latest_ledger["_embedded"]["records"]
            and latest_ledger["_embedded"]["records"][0]
        ):
            base_fee = int(
                latest_ledger["_embedded"]["records"][0]["base_fee_in_stroops"]
            )
        return base_fee

    def close(self) -> Union[None, Coroutine[Any, Any, None]]:
        """Close underlying connector.

        Release all acquired resources.
        """
        raise NotImplementedError

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
