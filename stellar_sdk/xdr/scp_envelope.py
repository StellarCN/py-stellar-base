# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .scp_statement import SCPStatement
from .signature import Signature

__all__ = ["SCPEnvelope"]


class SCPEnvelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPEnvelope
    {
        SCPStatement statement;
        Signature signature;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        statement: SCPStatement,
        signature: Signature,
    ) -> None:
        self.statement = statement
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        self.statement.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPEnvelope":
        statement = SCPStatement.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        return cls(
            statement=statement,
            signature=signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPEnvelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPEnvelope":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.statement == other.statement and self.signature == other.signature

    def __str__(self):
        out = [
            f"statement={self.statement}",
            f"signature={self.signature}",
        ]
        return f"<SCPEnvelope {[', '.join(out)]}>"
