# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque
from .sc_num_sign import SCNumSign

__all__ = ["SCBigInt"]


class SCBigInt:
    """
    XDR Source Code::

        union SCBigInt switch (SCNumSign sign)
        {
        case ZERO:
            void;
        case POSITIVE:
        case NEGATIVE:
            opaque magnitude<256000>;
        };
    """

    def __init__(
        self,
        sign: SCNumSign,
        magnitude: bytes = None,
    ) -> None:
        self.sign = sign
        self.magnitude = magnitude

    def pack(self, packer: Packer) -> None:
        self.sign.pack(packer)
        if self.sign == SCNumSign.ZERO:
            return
        if self.sign == SCNumSign.POSITIVE:
            if self.magnitude is None:
                raise ValueError("magnitude should not be None.")
            Opaque(self.magnitude, 256000, False).pack(packer)
            return
        if self.sign == SCNumSign.NEGATIVE:
            if self.magnitude is None:
                raise ValueError("magnitude should not be None.")
            Opaque(self.magnitude, 256000, False).pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCBigInt":
        sign = SCNumSign.unpack(unpacker)
        if sign == SCNumSign.ZERO:
            return cls(sign=sign)
        if sign == SCNumSign.POSITIVE:
            magnitude = Opaque.unpack(unpacker, 256000, False)
            return cls(sign=sign, magnitude=magnitude)
        if sign == SCNumSign.NEGATIVE:
            magnitude = Opaque.unpack(unpacker, 256000, False)
            return cls(sign=sign, magnitude=magnitude)
        return cls(sign=sign)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCBigInt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCBigInt":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sign == other.sign and self.magnitude == other.magnitude

    def __str__(self):
        out = []
        out.append(f"sign={self.sign}")
        out.append(
            f"magnitude={self.magnitude}"
        ) if self.magnitude is not None else None
        return f"<SCBigInt [{', '.join(out)}]>"
