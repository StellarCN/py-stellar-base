from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import OffersCallBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestOffersCallBuilder:
    def test_init(self):
        builder = OffersCallBuilder(horizon_url, client)
        assert builder.endpoint == "offers"
        assert builder.params == {}

    def test_for_offer(self):
        offer_id = "1000"
        builder = OffersCallBuilder(horizon_url, client)
        builder.offer(offer_id)
        assert builder.endpoint == "offers/{offer_id}".format(offer_id=offer_id)
        assert builder.params == {}

    def test_for_asset(self):
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = OffersCallBuilder(horizon_url, client)
        builder.for_selling(selling)
        builder.for_buying(buying)
        assert builder.endpoint == "offers"
        assert builder.params == {
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }

    def test_for_seller(self):
        seller = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = OffersCallBuilder(horizon_url, client)
        builder.for_seller(seller)
        builder.for_selling(selling)
        builder.for_buying(buying)
        assert builder.endpoint == "offers"
        assert builder.params == {
            "seller": seller,
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }

    def test_for_sponsor(self):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = OffersCallBuilder(horizon_url, client).for_sponsor(sponsor)
        assert builder.endpoint == "offers"
        assert builder.params == {"sponsor": sponsor}
