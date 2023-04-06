from typing import Union, Optional, List

from .base import BaseScValAlias
from ... import xdr as stellar_xdr


__all__ = ["Enum"]


class Enum(BaseScValAlias):
    """Represents a Soroban Enum type.

    :param key: The enum key.
    :param value: The enum value.
    """

    # TODO: code example
    def __init__(
        self, key: str, value: Optional[Union[stellar_xdr.SCVal, BaseScValAlias]]
    ):
        self.key = key
        if self.value is not None:
            self.value: Optional[stellar_xdr.SCVal] = (
                value.to_xdr_sc_val() if isinstance(value, BaseScValAlias) else value
            )
        else:
            self.value = None

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        vec: List[stellar_xdr.SCVal] = [
            stellar_xdr.SCVal(
                stellar_xdr.SCValType.SCV_SYMBOL,
                sym=stellar_xdr.SCSymbol(self.key.encode()),
            ),
        ]
        if self.value is not None:
            vec.append(self.value)
        return stellar_xdr.SCVal.from_scv_vec(stellar_xdr.SCVec(vec))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Enum":
        if sc_val.type != stellar_xdr.SCValType.SCV_VEC:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.vec is not None
        assert len(sc_val.vec.sc_vec) > 0
        assert sc_val.vec.sc_vec[0].sym is not None
        key = sc_val.vec.sc_vec[0].sym.sc_symbol.decode("utf-8")
        value_exists = len(sc_val.vec.sc_vec) > 1
        value = sc_val.vec.sc_vec[1] if value_exists else None
        return cls(key, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Enum [key={self.key}, value={self.value}]>"
