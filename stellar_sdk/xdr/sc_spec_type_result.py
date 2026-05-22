# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecTypeResult"]


class SCSpecTypeResult:
    """
    XDR Source Code::

        struct SCSpecTypeResult
        {
            SCSpecTypeDef okType;
            SCSpecTypeDef errorType;
        };
    """

    def __init__(
        self,
        ok_type: SCSpecTypeDef,
        error_type: SCSpecTypeDef,
    ) -> None:
        self.ok_type = ok_type
        self.error_type = error_type

    def pack(self, packer: Packer) -> None:
        self.ok_type.pack(packer)
        self.error_type.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecTypeResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ok_type = SCSpecTypeDef.unpack(unpacker, depth_limit - 1)
        error_type = SCSpecTypeDef.unpack(unpacker, depth_limit - 1)
        return cls(
            ok_type=ok_type,
            error_type=error_type,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeResult:
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
    def from_xdr(cls, xdr: str) -> SCSpecTypeResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecTypeResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ok_type": self.ok_type.to_json_dict(),
            "error_type": self.error_type.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCSpecTypeResult:
        ok_type = SCSpecTypeDef.from_json_dict(json_dict["ok_type"])
        error_type = SCSpecTypeDef.from_json_dict(json_dict["error_type"])
        return cls(
            ok_type=ok_type,
            error_type=error_type,
        )

    def __hash__(self):
        return hash(
            (
                self.ok_type,
                self.error_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ok_type == other.ok_type and self.error_type == other.error_type

    def __repr__(self):
        out = [
            f"ok_type={self.ok_type}",
            f"error_type={self.error_type}",
        ]
        return f"<SCSpecTypeResult [{', '.join(out)}]>"
