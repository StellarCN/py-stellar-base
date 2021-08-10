# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .sequence_number import SequenceNumber

__all__ = ["BumpSequenceOp"]


class BumpSequenceOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct BumpSequenceOp
    {
        SequenceNumber bumpTo;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        bump_to: SequenceNumber,
    ) -> None:
        self.bump_to = bump_to

    def pack(self, packer: Packer) -> None:
        self.bump_to.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BumpSequenceOp":
        bump_to = SequenceNumber.unpack(unpacker)
        return cls(
            bump_to=bump_to,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "BumpSequenceOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BumpSequenceOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.bump_to == other.bump_to

    def __str__(self):
        out = [
            f"bump_to={self.bump_to}",
        ]
        return f"<BumpSequenceOp {[', '.join(out)]}>"
