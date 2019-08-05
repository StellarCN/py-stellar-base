from stellar_sdk.call_builder.offers_call_builder import OffersCallBuilder
from tests.call_builder import horizon_url, client


class TestOffersCallBuilder:
    def test_init(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = OffersCallBuilder(horizon_url, client, account_id)
        assert builder.endpoint == "accounts/{account_id}/offers".format(
            account_id=account_id
        )
        assert builder.params == {}
