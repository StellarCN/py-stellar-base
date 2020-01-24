from stellar_sdk import Asset

from stellar_sdk.call_builder.offers_call_builder import OffersCallBuilder
from tests.call_builder import horizon_url, client


class TestOffersCallBuilder:
    def test_init(self):
        builder = OffersCallBuilder(horizon_url, client)
        assert builder.endpoint == "offers"
        assert builder.params == {}

    def test_for_account(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = OffersCallBuilder(horizon_url, client)
        builder.for_account(account_id)
        assert builder.endpoint == "accounts/{account_id}/offers".format(
            account_id=account_id
        )
        assert builder.params == {}

    def test_for_offer(self):
        offer_id = "1000"
        builder = OffersCallBuilder(horizon_url, client)
        builder.for_offer(offer_id)
        assert builder.endpoint == "offers/{offer_id}".format(offer_id=offer_id)
        assert builder.params == {}

    def test_for_asset(self):
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = OffersCallBuilder(horizon_url, client)
        builder.for_asset(selling, buying)
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
        builder.for_asset(selling, buying)
        assert builder.endpoint == "offers"
        assert builder.params == {
            "seller": seller,
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }
