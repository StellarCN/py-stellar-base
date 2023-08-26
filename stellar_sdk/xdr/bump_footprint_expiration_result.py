# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .bump_footprint_expiration_result_code import BumpFootprintExpirationResultCode

__all__ = ["BumpFootprintExpirationResult"]


class BumpFootprintExpirationResult:
    """
    XDR Source Code::

        union BumpFootprintExpirationResult switch (BumpFootprintExpirationResultCode code)
        {
        case BUMP_FOOTPRINT_EXPIRATION_SUCCESS:
            void;
        case BUMP_FOOTPRINT_EXPIRATION_MALFORMED:
        case BUMP_FOOTPRINT_EXPIRATION_RESOURCE_LIMIT_EXCEEDED:
            void;
        };
    """

    def __init__(
        self,
        code: BumpFootprintExpirationResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_SUCCESS
        ):
            return
        if (
            self.code
            == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_MALFORMED
        ):
            return
        if (
            self.code
            == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_RESOURCE_LIMIT_EXCEEDED
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BumpFootprintExpirationResult:
        code = BumpFootprintExpirationResultCode.unpack(unpacker)
        if code == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_SUCCESS:
            return cls(code=code)
        if (
            code
            == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_MALFORMED
        ):
            return cls(code=code)
        if (
            code
            == BumpFootprintExpirationResultCode.BUMP_FOOTPRINT_EXPIRATION_RESOURCE_LIMIT_EXCEEDED
        ):
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpFootprintExpirationResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BumpFootprintExpirationResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<BumpFootprintExpirationResult [{', '.join(out)}]>"
