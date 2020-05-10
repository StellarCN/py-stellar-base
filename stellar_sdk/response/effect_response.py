from typing import Optional, Union, Type

from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    operation: Link
    succeeds: Link
    precedes: Link


class BaseEffectResponse(BaseModel):
    id: str
    paging_token: str
    account: str
    type: str
    type_i: int
    # The maximum year in Python is 9999
    # https://horizon.stellar.org/transactions/8761d590f853174b42c7d8e5e1a274a6dfd786091d1776eaf61965920346e9b8
    created_at: str
    links: Links = Field(None, alias="_links")


class AccountCreatedEffectResponse(BaseEffectResponse):
    starting_balance: str


class AccountRemovedEffectResponse(BaseEffectResponse):
    pass


class AccountCreditedEffectResponse(BaseEffectResponse):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    amount: str


class AccountDebitedEffectResponse(BaseEffectResponse):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    amount: str


class AccountThresholdsUpdatedEffectResponse(BaseEffectResponse):
    low_threshold: int
    med_threshold: int
    high_threshold: int


class AccountHomeDomainUpdatedEffectResponse(BaseEffectResponse):
    home_domain: str


class AccountFlagsUpdatedEffectResponse(BaseEffectResponse):
    auth_required_flag: Optional[bool]
    auth_revokable_flag: Optional[bool]


class AccountInflationDestinationUpdatedEffectResponse(BaseEffectResponse):
    pass


class SequenceBumpedEffectResponse(BaseEffectResponse):
    new_seq: int


class SignerCreatedEffectResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


class SignerRemovedEffectResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


class SignerUpdatedEffectResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


# TODO: In my opinion asset_code should not be optional in trustline,
# but it is optional in the source code of Horizon.
class TrustlineCreatedEffectResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineRemovedEffectResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineUpdatedEffectResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineAuthorizedEffectResponse(BaseEffectResponse):
    trustor: str
    asset_type: str
    asset_code: str


class TrustlineDeauthorizedEffectResponse(BaseEffectResponse):
    trustor: str
    asset_type: str
    asset_code: str


class TrustlineAuthorizedToMaintainLiabilitiesEffectResponse(BaseEffectResponse):
    trustor: str
    asset_type: str
    asset_code: str


class TradeEffectResponse(BaseEffectResponse):
    seller: str
    sold_amount: str
    sold_asset_type: str
    sold_asset_code: Optional[str]
    sold_asset_issuer: Optional[str]
    bought_amount: str
    bought_asset_type: str
    bought_asset_code: Optional[str]
    bought_asset_issuer: Optional[str]
    offer_id: int  # str in Go impl


class OfferCreatedEffectResponse(BaseEffectResponse):
    pass


class OfferRemovedEffectResponse(BaseEffectResponse):
    pass


class OfferUpdatedEffectResponse(BaseEffectResponse):
    pass


class DataCreatedEffectResponse(BaseEffectResponse):
    pass


class DataRemovedEffectResponse(BaseEffectResponse):
    pass


class DataUpdatedEffectResponse(BaseEffectResponse):
    pass


EFFECT_TYPE_I_RESPONSE = {
    0: AccountCreatedEffectResponse,
    1: AccountRemovedEffectResponse,
    2: AccountCreditedEffectResponse,
    3: AccountDebitedEffectResponse,
    4: AccountThresholdsUpdatedEffectResponse,
    5: AccountHomeDomainUpdatedEffectResponse,
    6: AccountFlagsUpdatedEffectResponse,
    7: AccountInflationDestinationUpdatedEffectResponse,
    10: SignerCreatedEffectResponse,
    11: SignerRemovedEffectResponse,
    12: SignerUpdatedEffectResponse,
    20: TrustlineCreatedEffectResponse,
    21: TrustlineRemovedEffectResponse,
    22: TrustlineUpdatedEffectResponse,
    23: TrustlineAuthorizedEffectResponse,
    24: TrustlineDeauthorizedEffectResponse,
    25: TrustlineAuthorizedToMaintainLiabilitiesEffectResponse,
    30: OfferCreatedEffectResponse,
    31: OfferRemovedEffectResponse,
    32: OfferUpdatedEffectResponse,
    33: TradeEffectResponse,
    40: DataCreatedEffectResponse,
    41: DataRemovedEffectResponse,
    42: DataRemovedEffectResponse,
    43: SequenceBumpedEffectResponse,
}

EFFECT_RESPONSE_TYPE_UNION = Union[
    AccountCreatedEffectResponse,
    AccountRemovedEffectResponse,
    AccountCreditedEffectResponse,
    AccountDebitedEffectResponse,
    AccountThresholdsUpdatedEffectResponse,
    AccountHomeDomainUpdatedEffectResponse,
    AccountFlagsUpdatedEffectResponse,
    AccountInflationDestinationUpdatedEffectResponse,
    SignerCreatedEffectResponse,
    SignerRemovedEffectResponse,
    SignerUpdatedEffectResponse,
    TrustlineCreatedEffectResponse,
    TrustlineRemovedEffectResponse,
    TrustlineUpdatedEffectResponse,
    TrustlineAuthorizedEffectResponse,
    TrustlineDeauthorizedEffectResponse,
    OfferCreatedEffectResponse,
    OfferRemovedEffectResponse,
    OfferUpdatedEffectResponse,
    TradeEffectResponse,
    DataCreatedEffectResponse,
    DataRemovedEffectResponse,
    DataRemovedEffectResponse,
    SequenceBumpedEffectResponse,
]

EFFECT_RESPONSE_TYPE_UNION_TYPE = Union[
    Type[AccountCreatedEffectResponse],
    Type[AccountRemovedEffectResponse],
    Type[AccountCreditedEffectResponse],
    Type[AccountDebitedEffectResponse],
    Type[AccountThresholdsUpdatedEffectResponse],
    Type[AccountHomeDomainUpdatedEffectResponse],
    Type[AccountFlagsUpdatedEffectResponse],
    Type[AccountInflationDestinationUpdatedEffectResponse],
    Type[SignerCreatedEffectResponse],
    Type[SignerRemovedEffectResponse],
    Type[SignerUpdatedEffectResponse],
    Type[TrustlineCreatedEffectResponse],
    Type[TrustlineRemovedEffectResponse],
    Type[TrustlineUpdatedEffectResponse],
    Type[TrustlineAuthorizedEffectResponse],
    Type[TrustlineDeauthorizedEffectResponse],
    Type[OfferCreatedEffectResponse],
    Type[OfferRemovedEffectResponse],
    Type[OfferUpdatedEffectResponse],
    Type[TradeEffectResponse],
    Type[DataCreatedEffectResponse],
    Type[DataRemovedEffectResponse],
    Type[DataRemovedEffectResponse],
    Type[SequenceBumpedEffectResponse],
]

# TODO: Protocol 13 / add trustline_authorized_to_maintain_liabilities
