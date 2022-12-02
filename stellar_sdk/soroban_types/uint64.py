from .base import BaseScValAlias
from ..xdr import SCVal, SCObject, Uint64 as XdrUint64

__all__ = ["Uint64"]


class Uint64(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal.from_scv_object(SCObject.from_sco_u64(XdrUint64(self.value)))
