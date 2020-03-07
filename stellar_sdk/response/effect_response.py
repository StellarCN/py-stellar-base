from datetime import datetime
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
    created_at: datetime
    links: Links = Field(None, alias="_links")


class AccountCreatedResponse(BaseEffectResponse):
    starting_balance: str


class AccountRemovedResponse(BaseEffectResponse):
    pass


class AccountCreditedResponse(BaseEffectResponse):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    amount: str


class AccountDebitedResponse(BaseEffectResponse):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    amount: str


class AccountThresholdsUpdatedResponse(BaseEffectResponse):
    low_threshold: int
    med_threshold: int
    high_threshold: int


class AccountHomeDomainUpdatedResponse(BaseEffectResponse):
    home_domain: str


class AccountFlagsUpdatedResponse(BaseEffectResponse):
    auth_required_flag: Optional[bool]
    auth_revokable_flag: Optional[bool]


class AccountInflationDestinationUpdatedResponse(BaseEffectResponse):
    pass


class SequenceBumpedResponse(BaseEffectResponse):
    new_seq: int


class SignerCreatedResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


class SignerRemovedResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


class SignerUpdatedResponse(BaseEffectResponse):
    weight: int
    public_key: str
    key: str


# TODO: In my opinion asset_code should not be optional in trustline,
# but it is optional in the source code of Horizon.
class TrustlineCreatedResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineRemovedResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineUpdatedResponse(BaseEffectResponse):
    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str


class TrustlineAuthorizedResponse(BaseEffectResponse):
    trustor: str
    asset_type: str
    asset_code: str


class TrustlineDeauthorizedResponse(BaseEffectResponse):
    trustor: str
    asset_type: str
    asset_code: str


class TradeResponse(BaseEffectResponse):
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


class OfferCreatedResponse(BaseEffectResponse):
    pass


class OfferRemovedResponse(BaseEffectResponse):
    pass


class OfferUpdatedResponse(BaseEffectResponse):
    pass


class DataCreatedResponse(BaseEffectResponse):
    pass


class DataRemovedResponse(BaseEffectResponse):
    pass


class DataUpdatedResponse(BaseEffectResponse):
    pass


EFFECT_TYPE_I_RESPONSE = {
    0: AccountCreatedResponse,
    1: AccountRemovedResponse,
    2: AccountCreditedResponse,
    3: AccountDebitedResponse,
    4: AccountThresholdsUpdatedResponse,
    5: AccountHomeDomainUpdatedResponse,
    6: AccountFlagsUpdatedResponse,
    7: AccountInflationDestinationUpdatedResponse,
    10: SignerCreatedResponse,
    11: SignerRemovedResponse,
    12: SignerUpdatedResponse,
    20: TrustlineCreatedResponse,
    21: TrustlineRemovedResponse,
    22: TrustlineUpdatedResponse,
    23: TrustlineAuthorizedResponse,
    24: TrustlineDeauthorizedResponse,
    30: OfferCreatedResponse,
    31: OfferRemovedResponse,
    32: OfferUpdatedResponse,
    33: TradeResponse,
    40: DataCreatedResponse,
    41: DataRemovedResponse,
    42: DataRemovedResponse,
    43: SequenceBumpedResponse,
}

EFFECT_RESPONSE_TYPE_UNION = Union[
    AccountCreatedResponse,
    AccountRemovedResponse,
    AccountCreditedResponse,
    AccountDebitedResponse,
    AccountThresholdsUpdatedResponse,
    AccountHomeDomainUpdatedResponse,
    AccountFlagsUpdatedResponse,
    AccountInflationDestinationUpdatedResponse,
    SignerCreatedResponse,
    SignerRemovedResponse,
    SignerUpdatedResponse,
    TrustlineCreatedResponse,
    TrustlineRemovedResponse,
    TrustlineUpdatedResponse,
    TrustlineAuthorizedResponse,
    TrustlineDeauthorizedResponse,
    OfferCreatedResponse,
    OfferRemovedResponse,
    OfferUpdatedResponse,
    TradeResponse,
    DataCreatedResponse,
    DataRemovedResponse,
    DataRemovedResponse,
    SequenceBumpedResponse,
]

EFFECT_RESPONSE_TYPE_UNION_TYPE = Union[
    Type[AccountCreatedResponse],
    Type[AccountRemovedResponse],
    Type[AccountCreditedResponse],
    Type[AccountDebitedResponse],
    Type[AccountThresholdsUpdatedResponse],
    Type[AccountHomeDomainUpdatedResponse],
    Type[AccountFlagsUpdatedResponse],
    Type[AccountInflationDestinationUpdatedResponse],
    Type[SignerCreatedResponse],
    Type[SignerRemovedResponse],
    Type[SignerUpdatedResponse],
    Type[TrustlineCreatedResponse],
    Type[TrustlineRemovedResponse],
    Type[TrustlineUpdatedResponse],
    Type[TrustlineAuthorizedResponse],
    Type[TrustlineDeauthorizedResponse],
    Type[OfferCreatedResponse],
    Type[OfferRemovedResponse],
    Type[OfferUpdatedResponse],
    Type[TradeResponse],
    Type[DataCreatedResponse],
    Type[DataRemovedResponse],
    Type[DataRemovedResponse],
    Type[SequenceBumpedResponse],
]
