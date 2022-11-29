from dataclasses import dataclass
from typing import Union, Sequence

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

__all__ = ["StructField", "Struct"]


@dataclass
class StructField:
    key: str
    value: Union[SCVal, BaseScValAlias]


class Struct(BaseScValAlias):
    def __init__(self, fields: Sequence[StructField]):
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


class TupleStruct(BaseScValAlias):
    def __init__(self, fields: Sequence[Union[SCVal, BaseScValAlias]]):
        self.fields = fields

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(
                    [
                        field._to_xdr_sc_val()
                        if isinstance(field, BaseScValAlias)
                        else field
                        for field in self.fields
                    ]
                ),
            ),
        )
