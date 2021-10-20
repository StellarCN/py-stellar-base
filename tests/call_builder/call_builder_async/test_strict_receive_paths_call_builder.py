from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import StrictReceivePathsCallBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestStrictReceivePathsCallBuilder:
    def test_init_source_account(self):
        builder = StrictReceivePathsCallBuilder(
            horizon_url,
            client,
            source="GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP",
            destination_asset=Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            ),
            destination_amount="20.0",
        )
        assert builder.endpoint == "paths/strict-receive"
        assert builder.params == {
            "destination_amount": "20.0",
            "destination_asset_type": "credit_alphanum4",
            "destination_asset_code": "EUR",
            "destination_asset_issuer": "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN",
            "source_account": "GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP",
        }

    def test_init_source_assets(self):
        builder = StrictReceivePathsCallBuilder(
            horizon_url,
            client,
            source=[
                Asset.native(),
                Asset(
                    "USD", "GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
            ],
            destination_asset=Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            ),
            destination_amount="20.0",
        )
        assert builder.endpoint == "paths/strict-receive"
        assert builder.params == {
            "destination_amount": "20.0",
            "destination_asset_type": "credit_alphanum4",
            "destination_asset_code": "EUR",
            "destination_asset_issuer": "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN",
            "source_assets": "native,USD:GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH,XCN:GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY",
        }
