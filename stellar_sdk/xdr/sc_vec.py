# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .sc_val import SCVal

__all__ = ["SCVec"]


class SCVec:
    """
    XDR Source Code::

        typedef SCVal SCVec<>;
    """

    def __init__(self, sc_vec: List[SCVal]) -> None:
        _expect_max_length = 4294967295
        if sc_vec and len(sc_vec) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sc_vec` should be {_expect_max_length}, but got {len(sc_vec)}."
            )
        self.sc_vec = sc_vec

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.sc_vec))
        for sc_vec_item in self.sc_vec:
            sc_vec_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCVec:
        length = unpacker.unpack_uint()
        sc_vec = []
        for _ in range(length):
            sc_vec.append(SCVal.unpack(unpacker))
        return cls(sc_vec)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCVec:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCVec:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.sc_vec)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_vec == other.sc_vec

    def __repr__(self):
        return f"<SCVec [sc_vec={self.sc_vec}]>"
