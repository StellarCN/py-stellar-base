# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint64 import Uint64
from .uint256 import Uint256

__all__ = ["MuxedEd25519Account"]


class MuxedEd25519Account:
    """
    XDR Source Code::

        struct MuxedEd25519Account
        {
            uint64 id;
            uint256 ed25519;
        };
    """

    def __init__(
        self,
        id: Uint64,
        ed25519: Uint256,
    ) -> None:
        self.id = id
        self.ed25519 = ed25519

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        self.ed25519.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> MuxedEd25519Account:
        id = Uint64.unpack(unpacker)
        ed25519 = Uint256.unpack(unpacker)
        return cls(
            id=id,
            ed25519=ed25519,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MuxedEd25519Account:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> MuxedEd25519Account:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.id,
                self.ed25519,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id and self.ed25519 == other.ed25519

    def __repr__(self):
        out = [
            f"id={self.id}",
            f"ed25519={self.ed25519}",
        ]
        return f"<MuxedEd25519Account [{', '.join(out)}]>"
