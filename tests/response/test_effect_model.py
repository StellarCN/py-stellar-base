from stellar_sdk.response.effect_response import *
from . import load_file, parse_time


class TestEffectModel:
    def test_account_created(self):
        raw = load_file("effects/account_created.json")
        parsed = AccountCreatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_credited(self):
        raw = load_file("effects/account_credited.json")
        parsed = AccountCreditedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_debited(self):
        raw = load_file("effects/account_debited.json")
        parsed = AccountDebitedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_flags_updated(self):
        raw = load_file("effects/account_flags_updated.json")
        parsed = AccountFlagsUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_home_domain_updated(self):
        raw = load_file("effects/account_home_domain_updated.json")
        parsed = AccountHomeDomainUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_inflation_destination_updated(self):
        raw = load_file("effects/account_inflation_destination_updated.json")
        parsed = AccountInflationDestinationUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_removed(self):
        raw = load_file("effects/account_removed.json")
        parsed = AccountRemovedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_thresholds_updated(self):
        raw = load_file("effects/account_thresholds_updated.json")
        parsed = AccountThresholdsUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_created(self):
        raw = load_file("effects/data_created.json")
        parsed = DataCreatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_removed(self):
        raw = load_file("effects/data_removed.json")
        parsed = DataRemovedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_updated(self):
        raw = load_file("effects/data_updated.json")
        parsed = DataUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_sequence_bumped(self):
        raw = load_file("effects/sequence_bumped.json")
        parsed = SequenceBumpedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_created(self):
        raw = load_file("effects/signer_created.json")
        parsed = SignerCreatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_removed(self):
        raw = load_file("effects/signer_removed.json")
        parsed = SignerRemovedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_updated(self):
        raw = load_file("effects/signer_updated.json")
        parsed = SignerUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trade(self):
        raw = load_file("effects/trade.json")
        parsed = TradeResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_authorized(self):
        raw = load_file("effects/trustline_authorized.json")
        parsed = TrustlineAuthorizedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_created(self):
        raw = load_file("effects/trustline_created.json")
        parsed = TrustlineCreatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_deauthorized(self):
        raw = load_file("effects/trustline_deauthorized.json")
        parsed = TrustlineDeauthorizedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_removed(self):
        raw = load_file("effects/trustline_removed.json")
        parsed = TrustlineRemovedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_updated(self):
        raw = load_file("effects/trustline_updated.json")
        parsed = TrustlineUpdatedResponse.parse_obj(raw)
        raw["created_at"] = parse_time(raw["created_at"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_offer_created(self):
        pass

    def test_offer_removed(self):
        pass

    def test_offer_updated(self):
        pass
