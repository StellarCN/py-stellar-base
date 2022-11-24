# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .set_trust_line_flags_result_code import SetTrustLineFlagsResultCode

__all__ = ["SetTrustLineFlagsResult"]


class SetTrustLineFlagsResult:
    """
    XDR Source Code::

        union SetTrustLineFlagsResult switch (SetTrustLineFlagsResultCode code)
        {
        case SET_TRUST_LINE_FLAGS_SUCCESS:
            void;
        case SET_TRUST_LINE_FLAGS_MALFORMED:
        case SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
        case SET_TRUST_LINE_FLAGS_CANT_REVOKE:
        case SET_TRUST_LINE_FLAGS_INVALID_STATE:
        case SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            void;
        };
    """

    def __init__(
        self,
        code: SetTrustLineFlagsResultCode,
    ) -> None:
        self.code = code

    @classmethod
    def from_set_trust_line_flags_success(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS)

    @classmethod
    def from_set_trust_line_flags_malformed(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED)

    @classmethod
    def from_set_trust_line_flags_no_trust_line(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE)

    @classmethod
    def from_set_trust_line_flags_cant_revoke(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE)

    @classmethod
    def from_set_trust_line_flags_invalid_state(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE)

    @classmethod
    def from_set_trust_line_flags_low_reserve(cls) -> "SetTrustLineFlagsResult":
        return cls(SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE)

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE:
            return
        if self.code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetTrustLineFlagsResult":
        code = SetTrustLineFlagsResultCode.unpack(unpacker)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_SUCCESS:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_MALFORMED:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_NO_TRUST_LINE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_CANT_REVOKE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_INVALID_STATE:
            return cls(code=code)
        if code == SetTrustLineFlagsResultCode.SET_TRUST_LINE_FLAGS_LOW_RESERVE:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SetTrustLineFlagsResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetTrustLineFlagsResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<SetTrustLineFlagsResult [{', '.join(out)}]>"
