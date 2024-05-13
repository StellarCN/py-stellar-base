# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String
from .error_code import ErrorCode

__all__ = ["Error"]


class Error:
    """
    XDR Source Code::

        struct Error
        {
            ErrorCode code;
            string msg<100>;
        };
    """

    def __init__(
        self,
        code: ErrorCode,
        msg: bytes,
    ) -> None:
        self.code = code
        self.msg = msg

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        String(self.msg, 100).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Error:
        code = ErrorCode.unpack(unpacker)
        msg = String.unpack(unpacker)
        return cls(
            code=code,
            msg=msg,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Error:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Error:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.code,
                self.msg,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.msg == other.msg

    def __repr__(self):
        out = [
            f"code={self.code}",
            f"msg={self.msg}",
        ]
        return f"<Error [{', '.join(out)}]>"
