from stellar_sdk.response.operation_response import *
from . import load_file, parse_time


class TestOperationModel:
    def test_account_merge(self):
        raw = load_file("operations/account_merge.json")
        parsed = AccountMergeResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_allow_trust(self):
        raw = load_file("operations/allow_trust.json")
        parsed = AllowTrustResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_bump_sequence(self):
        raw = load_file("operations/bump_sequence.json")
        parsed = BumpSequenceResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        raw["bump_to"] = int(raw["bump_to"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_change_trust(self):
        raw = load_file("operations/change_trust.json")
        parsed = ChangeTrustResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_create_passive_offer(self):
        raw = load_file("operations/create_passive_offer.json")
        parsed = CreatePassiveSellOfferResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_inflation(self):
        raw = load_file("operations/inflation.json")
        parsed = InflationResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_buy_offer(self):
        raw = load_file("operations/manage_buy_offer.json")
        parsed = ManageBuyOfferResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_data(self):
        raw = load_file("operations/manage_data.json")
        parsed = ManageDataResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_manage_offer(self):
        raw = load_file("operations/manage_offer.json")
        parsed = ManageSellOfferResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_path_payment(self):
        raw = load_file("operations/path_payment.json")
        parsed = PathPaymentStrictReceiveResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_path_payment_strict_send(self):
        raw = load_file("operations/path_payment_strict_send.json")
        parsed = PathPaymentStrictSendResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_payment(self):
        raw = load_file("operations/payment.json")
        parsed = PaymentResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_set_options(self):
        raw = load_file("operations/set_options.json")
        parsed = SetOptionsResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)
