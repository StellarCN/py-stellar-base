import pytest

from stellar_sdk import Asset
from stellar_sdk.exceptions import ParseResponseError
from stellar_sdk.server import Server
from . import parse_time


class TestParseResponse:
    server = Server("https://horizon.stellar.org")
    account = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"

    def test_account(self):
        resp = self.server.accounts().account_id(self.account).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_accounts(self):
        asset = Asset("XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
        resp = self.server.accounts().for_asset(asset).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_assets(self):
        resp = self.server.assets().call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_data(self):
        resp = self.server.data(account_id=self.account, data_name="Stellar SDK").call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_effects(self):
        resp = self.server.effects().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["created_at"] = parse_time(
                raw_resp["_embedded"]["records"][i]["created_at"]
            )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_fee_stats(self):
        resp = self.server.fee_stats().call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        raw_resp["last_ledger"] = int(parsed_resp.last_ledger)
        raw_resp["last_ledger_base_fee"] = int(parsed_resp.last_ledger_base_fee)
        raw_resp["ledger_capacity_usage"] = float(parsed_resp.ledger_capacity_usage)
        for k, v in raw_resp["fee_charged"].items():
            raw_resp["fee_charged"][k] = int(v)
        for k, v in raw_resp["max_fee"].items():
            raw_resp["max_fee"][k] = int(v)
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_ledger(self):
        resp = self.server.ledgers().ledger(28566227).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        raw_resp["closed_at"] = parse_time(raw_resp["closed_at"])
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_ledgers(self):
        resp = self.server.ledgers().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["closed_at"] = parse_time(
                raw_resp["_embedded"]["records"][i]["closed_at"]
            )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_offers(self):
        resp = self.server.offers().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["last_modified_time"] = parse_time(
                raw_resp["_embedded"]["records"][i]["last_modified_time"]
            )
            raw_resp["_embedded"]["records"][i]["id"] = int(
                raw_resp["_embedded"]["records"][i]["id"]
            )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_operation(self):
        resp = self.server.operations().operation(122691075160104961).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        raw_resp["created_at"] = parse_time(raw_resp["created_at"])
        if raw_resp.__contains__("bump_to"):
            raw_resp["bump_to"] = int(raw_resp["bump_to"])
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_operations(self):
        resp = self.server.operations().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["created_at"] = parse_time(
                raw_resp["_embedded"]["records"][i]["created_at"]
            )
            if raw_resp["_embedded"]["records"][i].__contains__("bump_to"):
                raw_resp["_embedded"]["records"][i]["bump_to"] = int(
                    raw_resp["_embedded"]["records"][i]["bump_to"]
                )
            if raw_resp["_embedded"]["records"][i].__contains__("offer_id"):
                raw_resp["_embedded"]["records"][i]["offer_id"] = int(
                    raw_resp["_embedded"]["records"][i]["offer_id"]
                )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_orderbook(self):
        selling = Asset(
            "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        )
        buying = Asset.native()
        resp = self.server.orderbook(selling, buying).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_payments(self):
        resp = self.server.payments().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["created_at"] = parse_time(
                raw_resp["_embedded"]["records"][i]["created_at"]
            )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_root(self):
        resp = self.server.root().call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_strict_receive_paths(self):
        resp = self.server.strict_receive_paths(
            self.account,
            Asset("XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"),
            "0.1",
        ).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_strict_send_paths(self):
        resp = self.server.strict_send_paths(
            Asset("XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"),
            "0.1",
            self.account,
        ).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def trades_aggregation(self):
        resp = (
            self.server.trade_aggregations(
                base=Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                counter=Asset.native(),
                resolution=300000,
            )
            .order(desc=True)
            .call()
        )
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_trades(self):
        resp = self.server.trades().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["ledger_close_time"] = parse_time(
                raw_resp["_embedded"]["records"][i]["ledger_close_time"]
            )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_transaction(self):
        resp = (
            self.server.transactions()
            .transaction(
                "b154e45e592a546226f6c58a4d28e03bb37266b7fa6bd3f6fab1d3bf69f088dd"
            )
            .call()
        )
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        raw_resp["created_at"] = parse_time(raw_resp["created_at"])
        raw_resp["valid_before"] = parse_time(raw_resp["valid_before"])
        raw_resp["valid_after"] = parse_time(raw_resp["valid_after"])
        raw_resp["source_account_sequence"] = int(raw_resp["source_account_sequence"])
        assert raw_resp == parsed_resp.dict(exclude_unset=True, by_alias=True)

    def test_transactions(self):
        resp = self.server.transactions().order(desc=True).call()
        raw_resp = resp.raw_data
        parsed_resp = resp.parse()
        for i in range(len(parsed_resp)):
            raw_resp["_embedded"]["records"][i]["created_at"] = parse_time(
                raw_resp["_embedded"]["records"][i]["created_at"]
            )
            raw_resp["_embedded"]["records"][i]["source_account_sequence"] = int(
                raw_resp["_embedded"]["records"][i]["source_account_sequence"]
            )
            if raw_resp["_embedded"]["records"][i].__contains__("valid_before"):
                raw_resp["_embedded"]["records"][i]["valid_before"] = parse_time(
                    raw_resp["_embedded"]["records"][i]["valid_before"]
                )
            if raw_resp["_embedded"]["records"][i].__contains__("valid_after"):
                raw_resp["_embedded"]["records"][i]["valid_after"] = parse_time(
                    raw_resp["_embedded"]["records"][i]["valid_after"]
                )
            assert raw_resp["_embedded"]["records"][i] == parsed_resp[i].dict(
                exclude_unset=True, by_alias=True
            )

    def test_parse_failed_raise(self):
        resp = self.server.root().call()
        resp.raw_data["current_protocol_version"] = "raise"
        with pytest.raises(
            ParseResponseError,
            match="Parsing the response failed. This may be due to a change in the Horizon field.",
        ):
            parsed_resp = resp.parse()
