from typing import Union

from .base import BaseScValAlias
from ..keypair import Keypair
from ..xdr import SCVal, SCValType, SCObjectType, SCObject

__all__ = ["AccountId"]


class AccountId(BaseScValAlias):
    def __init__(self, public_key: Union[str, Keypair]):
        if isinstance(public_key, str):
            public_key = Keypair.from_public_key(public_key)
        self.keypair: Keypair = public_key

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_ACCOUNT_ID, account_id=self.keypair.xdr_account_id()
            ),
        )
