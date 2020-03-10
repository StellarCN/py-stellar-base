from stellar_sdk.response.operation_response import *
from . import load_file, parse_time


class TestOperationModel:
    def test_account_merge(self):
        raw = load_file("operations/account_merge.json")
        parsed = AccountMergeOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_allow_trust(self):
        raw = load_file("operations/allow_trust.json")
        parsed = AllowTrustOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_bump_sequence(self):
        raw = load_file("operations/bump_sequence.json")
        parsed = BumpSequenceOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        raw["bump_to"] = int(raw["bump_to"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_change_trust(self):
        raw = load_file("operations/change_trust.json")
        parsed = ChangeTrustOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_create_passive_offer(self):
        raw = load_file("operations/create_passive_offer.json")
        parsed = CreatePassiveSellOfferOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_inflation(self):
        raw = load_file("operations/inflation.json")
        parsed = InflationOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_buy_offer(self):
        raw = load_file("operations/manage_buy_offer.json")
        parsed = ManageBuyOfferOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        raw["offer_id"] = int(raw["offer_id"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_data(self):
        raw = load_file("operations/manage_data.json")
        parsed = ManageDataOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_offer(self):
        raw = load_file("operations/manage_offer.json")
        parsed = ManageSellOfferOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        raw["offer_id"] = int(raw["offer_id"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_path_payment(self):
        raw = load_file("operations/path_payment.json")
        parsed = PathPaymentStrictReceiveOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_path_payment_strict_send(self):
        raw = load_file("operations/path_payment_strict_send.json")
        parsed = PathPaymentStrictSendOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_payment(self):
        raw = load_file("operations/payment.json")
        parsed = PaymentOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_set_options(self):
        raw = load_file("operations/set_options.json")
        parsed = SetOptionsOperationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)
