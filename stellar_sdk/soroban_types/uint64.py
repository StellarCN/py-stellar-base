from .base import BaseScValAlias
from ..xdr import SCVal, SCObject, Uint64 as XdrUint64, SCValType, SCObjectType

__all__ = ["Uint64"]


class Uint64(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal.from_scv_object(SCObject.from_sco_u64(XdrUint64(self.value)))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint64":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_U64
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.u64 is not None
        return cls(sc_val.obj.u64.uint64)
