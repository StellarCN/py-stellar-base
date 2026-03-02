# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .data_value import DataValue
from .string64 import String64

__all__ = ["ManageDataOp"]


class ManageDataOp:
    """
    XDR Source Code::

        struct ManageDataOp
        {
            string64 dataName;
            DataValue* dataValue; // set to null to clear
        };
    """

    def __init__(
        self,
        data_name: String64,
        data_value: Optional[DataValue],
    ) -> None:
        self.data_name = data_name
        self.data_value = data_value

    def pack(self, packer: Packer) -> None:
        self.data_name.pack(packer)
        if self.data_value is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.data_value.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ManageDataOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        data_name = String64.unpack(unpacker, depth_limit - 1)
        data_value = (
            DataValue.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        return cls(
            data_name=data_name,
            data_value=data_value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageDataOp:
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
    def from_xdr(cls, xdr: str) -> ManageDataOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageDataOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "data_name": self.data_name.to_json_dict(),
            "data_value": (
                self.data_value.to_json_dict() if self.data_value is not None else None
            ),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ManageDataOp:
        data_name = String64.from_json_dict(json_dict["data_name"])
        data_value = (
            DataValue.from_json_dict(json_dict["data_value"])
            if json_dict["data_value"] is not None
            else None
        )
        return cls(
            data_name=data_name,
            data_value=data_value,
        )

    def __hash__(self):
        return hash(
            (
                self.data_name,
                self.data_value,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_name == other.data_name and self.data_value == other.data_value

    def __repr__(self):
        out = [
            f"data_name={self.data_name}",
            f"data_value={self.data_value}",
        ]
        return f"<ManageDataOp [{', '.join(out)}]>"
