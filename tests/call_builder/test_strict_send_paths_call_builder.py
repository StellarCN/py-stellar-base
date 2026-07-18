from decimal import Decimal

import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    StrictSendPathsCallBuilder as StrictSendPathsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import StrictSendPathsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (StrictSendPathsCallBuilder, SYNC_CLIENT),
        "async": (StrictSendPathsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestStrictSendPathsCallBuilder:
    def test_init_destination_account(self, builder_factory):
        builder = builder_factory(
            source_asset=Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            ),
            source_amount="10.25",
            destination="GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP",
        )
        assert builder.endpoint == "paths/strict-send"
        assert builder.params == {
            "source_amount": "10.25",
            "source_asset_type": "credit_alphanum4",
            "source_asset_code": "EUR",
            "source_asset_issuer": "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN",
            "destination_account": "GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP",
        }

    def test_destination_source_assets(self, builder_factory):
        builder = builder_factory(
            source_asset=Asset(
                "EUR", "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN"
            ),
            source_amount=Decimal("10.25"),
            destination=[
                Asset(
                    "USD", "GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH"
                ),
                Asset.native(),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
            ],
        )
        assert builder.endpoint == "paths/strict-send"
        assert builder.params == {
            "source_amount": "10.25",
            "source_asset_type": "credit_alphanum4",
            "source_asset_code": "EUR",
            "source_asset_issuer": "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN",
            "destination_assets": "USD:GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH,native,XCN:GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY",
        }
