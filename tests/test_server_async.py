from decimal import Decimal

import pytest
from aioresponses import aioresponses

from stellar_sdk import (
    AiohttpClient,
    Asset,
    MuxedAccount,
    Network,
    ServerAsync,
    TransactionEnvelope,
)
from stellar_sdk.account import Thresholds
from stellar_sdk.call_builder.call_builder_async import *


@pytest.mark.slow
@pytest.mark.asyncio
class TestServerAsync:
    async def test_load_acount(self):
        account_id = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == MuxedAccount.from_account(account_id)
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_load_acount_muxed_account_str(self):
        account_id = (
            "MDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQAAAAAAAAAAE2KS7Y"
        )
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == MuxedAccount.from_account(account_id)
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_load_acount_muxed_account(self):
        account_id = MuxedAccount(
            "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D", 1234
        )
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            account = await server.load_account(account_id)
            assert account.account == account_id
            assert isinstance(account.sequence, int)
            assert account.thresholds == Thresholds(1, 2, 3)

    async def test_fetch_base_fee(self):
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            base_fee = await server.fetch_base_fee()
            assert isinstance(base_fee, int)

    async def test_endpoint(self):
        horizon_url = "https://horizon.stellar.org"
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

    async def test_submit_transaction_with_xdr(self):
        xdr = "AAAAAgAAAACpYAfsZFw9X5E2fHFl+xYB3D9dxwhtVPZ6c8QW/7KNxAAAAGQDBJRXAAYt2AAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAwAAAAAAAAABVVNEQwAAAAA7mRE4Dv6Yi6CokA6xz+RPNm99vpRr7QdyQPf2JN8VxQAAAAAATEShAA9I5QCYloAAAAAAX5K4WgAAAAAAAAAB/7KNxAAAAEChPdaEabaexQ6vjiJxI0ECXuK97fidU4a8l0/iK6ORCAQ+NGeBAIfaLAZiyww+I/nWEqrihn8zdN+wNdUUoDgF"
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            resp = await server.submit_transaction(xdr, True)
            assert resp["envelope_xdr"] == xdr

    async def test_submit_transaction_with_te(self):
        xdr = "AAAAAgAAAACpYAfsZFw9X5E2fHFl+xYB3D9dxwhtVPZ6c8QW/7KNxAAAAGQDBJRXAAYt2AAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAwAAAAAAAAABVVNEQwAAAAA7mRE4Dv6Yi6CokA6xz+RPNm99vpRr7QdyQPf2JN8VxQAAAAAATEShAA9I5QCYloAAAAAAX5K4WgAAAAAAAAAB/7KNxAAAAEChPdaEabaexQ6vjiJxI0ECXuK97fidU4a8l0/iK6ORCAQ+NGeBAIfaLAZiyww+I/nWEqrihn8zdN+wNdUUoDgF"
        te = TransactionEnvelope.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        async with ServerAsync(horizon_url, client) as server:
            resp = await server.submit_transaction(te, True)
            assert resp["envelope_xdr"] == xdr

    async def test_submit_transaction_async_with_xdr(self):
        xdr = "AAAAAHI7fpgo+b7tgpiFyYWimjV7L7IOYLwmQS7k7F8SronXAAAAZAE+QT4AAAAJAAAAAQAAAAAAAAAAAAAAAF1MG8cAAAAAAAAAAQAAAAAAAAAAAAAAAOvi1O/HEn+QgZJw+EMZBtwvTVNmpgvE9p8IRfwp0GY4AAAAAAExLQAAAAAAAAAAARKuidcAAABAJVc1ASGp35hUquGNbzzSqWPoTG0zgc89zc4p+19QkgbPqsdyEfHs7+ng9VJA49YneEXRa6Fv7pfKpEigb3VTCg=="
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        te = TransactionEnvelope.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert (
            te.hash_hex()
            == "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084"
        )
        data = {
            "tx_status": "PENDING",
            "hash": "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084",
        }

        with aioresponses() as m:
            m.post(f"{horizon_url}/transactions_async", payload=data)
            async with ServerAsync(horizon_url, client) as server:
                resp = await server.submit_transaction_async(xdr, True)
                assert (
                    resp["hash"]
                    == "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084"
                )
                assert resp["tx_status"] == "PENDING"

    async def test_submit_transaction_async_with_te(self):
        xdr = "AAAAAHI7fpgo+b7tgpiFyYWimjV7L7IOYLwmQS7k7F8SronXAAAAZAE+QT4AAAAJAAAAAQAAAAAAAAAAAAAAAF1MG8cAAAAAAAAAAQAAAAAAAAAAAAAAAOvi1O/HEn+QgZJw+EMZBtwvTVNmpgvE9p8IRfwp0GY4AAAAAAExLQAAAAAAAAAAARKuidcAAABAJVc1ASGp35hUquGNbzzSqWPoTG0zgc89zc4p+19QkgbPqsdyEfHs7+ng9VJA49YneEXRa6Fv7pfKpEigb3VTCg=="
        horizon_url = "https://horizon.stellar.org"
        client = AiohttpClient()
        te = TransactionEnvelope.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert (
            te.hash_hex()
            == "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084"
        )
        data = {
            "tx_status": "PENDING",
            "hash": "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084",
        }

        with aioresponses() as m:
            m.post(f"{horizon_url}/transactions_async", payload=data)
            async with ServerAsync(horizon_url, client) as server:
                resp = await server.submit_transaction_async(te, True)
                assert (
                    resp["hash"]
                    == "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084"
                )
                assert resp["tx_status"] == "PENDING"
