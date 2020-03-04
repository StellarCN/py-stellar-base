from datetime import datetime
from typing import Optional, List, Union, Type

from pydantic import BaseModel, Field

from .common import Asset, Link, Price
from .transaction_response import TransactionResponse
from ..xdr.StellarXDR_const import (
    CREATE_ACCOUNT,
    PAYMENT,
    PATH_PAYMENT_STRICT_RECEIVE,
    MANAGE_SELL_OFFER,
    CREATE_PASSIVE_SELL_OFFER,
    SET_OPTIONS,
    CHANGE_TRUST,
    ALLOW_TRUST,
    ACCOUNT_MERGE,
    INFLATION,
    MANAGE_DATA,
    BUMP_SEQUENCE,
    MANAGE_BUY_OFFER,
    PATH_PAYMENT_STRICT_SEND,
)

__all__ = [
    "CreateAccountResponse",
    "PaymentResponse",
    "PathPaymentStrictReceiveResponse",
    "ManageSellOfferResponse",
    "CreatePassiveSellOfferResponse",
    "SetOptionsResponse",
    "ChangeTrustResponse",
    "AllowTrustResponse",
    "AccountMergeResponse",
    "InflationResponse",
    "ManageDataResponse",
    "BumpSequenceResponse",
    "ManageBuyOfferResponse",
    "PathPaymentStrictSendResponse",
]


class Links(BaseModel):
    self: Link
    transaction: Link
    effects: Link
    succeeds: Link
    precedes: Link


class BaseOperationResponse(BaseModel):
    id: str
    paging_token: str
    transaction_successful: bool
    source_account: str
    type: str
    type_i: int
    created_at: datetime
    transaction_hash: str
    transaction: Optional[TransactionResponse]
    links: Links = Field(None, alias="_links")


class BumpSequenceResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is BumpSequence.
    """

    bump_to: int  # str in Go impl


class CreateAccountResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is CreateAccount.
    """

    starting_balance: str
    funder: str
    account: str


class PaymentResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is Payment.
    """

    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    from_: str = Field(
        None,
        alias="from",
        description="This variable should be called `from`, "
        "but `from` is a keyword in Python, so we named it `from_`.",
    )
    to: str
    amount: str


class PathPaymentStrictReceiveResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is PathPaymentStrictReceive.
    """

    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    from_: str = Field(
        None,
        alias="from",
        description="This variable should be called `from`, "
        "but `from` is a keyword in Python, so we named it` from_`.",
    )
    to: str
    amount: str
    path: List[Asset]
    source_amount: str
    source_max: str
    source_asset_type: str
    source_asset_code: Optional[str]
    source_asset_issuer: Optional[str]


class PathPaymentStrictSendResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is PathPaymentStrictSend.
    """

    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    from_: str = Field(
        None,
        alias="from",
        description="This variable should be called `from`, "
        "but `from` is a keyword in Python, so we named it` from_`.",
    )
    to: str
    amount: str
    path: List[Asset]
    source_amount: str
    destination_min: str
    source_asset_type: str
    source_asset_code: Optional[str]
    source_asset_issuer: Optional[str]


class ManageDataResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is ManageData.
    """

    name: str
    value: str


class BaseOfferOperationResponse(BaseOperationResponse):
    amount: str
    price: str
    price_r: Price
    buying_asset_type: str
    buying_asset_code: Optional[str]
    buying_asset_issuer: Optional[str]
    selling_asset_type: str
    selling_asset_code: Optional[str]
    selling_asset_issuer: Optional[str]


class CreatePassiveSellOfferResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is CreatePassiveSellOffer.
    """


class ManageSellOfferResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is CreatePassiveSellOffer.
    """

    offer_id: int  # str in Go Impl


class ManageBuyOfferResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is ManageBuyOffer.
    """

    offer_id: int  # str in Go Impl


class SetOptionsResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is SetOptions.
    """

    home_domain: Optional[str]
    inflation_dest: Optional[str]
    master_key_weight: Optional[int]
    signer_key: Optional[str]
    signer_weight: Optional[int]
    set_flags: Optional[List[int]]
    set_flags_s: Optional[List[str]]
    clear_flags: Optional[List[int]]
    clear_flags_s: Optional[List[str]]
    low_threshold: Optional[int]
    med_threshold: Optional[int]
    high_threshold: Optional[int]


class ChangeTrustResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is ChangeTrust.
    """

    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str
    trustee: str
    trustor: str


class AllowTrustResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is AllowTrust.
    """

    asset_type: str
    asset_code: str
    asset_issuer: str
    trustee: str
    trustor: str
    authorize: bool


class AccountMergeResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is AccountMerge.
    """

    account: str
    into: str


class InflationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is Inflation.
    """


OPERATION_RESPONSE_TYPE_UNION = Union[
    CreateAccountResponse,
    PaymentResponse,
    PathPaymentStrictReceiveResponse,
    ManageSellOfferResponse,
    CreatePassiveSellOfferResponse,
    SetOptionsResponse,
    ChangeTrustResponse,
    AllowTrustResponse,
    AccountMergeResponse,
    InflationResponse,
    ManageDataResponse,
    BumpSequenceResponse,
    ManageBuyOfferResponse,
    PathPaymentStrictSendResponse,
]

PAYMENT_RESPONSE_TYPE_UNION = Union[
    CreateAccountResponse,
    PaymentResponse,
    AccountMergeResponse,
    PathPaymentStrictReceiveResponse,
    PathPaymentStrictSendResponse,
]

OPERATION_TYPE_I_RESPONSE = {
    CREATE_ACCOUNT: CreateAccountResponse,
    PAYMENT: PaymentResponse,
    PATH_PAYMENT_STRICT_RECEIVE: PathPaymentStrictReceiveResponse,
    MANAGE_SELL_OFFER: ManageSellOfferResponse,
    CREATE_PASSIVE_SELL_OFFER: CreatePassiveSellOfferResponse,
    SET_OPTIONS: SetOptionsResponse,
    CHANGE_TRUST: ChangeTrustResponse,
    ALLOW_TRUST: AllowTrustResponse,
    ACCOUNT_MERGE: AccountMergeResponse,
    INFLATION: InflationResponse,
    MANAGE_DATA: ManageDataResponse,
    BUMP_SEQUENCE: BumpSequenceResponse,
    MANAGE_BUY_OFFER: ManageBuyOfferResponse,
    PATH_PAYMENT_STRICT_SEND: PathPaymentStrictSendResponse,
}

OPERATION_TYPE_I_RESPONSE_TYPE = {
    CREATE_ACCOUNT: Type[CreateAccountResponse],
    PAYMENT: Type[PaymentResponse],
    PATH_PAYMENT_STRICT_RECEIVE: Type[PathPaymentStrictReceiveResponse],
    MANAGE_SELL_OFFER: Type[ManageSellOfferResponse],
    CREATE_PASSIVE_SELL_OFFER: Type[CreatePassiveSellOfferResponse],
    SET_OPTIONS: Type[SetOptionsResponse],
    CHANGE_TRUST: Type[ChangeTrustResponse],
    ALLOW_TRUST: Type[AllowTrustResponse],
    ACCOUNT_MERGE: Type[AccountMergeResponse],
    INFLATION: Type[InflationResponse],
    MANAGE_DATA: Type[ManageDataResponse],
    BUMP_SEQUENCE: Type[BumpSequenceResponse],
    MANAGE_BUY_OFFER: Type[ManageBuyOfferResponse],
    PATH_PAYMENT_STRICT_SEND: Type[PathPaymentStrictSendResponse],
}
