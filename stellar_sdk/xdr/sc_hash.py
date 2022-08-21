# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .sc_hash_type import SCHashType

__all__ = ["SCHash"]


class SCHash:
    """
    XDR Source Code::

        union SCHash switch (SCHashType type)
        {
        case SCHASH_SHA256:
            Hash sha256;
        };
    """

    def __init__(
        self,
        type: SCHashType,
        sha256: Hash = None,
    ) -> None:
        self.type = type
        self.sha256 = sha256

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCHashType.SCHASH_SHA256:
            if self.sha256 is None:
                raise ValueError("sha256 should not be None.")
            self.sha256.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHash":
        type = SCHashType.unpack(unpacker)
        if type == SCHashType.SCHASH_SHA256:
            sha256 = Hash.unpack(unpacker)
            return cls(type=type, sha256=sha256)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHash":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHash":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.sha256 == other.sha256

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"sha256={self.sha256}") if self.sha256 is not None else None
        return f"<SCHash [{', '.join(out)}]>"
