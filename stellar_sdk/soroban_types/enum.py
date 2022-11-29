from typing import Union, Optional

from .base import BaseScValAlias
from ..xdr import (
    SCObjectType,
    SCSymbol,
    SCVal,
    SCValType,
    SCObject,
    SCVec,
)

__all__ = ["Enum"]


class Enum(BaseScValAlias):
    def __init__(self, key: str, value: Optional[Union[SCVal, BaseScValAlias]]):
        self.key = key
        self.value = value

    def _to_xdr_sc_val(self) -> SCVal:
        vec = [
            SCVal(SCValType.SCV_SYMBOL, sym=SCSymbol(self.key.encode())),
        ]
        if self.value is not None:
            vec.append(
                self.value._to_xdr_sc_val()
                if isinstance(self.value, BaseScValAlias)
                else self.value
            )
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(vec),
            ),
        )
