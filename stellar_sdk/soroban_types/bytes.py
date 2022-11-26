from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType

__all__ = ["Bytes"]


class Bytes(BaseScValAlias):
    def __init__(self, value: bytes):
        self.value = value

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT, obj=SCObject(SCObjectType.SCO_BYTES, bin=self.value)
        )
