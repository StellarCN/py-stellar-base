# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .manage_data_result_code import ManageDataResultCode

__all__ = ["ManageDataResult"]


class ManageDataResult:
    """
    XDR Source Code::

        union ManageDataResult switch (ManageDataResultCode code)
        {
        case MANAGE_DATA_SUCCESS:
            void;
        case MANAGE_DATA_NOT_SUPPORTED_YET:
        case MANAGE_DATA_NAME_NOT_FOUND:
        case MANAGE_DATA_LOW_RESERVE:
        case MANAGE_DATA_INVALID_NAME:
            void;
        };
    """

    def __init__(
        self,
        code: ManageDataResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_NOT_SUPPORTED_YET:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_NAME_NOT_FOUND:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_LOW_RESERVE:
            return
        if self.code == ManageDataResultCode.MANAGE_DATA_INVALID_NAME:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageDataResult:
        code = ManageDataResultCode.unpack(unpacker)
        if code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_NOT_SUPPORTED_YET:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_NAME_NOT_FOUND:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_LOW_RESERVE:
            return cls(code=code)
        if code == ManageDataResultCode.MANAGE_DATA_INVALID_NAME:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageDataResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ManageDataResult:
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
        return f"<ManageDataResult [{', '.join(out)}]>"
