from stellar_sdk.response.effect_response import *
from . import load_file


class TestEffectModel:
    def test_account_created(self):
        raw = load_file("effects/account_created.json")
        parsed = AccountCreatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_credited(self):
        raw = load_file("effects/account_credited.json")
        parsed = AccountCreditedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_debited(self):
        raw = load_file("effects/account_debited.json")
        parsed = AccountDebitedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_flags_updated(self):
        raw = load_file("effects/account_flags_updated.json")
        parsed = AccountFlagsUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_home_domain_updated(self):
        raw = load_file("effects/account_home_domain_updated.json")
        parsed = AccountHomeDomainUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_inflation_destination_updated(self):
        raw = load_file("effects/account_inflation_destination_updated.json")
        parsed = AccountInflationDestinationUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_removed(self):
        raw = load_file("effects/account_removed.json")
        parsed = AccountRemovedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_account_thresholds_updated(self):
        raw = load_file("effects/account_thresholds_updated.json")
        parsed = AccountThresholdsUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_created(self):
        raw = load_file("effects/data_created.json")
        parsed = DataCreatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_removed(self):
        raw = load_file("effects/data_removed.json")
        parsed = DataRemovedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_data_updated(self):
        raw = load_file("effects/data_updated.json")
        parsed = DataUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_sequence_bumped(self):
        raw = load_file("effects/sequence_bumped.json")
        parsed = SequenceBumpedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_created(self):
        raw = load_file("effects/signer_created.json")
        parsed = SignerCreatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_removed(self):
        raw = load_file("effects/signer_removed.json")
        parsed = SignerRemovedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_signer_updated(self):
        raw = load_file("effects/signer_updated.json")
        parsed = SignerUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trade(self):
        raw = load_file("effects/trade.json")
        parsed = TradeEffectResponse.parse_obj(raw)
        raw["offer_id"] = int(raw["offer_id"])
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_authorized(self):
        raw = load_file("effects/trustline_authorized.json")
        parsed = TrustlineAuthorizedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_created(self):
        raw = load_file("effects/trustline_created.json")
        parsed = TrustlineCreatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_deauthorized(self):
        raw = load_file("effects/trustline_deauthorized.json")
        parsed = TrustlineDeauthorizedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_authorized_to_maintain_liabilities(self):
        raw = load_file("effects/trustline_authorized_to_maintain_liabilities.json")
        parsed = TrustlineAuthorizedToMaintainLiabilitiesEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_removed(self):
        raw = load_file("effects/trustline_removed.json")
        parsed = TrustlineRemovedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_trustline_updated(self):
        raw = load_file("effects/trustline_updated.json")
        parsed = TrustlineUpdatedEffectResponse.parse_obj(raw)
        assert raw == parsed.dict(exclude_unset=True, by_alias=True)

    def test_offer_created(self):
        pass

    def test_offer_removed(self):
        pass

    def test_offer_updated(self):
        pass
