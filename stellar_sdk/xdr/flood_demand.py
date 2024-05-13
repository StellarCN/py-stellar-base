# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .tx_demand_vector import TxDemandVector

__all__ = ["FloodDemand"]


class FloodDemand:
    """
    XDR Source Code::

        struct FloodDemand
        {
            TxDemandVector txHashes;
        };
    """

    def __init__(
        self,
        tx_hashes: TxDemandVector,
    ) -> None:
        self.tx_hashes = tx_hashes

    def pack(self, packer: Packer) -> None:
        self.tx_hashes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> FloodDemand:
        tx_hashes = TxDemandVector.unpack(unpacker)
        return cls(
            tx_hashes=tx_hashes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FloodDemand:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> FloodDemand:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.tx_hashes,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx_hashes == other.tx_hashes

    def __repr__(self):
        out = [
            f"tx_hashes={self.tx_hashes}",
        ]
        return f"<FloodDemand [{', '.join(out)}]>"
