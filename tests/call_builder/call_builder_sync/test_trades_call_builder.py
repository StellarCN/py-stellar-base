from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_sync import TradesCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestTradesCallBuilder:
    def test_init(self):
        builder = TradesCallBuilder(horizon_url, client)
        assert builder.endpoint == "trades"
        assert builder.params == {}

    def test_for_offer(self):
        offer_id = 1233453
        builder = TradesCallBuilder(horizon_url, client).for_offer(offer_id)
        assert builder.endpoint == "offers/{offer_id}/trades".format(offer_id=offer_id)
        assert builder.params == {}

    def test_for_account(self):
        account_id = "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z"
        builder = TradesCallBuilder(horizon_url, client).for_account(account_id)
        assert builder.endpoint == "accounts/{account_id}/trades".format(
            account_id=account_id
        )
        assert builder.params == {}

    def test_for_asset_pair(self):
        base = Asset("XCN", "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z")
        counter = Asset.native()
        builder = TradesCallBuilder(horizon_url, client).for_asset_pair(
            base=base, counter=counter
        )
        assert builder.endpoint == "trades"
        assert builder.params == {
            "base_asset_type": base.type,
            "base_asset_code": base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
        }

    def test_for_trade_type(self):
        trade_type = "liquidity_pools"
        builder = TradesCallBuilder(horizon_url, client).for_trade_type(trade_type)
        assert builder.endpoint == "trades"
        assert builder.params == {
            "trade_type": trade_type,
        }

    def test_for_liquidity_pool(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = TradesCallBuilder(horizon_url, client).for_liquidity_pool(
            liquidity_pool_id
        )
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}/trades"
        assert builder.params == {}
