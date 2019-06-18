from schematics.types import IntType, BooleanType, StringType, DecimalType, DictType, ModelType, ListType

from .base import BaseModel


class Account(BaseModel):
    class Thresholds(BaseModel):
        low_threshold = IntType()
        med_threshold = IntType()
        high_threshold = IntType()

    class Flags(BaseModel):
        auth_required = BooleanType()
        auth_revocable = BooleanType()
        auth_immutable = BooleanType()

    class Balance(BaseModel):
        balance = DecimalType()
        limit = DecimalType()
        buying_liabilities = DecimalType()
        selling_liabilities = DecimalType()
        last_modified_ledger = IntType()
        is_authorized = BooleanType()
        asset_type = StringType()
        asset_code = StringType()
        asset_issuer = StringType()

    class Signer(BaseModel):
        key = StringType()
        weight = IntType()
        type = StringType()

    id = StringType()
    account_id = StringType()
    sequence = StringType()
    subentry_count = IntType()
    inflation_destination = StringType()
    home_domain = StringType()
    last_modified_ledger = IntType()
    thresholds = ModelType(Thresholds)
    flags = ModelType(Flags)
    paging_token = StringType()
    balances = ListType(ModelType(Balance), default=[])
    signers = ListType(ModelType(Signer), default=[])
    data = DictType(StringType, default={})
