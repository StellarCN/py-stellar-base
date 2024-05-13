# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .sc_map_entry import SCMapEntry

__all__ = ["SCMap"]


class SCMap:
    """
    XDR Source Code::

        typedef SCMapEntry SCMap<>;
    """

    def __init__(self, sc_map: List[SCMapEntry]) -> None:
        _expect_max_length = 4294967295
        if sc_map and len(sc_map) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sc_map` should be {_expect_max_length}, but got {len(sc_map)}."
            )
        self.sc_map = sc_map

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.sc_map))
        for sc_map_item in self.sc_map:
            sc_map_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCMap:
        length = unpacker.unpack_uint()
        sc_map = []
        for _ in range(length):
            sc_map.append(SCMapEntry.unpack(unpacker))
        return cls(sc_map)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMap:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCMap:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.sc_map)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_map == other.sc_map

    def __repr__(self):
        return f"<SCMap [sc_map={self.sc_map}]>"
