from decimal import Decimal

import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    StrictReceivePathsCallBuilder as StrictReceivePathsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import StrictReceivePathsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (StrictReceivePathsCallBuilder, SYNC_CLIENT),
        "async": (StrictReceivePathsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestStrictReceivePathsCallBuilder:
    def test_init_source_account(self, builder_factory):
        builder = builder_factory(
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

    def test_init_source_assets(self, builder_factory):
        builder = builder_factory(
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
            destination_amount=Decimal("20.0"),
        )
        assert builder.endpoint == "paths/strict-receive"
        assert builder.params == {
            "destination_amount": "20.0",
            "destination_asset_type": "credit_alphanum4",
            "destination_asset_code": "EUR",
            "destination_asset_issuer": "GDSBCQO34HWPGUGQSP3QBFEXVTSR2PW46UIGTHVWGWJGQKH3AFNHXHXN",
            "source_assets": "native,USD:GAYSHLG75RPSMXWJ5KX7O7STE6RSZTD6NE4CTWAXFZYYVYIFRUVJIBJH,XCN:GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY",
        }

    @pytest.mark.parametrize(
        ("amount", "expected"),
        [
            (Decimal("0.0000001"), "0.0000001"),
            (Decimal("100").normalize(), "100"),
            (Decimal("12.50"), "12.50"),
        ],
    )
    def test_decimal_amount_without_exponent(self, builder_factory, amount, expected):
        # Horizon accepts only plain decimal numbers, while str() writes 1E-7 and 1E+2.
        builder = builder_factory(
            source="GARSFJNXJIHO6ULUBK3DBYKVSIZE7SC72S5DYBCHU7DKL22UXKVD7MXP",
            destination_asset=Asset.native(),
            destination_amount=amount,
        )
        assert builder.params["destination_amount"] == expected
