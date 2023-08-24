# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_error_code import SCErrorCode
from .sc_error_type import SCErrorType

__all__ = ["SCError"]


class SCError:
    """
    XDR Source Code::

        struct SCError
        {
            SCErrorType type;
            SCErrorCode code;
        };
    """

    def __init__(
        self,
        type: SCErrorType,
        code: SCErrorCode,
    ) -> None:
        self.type = type
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        self.code.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCError:
        type = SCErrorType.unpack(unpacker)
        code = SCErrorCode.unpack(unpacker)
        return cls(
            type=type,
            code=code,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCError:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCError:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.code == other.code

    def __str__(self):
        out = [
            f"type={self.type}",
            f"code={self.code}",
        ]
        return f"<SCError [{', '.join(out)}]>"
