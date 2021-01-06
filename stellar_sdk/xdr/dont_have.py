# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .message_type import MessageType
from .uint256 import Uint256

__all__ = ["DontHave"]


class DontHave:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct DontHave
    {
        MessageType type;
        uint256 reqHash;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, type: MessageType, req_hash: Uint256,) -> None:
        self.type = type
        self.req_hash = req_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        self.req_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DontHave":
        type = MessageType.unpack(unpacker)
        req_hash = Uint256.unpack(unpacker)
        return cls(type=type, req_hash=req_hash,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "DontHave":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DontHave":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.req_hash == other.req_hash

    def __str__(self):
        out = [
            f"type={self.type}",
            f"req_hash={self.req_hash}",
        ]
        return f"<DontHave {[', '.join(out)]}>"
