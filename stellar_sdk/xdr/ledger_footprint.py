# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .ledger_key import LedgerKey

__all__ = ["LedgerFootprint"]


class LedgerFootprint:
    """
    XDR Source Code::

        struct LedgerFootprint
        {
            LedgerKey readOnly<>;
            LedgerKey readWrite<>;
        };
    """

    def __init__(
        self,
        read_only: List[LedgerKey],
        read_write: List[LedgerKey],
    ) -> None:
        _expect_max_length = 4294967295
        if read_only and len(read_only) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `read_only` should be {_expect_max_length}, but got {len(read_only)}."
            )
        _expect_max_length = 4294967295
        if read_write and len(read_write) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `read_write` should be {_expect_max_length}, but got {len(read_write)}."
            )
        self.read_only = read_only
        self.read_write = read_write

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.read_only))
        for read_only_item in self.read_only:
            read_only_item.pack(packer)
        packer.pack_uint(len(self.read_write))
        for read_write_item in self.read_write:
            read_write_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerFootprint:
        length = unpacker.unpack_uint()
        read_only = []
        for _ in range(length):
            read_only.append(LedgerKey.unpack(unpacker))
        length = unpacker.unpack_uint()
        read_write = []
        for _ in range(length):
            read_write.append(LedgerKey.unpack(unpacker))
        return cls(
            read_only=read_only,
            read_write=read_write,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerFootprint:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerFootprint:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.read_only,
                self.read_write,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.read_only == other.read_only and self.read_write == other.read_write

    def __repr__(self):
        out = [
            f"read_only={self.read_only}",
            f"read_write={self.read_write}",
        ]
        return f"<LedgerFootprint [{', '.join(out)}]>"
