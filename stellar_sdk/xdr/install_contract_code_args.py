# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .base import Opaque
from .constants import *

__all__ = ["InstallContractCodeArgs"]


class InstallContractCodeArgs:
    """
    XDR Source Code::

        struct InstallContractCodeArgs
        {
            opaque code<SCVAL_LIMIT>;
        };
    """

    def __init__(
        self,
        code: bytes,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        Opaque(self.code, SCVAL_LIMIT, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InstallContractCodeArgs":
        code = Opaque.unpack(unpacker, SCVAL_LIMIT, False)
        return cls(
            code=code,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InstallContractCodeArgs":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InstallContractCodeArgs":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = [
            f"code={self.code}",
        ]
        return f"<InstallContractCodeArgs [{', '.join(out)}]>"
