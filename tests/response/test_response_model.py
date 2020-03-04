from stellar_sdk.response.account_response import AccountResponse
from stellar_sdk.response.data_response import DataResponse
from stellar_sdk.response.asset_response import AssetResponse
from stellar_sdk.response.fee_stats_response import FeeStatsResponse
from stellar_sdk.response.ledger_response import LedgerResponse
from stellar_sdk.response.offer_response import OfferResponse
from stellar_sdk.response.orderbook_response import OrderbookResponse
from stellar_sdk.response.payment_path_response import PaymentPathResponse
from stellar_sdk.response.root_response import RootResponse
from stellar_sdk.response.trade_response import TradeResponse
from stellar_sdk.response.trades_aggregation_response import TradesAggregationResponse
from stellar_sdk.response.transaction_response import TransactionResponse
from stellar_sdk.response.submit_response import TransactionSuccessResponse

from . import load_file, parse_time


class TestResponseModel:
    def test_account(self):
        raw = load_file("account.json")
        parsed = AccountResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_asset(self):
        raw = load_file("asset.json")
        parsed = AssetResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data(self):
        raw = load_file("data.json")
        parsed = DataResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_fee_stats(self):
        raw = load_file("fee_stats.json")
        parsed = FeeStatsResponse.parse_obj(raw)
        raw["last_ledger"] = int(parsed.last_ledger)
        raw["last_ledger_base_fee"] = int(parsed.last_ledger_base_fee)
        raw["ledger_capacity_usage"] = float(parsed.ledger_capacity_usage)
        for k, v in raw["fee_charged"].items():
            raw["fee_charged"][k] = int(v)
        for k, v in raw["max_fee"].items():
            raw["max_fee"][k] = int(v)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_ledger(self):
        raw = load_file("ledger.json")
        parsed = LedgerResponse.parse_obj(raw)
        raw["closed_at"] = parse_time(raw["closed_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_offer(self):
        raw = load_file("offer.json")
        parsed = OfferResponse.parse_obj(raw)
        raw["id"] = int(raw["id"])
        raw["last_modified_time"] = parse_time(raw["last_modified_time"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_orderbook(self):
        raw = load_file("orderbook.json")
        parsed = OrderbookResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_payment_path(self):
        raw = load_file("payment_path.json")
        parsed = PaymentPathResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_root(self):
        raw = load_file("root.json")
        parsed = RootResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trade(self):
        raw = load_file("trade.json")
        parsed = TradeResponse.parse_obj(raw)
        raw["ledger_close_time"] = parse_time(raw["ledger_close_time"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trades_aggregation(self):
        raw = load_file("trades_aggregation.json")
        parsed = TradesAggregationResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_transaction(self):
        raw = load_file("transaction.json")
        parsed = TransactionResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        raw["valid_before"] = parse_time(raw["valid_before"])
        raw["valid_after"] = parse_time(raw["valid_after"])
        raw["source_account_sequence"] = int(raw["source_account_sequence"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_submit_transaction_success(self):
        raw = load_file("transaction_success.json")
        parsed = TransactionSuccessResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)
