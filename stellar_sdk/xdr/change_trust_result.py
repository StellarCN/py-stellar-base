# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .change_trust_result_code import ChangeTrustResultCode
from ..exceptions import ValueError

__all__ = ["ChangeTrustResult"]


class ChangeTrustResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ChangeTrustResult switch (ChangeTrustResultCode code)
    {
    case CHANGE_TRUST_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: ChangeTrustResultCode,) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ChangeTrustResult":
        code = ChangeTrustResultCode.unpack(unpacker)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return cls(code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ChangeTrustResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ChangeTrustResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ChangeTrustResult {[', '.join(out)]}>"
