# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .clawback_result_code import ClawbackResultCode

__all__ = ["ClawbackResult"]


class ClawbackResult:
    """
    XDR Source Code::

        union ClawbackResult switch (ClawbackResultCode code)
        {
        case CLAWBACK_SUCCESS:
            void;
        case CLAWBACK_MALFORMED:
        case CLAWBACK_NOT_CLAWBACK_ENABLED:
        case CLAWBACK_NO_TRUST:
        case CLAWBACK_UNDERFUNDED:
            void;
        };
    """

    def __init__(
        self,
        code: ClawbackResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ClawbackResultCode.CLAWBACK_SUCCESS:
            return
        if self.code == ClawbackResultCode.CLAWBACK_MALFORMED:
            return
        if self.code == ClawbackResultCode.CLAWBACK_NOT_CLAWBACK_ENABLED:
            return
        if self.code == ClawbackResultCode.CLAWBACK_NO_TRUST:
            return
        if self.code == ClawbackResultCode.CLAWBACK_UNDERFUNDED:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClawbackResult:
        code = ClawbackResultCode.unpack(unpacker)
        if code == ClawbackResultCode.CLAWBACK_SUCCESS:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_MALFORMED:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_NOT_CLAWBACK_ENABLED:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_NO_TRUST:
            return cls(code=code)
        if code == ClawbackResultCode.CLAWBACK_UNDERFUNDED:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClawbackResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ClawbackResult [{', '.join(out)}]>"
