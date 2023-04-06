from typing import List, Union

from .base import BaseScValAlias
from ... import xdr as stellar_xdr


class MapEntry:
    """
    Represents a Soroban MapEntry type.

    :param key: The key of the map entry.
    :param value: The value of the map entry.
    """

    def __init__(
        self,
        key: Union[stellar_xdr.SCVal, BaseScValAlias],
        value: Union[stellar_xdr.SCVal, BaseScValAlias],
    ):
        self.key = key if isinstance(key, stellar_xdr.SCVal) else key.to_xdr_sc_val()
        self.value = (
            value if isinstance(value, stellar_xdr.SCVal) else value.to_xdr_sc_val()
        )

    def to_xdr_sc_map_entry(self) -> stellar_xdr.SCMapEntry:
        return stellar_xdr.SCMapEntry(
            key=self.key,
            val=self.value,
        )

    @classmethod
    def from_xdr_sc_map_entry(cls, sc_map_entry: stellar_xdr.SCMapEntry) -> "MapEntry":
        return cls(
            key=sc_map_entry.key,
            value=sc_map_entry.val,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.value == other.value

    def __str__(self) -> str:
        return f"<MapEntry [key={self.key}, value={self.value}]>"


class Map:
    """Represents a Soroban Map type.

    Map is an ordered key-value dictionary.

    The map is ordered by its keys. Iterating a map is stable and always
    returns the keys and values in order of the keys.

    :param entries: The list of map entries.
    """

    def __init__(self, entries: List[MapEntry]):
        self.entries = entries

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_map(
            stellar_xdr.SCMap(
                sc_map=[entry.to_xdr_sc_map_entry() for entry in self.entries]
            )
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Map":
        if sc_val.type != stellar_xdr.SCValType.SCV_MAP:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.map is not None
        return cls(
            entries=[
                MapEntry.from_xdr_sc_map_entry(entry) for entry in sc_val.map.sc_map
            ]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.entries == other.entries

    def __str__(self) -> str:
        return f"<Map [entries={self.entries}]>"
