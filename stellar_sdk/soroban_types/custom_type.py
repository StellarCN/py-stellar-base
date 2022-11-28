from dataclasses import dataclass
from typing import Union, Sequence, Optional

from .base import BaseScValAlias
from ..xdr import (
    SCObjectType,
    SCMap,
    SCMapEntry,
    SCSymbol,
    SCVal,
    SCValType,
    SCObject,
    SCVec,
)

__all__ = ["CustomTypeStructField", "CustomTypeStruct", "CustomTypeEnum"]


@dataclass
class CustomTypeStructField:
    key: str
    value: Union[SCVal, BaseScValAlias]


class CustomTypeStruct(BaseScValAlias):
    def __init__(self, fields: Sequence[CustomTypeStructField]):
        self.fields = fields

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_MAP,
                map=SCMap(
                    [
                        SCMapEntry(
                            key=SCVal(
                                SCValType.SCV_SYMBOL,
                                sym=SCSymbol(field.key.encode()),
                            ),
                            val=field.value._to_xdr_sc_val()
                            if isinstance(field.value, BaseScValAlias)
                            else field.value,
                        )
                        for field in self.fields
                    ]
                ),
            ),
        )


class CustomTypeEnum(BaseScValAlias):
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
