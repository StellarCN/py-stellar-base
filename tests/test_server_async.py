from decimal import Decimal

import pytest

from stellar_sdk import (
    AiohttpClient,
    Asset,
    FeeBumpTransactionEnvelope,
    MuxedAccount,
    Network,
    ServerAsync,
    TransactionEnvelope,
)
from stellar_sdk.account import Thresholds
from stellar_sdk.call_builder.call_builder_async import *
from tests import _horizon_fixtures as hf


@pytest.mark.asyncio
class TestServerAsync:
    async def test_load_acount(self, horizon_mock):
        account_id = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
        client = AiohttpClient()
        horizon_mock.expect(f"/accounts/{account_id}", json=hf.account(account_id))
        async with ServerAsync(horizon_mock.url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == MuxedAccount.from_account(account_id)
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_load_acount_muxed_account_str(self, horizon_mock):
        account_id = (
            "MDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQAAAAAAAAAAE2KS7Y"
        )
        base_account_id = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
        client = AiohttpClient()
        horizon_mock.expect(
            f"/accounts/{base_account_id}", json=hf.account(base_account_id)
        )
        async with ServerAsync(horizon_mock.url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == MuxedAccount.from_account(account_id)
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_load_acount_muxed_account(self, horizon_mock):
        account_id = MuxedAccount(
            "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D", 1234
        )
        client = AiohttpClient()
        horizon_mock.expect(
            f"/accounts/{account_id.account_id}", json=hf.account(account_id.account_id)
        )
        async with ServerAsync(horizon_mock.url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == account_id
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_fetch_base_fee(self, horizon_mock):
        client = AiohttpClient()
        horizon_mock.expect("/ledgers", json=hf.ledger())
        async with ServerAsync(horizon_mock.url, client) as server:
            base_fee = await server.fetch_base_fee()
            assert base_fee == 100

    async def test_endpoint(self, horizon_mock):
        horizon_url = horizon_mock.url
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            assert server.accounts() == AccountsCallBuilder(horizon_url, client)
            assert server.assets() == AssetsCallBuilder(horizon_url, client)
            assert server.claimable_balances() == ClaimableBalancesCallBuilder(
                horizon_url, client
            )
            assert server.data(
                "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D", "hello"
            ) == DataCallBuilder(
                horizon_url,
                client,
                "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D",
                "hello",
            )
            assert server.effects() == EffectsCallBuilder(horizon_url, client)
            assert server.fee_stats() == FeeStatsCallBuilder(horizon_url, client)
            assert server.ledgers() == LedgersCallBuilder(horizon_url, client)
            assert server.liquidity_pools() == LiquidityPoolsBuilder(
                horizon_url, client
            )
            assert server.offers() == OffersCallBuilder(horizon_url, client)
            assert server.operations() == OperationsCallBuilder(horizon_url, client)
            buying = Asset.native()
            selling = Asset(
                "MOE", "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
            )
            assert server.orderbook(buying, selling) == OrderbookCallBuilder(
                horizon_url, client, buying, selling
            )
            source = "GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH"
            destination_asset = Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            )
            destination_amount = "20.0"
            assert server.strict_receive_paths(
                source, destination_asset, destination_amount
            ) == StrictReceivePathsCallBuilder(
                horizon_url, client, source, destination_asset, destination_amount
            )
            destination_amount = Decimal("20.0")
            assert server.strict_receive_paths(
                source, destination_asset, destination_amount
            ) == StrictReceivePathsCallBuilder(
                horizon_url, client, source, destination_asset, destination_amount
            )
            source_asset = Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            )
            source_amount = "10.25"
            destination = "GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP"
            assert server.strict_send_paths(
                source_asset, source_amount, destination
            ) == StrictSendPathsCallBuilder(
                horizon_url, client, source_asset, source_amount, destination
            )
            source_amount = Decimal("10.25")
            assert server.strict_send_paths(
                source_asset, source_amount, destination
            ) == StrictSendPathsCallBuilder(
                horizon_url, client, source_asset, source_amount, destination
            )

            assert server.payments() == PaymentsCallBuilder(horizon_url, client)
            assert server.root() == RootCallBuilder(horizon_url, client)
            base = Asset.native()
            counter = Asset(
                "MOE", "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
            )
            resolution = 3600000
            start_time = 1565272000000
            end_time = 1565278000000
            offset = 3600000
            assert server.trade_aggregations(
                base, counter, resolution, start_time, end_time, offset
            ) == TradeAggregationsCallBuilder(
                horizon_url,
                client,
                base,
                counter,
                resolution,
                start_time,
                end_time,
                offset,
            )
            assert server.trades() == TradesCallBuilder(horizon_url, client)
            assert server.transactions() == TransactionsCallBuilder(horizon_url, client)

    async def test_submit_transaction_with_xdr(self, horizon_mock):
        client = AiohttpClient()
        horizon_mock.expect(
            "/transactions", method="POST", json=hf.submit_transaction()
        )
        async with ServerAsync(horizon_mock.url, client) as server:
            resp = await server.submit_transaction(hf.TRANSACTION_XDR, True)
            assert resp["envelope_xdr"] == hf.TRANSACTION_XDR

    async def test_submit_transaction_with_te(self, horizon_mock):
        client = AiohttpClient()
        horizon_mock.expect(
            "/transactions", method="POST", json=hf.submit_transaction()
        )
        try:
            te = TransactionEnvelope.from_xdr(
                hf.TRANSACTION_XDR, Network.PUBLIC_NETWORK_PASSPHRASE
            )
        except ValueError:
            te = FeeBumpTransactionEnvelope.from_xdr(
                hf.TRANSACTION_XDR, Network.PUBLIC_NETWORK_PASSPHRASE
            )
        async with ServerAsync(horizon_mock.url, client) as server:
            resp = await server.submit_transaction(te, True)
            assert resp["envelope_xdr"] == hf.TRANSACTION_XDR

    async def test_submit_transaction_async_with_xdr(self, horizon_mock):
        client = AiohttpClient()
        te = TransactionEnvelope.from_xdr(
            hf.TRANSACTION_XDR, Network.PUBLIC_NETWORK_PASSPHRASE
        )
        assert te.hash_hex() == hf.TRANSACTION_HASH
        horizon_mock.expect(
            "/transactions_async",
            method="POST",
            json=hf.submit_transaction_async(hf.TRANSACTION_HASH),
        )
        async with ServerAsync(horizon_mock.url, client) as server:
            resp = await server.submit_transaction_async(hf.TRANSACTION_XDR, True)
            assert resp["hash"] == hf.TRANSACTION_HASH
            assert resp["tx_status"] == "PENDING"

    async def test_submit_transaction_async_with_te(self, horizon_mock):
        client = AiohttpClient()
        te = TransactionEnvelope.from_xdr(
            hf.TRANSACTION_XDR, Network.PUBLIC_NETWORK_PASSPHRASE
        )
        assert te.hash_hex() == hf.TRANSACTION_HASH
        horizon_mock.expect(
            "/transactions_async",
            method="POST",
            json=hf.submit_transaction_async(hf.TRANSACTION_HASH),
        )
        async with ServerAsync(horizon_mock.url, client) as server:
            resp = await server.submit_transaction_async(te, True)
            assert resp["hash"] == hf.TRANSACTION_HASH
            assert resp["tx_status"] == "PENDING"
