# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .allow_trust_result_code import AllowTrustResultCode

__all__ = ["AllowTrustResult"]


class AllowTrustResult:
    """
    XDR Source Code::

        union AllowTrustResult switch (AllowTrustResultCode code)
        {
        case ALLOW_TRUST_SUCCESS:
            void;
        case ALLOW_TRUST_MALFORMED:
        case ALLOW_TRUST_NO_TRUST_LINE:
        case ALLOW_TRUST_TRUST_NOT_REQUIRED:
        case ALLOW_TRUST_CANT_REVOKE:
        case ALLOW_TRUST_SELF_NOT_ALLOWED:
        case ALLOW_TRUST_LOW_RESERVE:
            void;
        };
    """

    def __init__(
        self,
        code: AllowTrustResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_MALFORMED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_NO_TRUST_LINE:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_TRUST_NOT_REQUIRED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_CANT_REVOKE:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SELF_NOT_ALLOWED:
            return
        if self.code == AllowTrustResultCode.ALLOW_TRUST_LOW_RESERVE:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AllowTrustResult:
        code = AllowTrustResultCode.unpack(unpacker)
        if code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_MALFORMED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_NO_TRUST_LINE:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_TRUST_NOT_REQUIRED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_CANT_REVOKE:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_SELF_NOT_ALLOWED:
            return cls(code=code)
        if code == AllowTrustResultCode.ALLOW_TRUST_LOW_RESERVE:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AllowTrustResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> AllowTrustResult:
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
        return f"<AllowTrustResult [{', '.join(out)}]>"
