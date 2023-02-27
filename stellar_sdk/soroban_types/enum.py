from typing import Union, Optional, List

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
    """Represents a Soroban Enum type.

    :param key: The enum key.
    :param value: The enum value.
    """

    # TODO: code example
    def __init__(self, key: str, value: Optional[Union[SCVal, BaseScValAlias]]):
        self.key = key
        if self.value is not None:
            self.value: Optional[SCVal] = (
                value.to_xdr_sc_val() if isinstance(value, BaseScValAlias) else value
            )
        else:
            self.value = None

    def to_xdr_sc_val(self) -> SCVal:
        vec: List[SCVal] = [
            SCVal(SCValType.SCV_SYMBOL, sym=SCSymbol(self.key.encode())),
        ]
        if self.value is not None:
            vec.append(self.value)
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(vec),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Enum":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_VEC
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.vec is not None
        assert sc_val.obj.vec.sc_vec[0].sym is not None
        key = sc_val.obj.vec.sc_vec[0].sym.sc_symbol.decode("utf-8")
        value_exists = len(sc_val.obj.vec.sc_vec) > 1
        value = sc_val.obj.vec.sc_vec[1] if value_exists else None
        return cls(key, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Enum [key={self.key}, value={self.value}]>"
