# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .bump_sequence_result_code import BumpSequenceResultCode

__all__ = ["BumpSequenceResult"]


class BumpSequenceResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union BumpSequenceResult switch (BumpSequenceResultCode code)
    {
    case BUMP_SEQUENCE_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: BumpSequenceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BumpSequenceResult":
        code = BumpSequenceResultCode.unpack(unpacker)
        if code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return cls(code)
        return cls(code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "BumpSequenceResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BumpSequenceResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<BumpSequenceResult {[', '.join(out)]}>"
