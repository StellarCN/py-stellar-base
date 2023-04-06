from typing import Union, Sequence

from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["StructField", "Struct", "TupleStruct"]


class StructField:
    """Represents a Soroban Struct field.

    :param key: The field key.
    :param value: The field value.
    """

    # TODO: code example
    def __init__(self, key: str, value: Union[stellar_xdr.SCVal, BaseScValAlias]):
        self.key = key
        self.value = (
            value.to_xdr_sc_val() if isinstance(value, BaseScValAlias) else value
        )

    def to_xdr_sc_map_entry(self) -> stellar_xdr.SCMapEntry:
        return stellar_xdr.SCMapEntry(
            key=stellar_xdr.SCVal(
                stellar_xdr.SCValType.SCV_SYMBOL,
                sym=stellar_xdr.SCSymbol(self.key.encode()),
            ),
            val=self.value,
        )

    @classmethod
    def from_xdr_sc_map_entry(
        cls, sc_map_entry: stellar_xdr.SCMapEntry
    ) -> "StructField":
        assert sc_map_entry.key.sym is not None
        return cls(
            sc_map_entry.key.sym.sc_symbol.decode(),
            sc_map_entry.val,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.value == other.value

    def __str__(self) -> str:
        return f"<StructField key={self.key} value={self.value}>"


class Struct(BaseScValAlias):
    """Represents a Soroban Struct type.

    :param fields: The struct fields.
    """

    # TODO: code example
    def __init__(self, fields: Sequence[StructField]):
        self.fields = fields

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_map(
            map=stellar_xdr.SCMap(
                [field.to_xdr_sc_map_entry() for field in self.fields]
            )
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Struct":
        if sc_val.type != stellar_xdr.SCValType.SCV_MAP:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.map is not None
        fields = [
            StructField.from_xdr_sc_map_entry(field) for field in sc_val.map.sc_map
        ]
        return cls(fields)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fields == other.fields

    def __str__(self) -> str:
        return f"<Struct fields={self.fields}>"


class TupleStruct(BaseScValAlias):
    """Represents a Soroban Tuple Struct type.

    :param fields: The tuple struct fields.
    """

    # TODO: code example
    def __init__(self, fields: Sequence[Union[stellar_xdr.SCVal, BaseScValAlias]]):
        self.fields = [
            field.to_xdr_sc_val() if isinstance(field, BaseScValAlias) else field
            for field in fields
        ]

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_vec(
            vec=stellar_xdr.SCVec(self.fields),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "TupleStruct":
        if sc_val.type != stellar_xdr.SCValType.SCV_VEC:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.vec is not None
        return cls(sc_val.vec.sc_vec)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fields == other.fields

    def __str__(self) -> str:
        return f"<TupleStruct fields={self.fields}>"
