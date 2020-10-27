# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .uint32 import Uint32
from .value import Value

__all__ = ["SCPBallot"]


class SCPBallot:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPBallot
    {
        uint32 counter; // n
        Value value;    // x
    };
    ----------------------------------------------------------------
    """

    def __init__(self, counter: Uint32, value: Value,) -> None:
        self.counter = counter
        self.value = value

    def pack(self, packer: Packer) -> None:
        self.counter.pack(packer)
        self.value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPBallot":
        counter = Uint32.unpack(unpacker)
        value = Value.unpack(unpacker)
        return cls(counter=counter, value=value,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPBallot":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPBallot":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.counter == other.counter and self.value == other.value

    def __str__(self):
        out = [
            f"counter={self.counter}",
            f"value={self.value}",
        ]
        return f"<SCPBallot {[', '.join(out)]}>"
