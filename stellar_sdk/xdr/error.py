# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .error_code import ErrorCode

__all__ = ["Error"]


class Error:
    """
    XDR Source Code::

        struct Error
        {
            ErrorCode code;
            string msg<100>;
        };
    """

    def __init__(
        self,
        code: ErrorCode,
        msg: bytes,
    ) -> None:
        _expect_max_length = 100
        if msg and len(msg) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `msg` should be {_expect_max_length}, but got {len(msg)}."
            )
        self.code = code
        self.msg = msg

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        String(self.msg, 100).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Error:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = ErrorCode.unpack(unpacker)
        msg = String.unpack(unpacker, 100)
        return cls(
            code=code,
            msg=msg,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Error:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Error:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Error:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "code": self.code.to_json_dict(),
            "msg": String.to_json_dict(self.msg),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Error:
        code = ErrorCode.from_json_dict(json_dict["code"])
        msg = String.from_json_dict(json_dict["msg"])
        return cls(
            code=code,
            msg=msg,
        )

    def __hash__(self):
        return hash(
            (
                self.code,
                self.msg,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.msg == other.msg

    def __repr__(self):
        out = [
            f"code={self.code}",
            f"msg={self.msg}",
        ]
        return f"<Error [{', '.join(out)}]>"
