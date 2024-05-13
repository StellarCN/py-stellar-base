# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .change_trust_result_code import ChangeTrustResultCode

__all__ = ["ChangeTrustResult"]


class ChangeTrustResult:
    """
    XDR Source Code::

        union ChangeTrustResult switch (ChangeTrustResultCode code)
        {
        case CHANGE_TRUST_SUCCESS:
            void;
        case CHANGE_TRUST_MALFORMED:
        case CHANGE_TRUST_NO_ISSUER:
        case CHANGE_TRUST_INVALID_LIMIT:
        case CHANGE_TRUST_LOW_RESERVE:
        case CHANGE_TRUST_SELF_NOT_ALLOWED:
        case CHANGE_TRUST_TRUST_LINE_MISSING:
        case CHANGE_TRUST_CANNOT_DELETE:
        case CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES:
            void;
        };
    """

    def __init__(
        self,
        code: ChangeTrustResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_MALFORMED:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_NO_ISSUER:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_INVALID_LIMIT:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_LOW_RESERVE:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SELF_NOT_ALLOWED:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_TRUST_LINE_MISSING:
            return
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_CANNOT_DELETE:
            return
        if (
            self.code
            == ChangeTrustResultCode.CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ChangeTrustResult:
        code = ChangeTrustResultCode.unpack(unpacker)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_MALFORMED:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_NO_ISSUER:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_INVALID_LIMIT:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_LOW_RESERVE:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SELF_NOT_ALLOWED:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_TRUST_LINE_MISSING:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_CANNOT_DELETE:
            return cls(code=code)
        if code == ChangeTrustResultCode.CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ChangeTrustResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ChangeTrustResult:
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
        return f"<ChangeTrustResult [{', '.join(out)}]>"
