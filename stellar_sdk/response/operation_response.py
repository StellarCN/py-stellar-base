from typing import Optional, List, Union, Type

from pydantic import BaseModel, Field

from .common import Asset, Link, Price
from .transaction_response import TransactionResponse
from ..xdr.xdr import OperationType

__all__ = [
    "CreateAccountOperationResponse",
    "PaymentOperationResponse",
    "PathPaymentStrictReceiveOperationResponse",
    "ManageSellOfferOperationResponse",
    "CreatePassiveSellOfferOperationResponse",
    "SetOptionsOperationResponse",
    "ChangeTrustOperationResponse",
    "AllowTrustOperationResponse",
    "AccountMergeOperationResponse",
    "InflationOperationResponse",
    "ManageDataOperationResponse",
    "BumpSequenceOperationResponse",
    "ManageBuyOfferOperationResponse",
    "PathPaymentStrictSendOperationResponse",
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
    created_at: str
    transaction_hash: str
    transaction: Optional[TransactionResponse]
    links: Links = Field(None, alias="_links")


class BumpSequenceOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is BumpSequence.
    """

    bump_to: int  # str in Go impl


class CreateAccountOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is CreateAccount.
    """

    starting_balance: str
    funder: str
    account: str


class PaymentOperationResponse(BaseOperationResponse):
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


class PathPaymentStrictReceiveOperationResponse(BaseOperationResponse):
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


class PathPaymentStrictSendOperationResponse(BaseOperationResponse):
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


class ManageDataOperationResponse(BaseOperationResponse):
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


class CreatePassiveSellOfferOperationResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is CreatePassiveSellOffer.
    """


class ManageSellOfferOperationResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is CreatePassiveSellOffer.
    """

    offer_id: int  # str in Go Impl


class ManageBuyOfferOperationResponse(BaseOfferOperationResponse):
    """The resource representing a single operation whose type is ManageBuyOffer.
    """

    offer_id: int  # str in Go Impl


class SetOptionsOperationResponse(BaseOperationResponse):
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


class ChangeTrustOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is ChangeTrust.
    """

    asset_type: str
    asset_code: str
    asset_issuer: str
    limit: str
    trustee: str
    trustor: str


class AllowTrustOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is AllowTrust.
    """

    asset_type: str
    asset_code: str
    asset_issuer: str
    trustee: str
    trustor: str
    authorize: bool
    authorize_to_maintain_liabilities: bool


class AccountMergeOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is AccountMerge.
    """

    account: str
    into: str


class InflationOperationResponse(BaseOperationResponse):
    """The resource representing a single operation whose type is Inflation.
    """


OPERATION_RESPONSE_TYPE_UNION = Union[
    CreateAccountOperationResponse,
    PaymentOperationResponse,
    PathPaymentStrictReceiveOperationResponse,
    ManageSellOfferOperationResponse,
    CreatePassiveSellOfferOperationResponse,
    SetOptionsOperationResponse,
    ChangeTrustOperationResponse,
    AllowTrustOperationResponse,
    AccountMergeOperationResponse,
    InflationOperationResponse,
    ManageDataOperationResponse,
    BumpSequenceOperationResponse,
    ManageBuyOfferOperationResponse,
    PathPaymentStrictSendOperationResponse,
]

PAYMENT_RESPONSE_TYPE_UNION = Union[
    CreateAccountOperationResponse,
    PaymentOperationResponse,
    AccountMergeOperationResponse,
    PathPaymentStrictReceiveOperationResponse,
    PathPaymentStrictSendOperationResponse,
]

OPERATION_TYPE_I_RESPONSE = {
    OperationType.CREATE_ACCOUNT.value: CreateAccountOperationResponse,
    OperationType.PAYMENT.value: PaymentOperationResponse,
    OperationType.PATH_PAYMENT_STRICT_RECEIVE.value: PathPaymentStrictReceiveOperationResponse,
    OperationType.MANAGE_SELL_OFFER.value: ManageSellOfferOperationResponse,
    OperationType.CREATE_PASSIVE_SELL_OFFER.value: CreatePassiveSellOfferOperationResponse,
    OperationType.SET_OPTIONS.value: SetOptionsOperationResponse,
    OperationType.CHANGE_TRUST.value: ChangeTrustOperationResponse,
    OperationType.ALLOW_TRUST.value: AllowTrustOperationResponse,
    OperationType.ACCOUNT_MERGE.value: AccountMergeOperationResponse,
    OperationType.INFLATION.value: InflationOperationResponse,
    OperationType.MANAGE_DATA.value: ManageDataOperationResponse,
    OperationType.BUMP_SEQUENCE.value: BumpSequenceOperationResponse,
    OperationType.MANAGE_BUY_OFFER.value: ManageBuyOfferOperationResponse,
    OperationType.PATH_PAYMENT_STRICT_SEND.value: PathPaymentStrictSendOperationResponse,
}

OPERATION_TYPE_I_RESPONSE_TYPE = {
    OperationType.CREATE_ACCOUNT.value: Type[CreateAccountOperationResponse],
    OperationType.PAYMENT.value: Type[PaymentOperationResponse],
    OperationType.PATH_PAYMENT_STRICT_RECEIVE.value: Type[
        PathPaymentStrictReceiveOperationResponse
    ],
    OperationType.MANAGE_SELL_OFFER.value: Type[ManageSellOfferOperationResponse],
    OperationType.CREATE_PASSIVE_SELL_OFFER.value: Type[
        CreatePassiveSellOfferOperationResponse
    ],
    OperationType.SET_OPTIONS.value: Type[SetOptionsOperationResponse],
    OperationType.CHANGE_TRUST.value: Type[ChangeTrustOperationResponse],
    OperationType.ALLOW_TRUST.value: Type[AllowTrustOperationResponse],
    OperationType.ACCOUNT_MERGE.value: Type[AccountMergeOperationResponse],
    OperationType.INFLATION.value: Type[InflationOperationResponse],
    OperationType.MANAGE_DATA.value: Type[ManageDataOperationResponse],
    OperationType.BUMP_SEQUENCE.value: Type[BumpSequenceOperationResponse],
    OperationType.MANAGE_BUY_OFFER.value: Type[ManageBuyOfferOperationResponse],
    OperationType.PATH_PAYMENT_STRICT_SEND.value: Type[
        PathPaymentStrictSendOperationResponse
    ],
}
