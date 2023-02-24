from .base import BaseScValAlias
from .. import xdr as stellar_xdr
from ..xdr import SCVal, SCValType, SCObject, SCObjectType

__all__ = ["Bytes"]


class Bytes(BaseScValAlias):
    def __init__(self, value: bytes):
        self.value = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT, obj=SCObject(SCObjectType.SCO_BYTES, bin=self.value)
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Bytes":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_BYTES
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.bin is not None
        return cls(sc_val.obj.bin)
