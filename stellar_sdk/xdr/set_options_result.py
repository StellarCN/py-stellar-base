# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .set_options_result_code import SetOptionsResultCode

__all__ = ["SetOptionsResult"]


class SetOptionsResult:
    """
    XDR Source Code::

        union SetOptionsResult switch (SetOptionsResultCode code)
        {
        case SET_OPTIONS_SUCCESS:
            void;
        case SET_OPTIONS_LOW_RESERVE:
        case SET_OPTIONS_TOO_MANY_SIGNERS:
        case SET_OPTIONS_BAD_FLAGS:
        case SET_OPTIONS_INVALID_INFLATION:
        case SET_OPTIONS_CANT_CHANGE:
        case SET_OPTIONS_UNKNOWN_FLAG:
        case SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
        case SET_OPTIONS_BAD_SIGNER:
        case SET_OPTIONS_INVALID_HOME_DOMAIN:
        case SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            void;
        };
    """

    def __init__(
        self,
        code: SetOptionsResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_LOW_RESERVE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_TOO_MANY_SIGNERS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_FLAGS:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_INFLATION:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_CANT_CHANGE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_UNKNOWN_FLAG:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_BAD_SIGNER:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_INVALID_HOME_DOMAIN:
            return
        if self.code == SetOptionsResultCode.SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SetOptionsResult:
        code = SetOptionsResultCode.unpack(unpacker)
        if code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_LOW_RESERVE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_TOO_MANY_SIGNERS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_BAD_FLAGS:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_INVALID_INFLATION:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_CANT_CHANGE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_UNKNOWN_FLAG:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_THRESHOLD_OUT_OF_RANGE:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_BAD_SIGNER:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_INVALID_HOME_DOMAIN:
            return cls(code=code)
        if code == SetOptionsResultCode.SET_OPTIONS_AUTH_REVOCABLE_REQUIRED:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SetOptionsResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SetOptionsResult:
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
        return f"<SetOptionsResult [{', '.join(out)}]>"
