from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, SCBigInt, SCNumSign

__all__ = ["BigInt"]


class BigInt(BaseScValAlias):
    def __init__(self, value: int):
        self.value = value

    def _to_xdr_sc_val(self) -> SCVal:
        if self.value == 0:
            return SCVal(
                SCValType.SCV_OBJECT,
                obj=SCObject(
                    SCObjectType.SCO_BIG_INT, big_int=SCBigInt(SCNumSign.ZERO)
                ),
            )
        v_abs = abs(self.value)
        magnitude = v_abs.to_bytes((v_abs.bit_length() + 7) // 8, byteorder="big")
        if self.value > 0:
            return SCVal(
                SCValType.SCV_OBJECT,
                obj=SCObject(
                    SCObjectType.SCO_BIG_INT,
                    big_int=SCBigInt(SCNumSign.POSITIVE, magnitude=magnitude),
                ),
            )
        else:
            return SCVal(
                SCValType.SCV_OBJECT,
                obj=SCObject(
                    SCObjectType.SCO_BIG_INT,
                    big_int=SCBigInt(SCNumSign.NEGATIVE, magnitude=magnitude),
                ),
            )
