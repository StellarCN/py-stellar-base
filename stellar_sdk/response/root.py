from schematics.types import StringType, IntType

from .base import BaseModel


class Root(BaseModel):
    horizon_version = StringType()
    core_version = StringType()
    history_latest_ledger = IntType()
    history_elder_ledger = IntType()
    core_latest_ledger = IntType()
    network_passphrase = StringType()
    current_protocol_version = IntType()
    core_supported_protocol_version = IntType()
