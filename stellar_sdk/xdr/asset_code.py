# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .asset_code4 import AssetCode4
from .asset_code12 import AssetCode12
from .asset_type import AssetType
from .base import DEFAULT_XDR_MAX_DEPTH

__all__ = ["AssetCode"]


class AssetCode:
    """
    XDR Source Code::

        union AssetCode switch (AssetType type)
        {
        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AssetCode4 assetCode4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AssetCode12 assetCode12;

            // add other asset types here in the future
        };
    """

    def __init__(
        self,
        type: AssetType,
        asset_code4: Optional[AssetCode4] = None,
        asset_code12: Optional[AssetCode12] = None,
    ) -> None:
        self.type = type
        self.asset_code4 = asset_code4
        self.asset_code12 = asset_code12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            if self.asset_code4 is None:
                raise ValueError("asset_code4 should not be None.")
            self.asset_code4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            if self.asset_code12 is None:
                raise ValueError("asset_code12 should not be None.")
            self.asset_code12.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AssetCode:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code4 = AssetCode4.unpack(unpacker, depth_limit - 1)
            return cls(type=type, asset_code4=asset_code4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code12 = AssetCode12.unpack(unpacker, depth_limit - 1)
            return cls(type=type, asset_code12=asset_code12)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AssetCode:
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
    def from_xdr(cls, xdr: str) -> AssetCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AssetCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            assert self.asset_code4 is not None
            return {"credit_alphanum4": self.asset_code4.to_json_dict()}
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            assert self.asset_code12 is not None
            return {"credit_alphanum12": self.asset_code12.to_json_dict()}
        raise ValueError(f"Unknown type in AssetCode: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> AssetCode:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for AssetCode, got: {json_value}"
            )
        key = next(iter(json_value))
        type = AssetType.from_json_dict(key)
        if key == "credit_alphanum4":
            asset_code4 = AssetCode4.from_json_dict(json_value["credit_alphanum4"])
            return cls(type=type, asset_code4=asset_code4)
        if key == "credit_alphanum12":
            asset_code12 = AssetCode12.from_json_dict(json_value["credit_alphanum12"])
            return cls(type=type, asset_code12=asset_code12)
        raise ValueError(f"Unknown key '{key}' for AssetCode")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.asset_code4,
                self.asset_code12,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.asset_code4 == other.asset_code4
            and self.asset_code12 == other.asset_code12
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.asset_code4 is not None:
            out.append(f"asset_code4={self.asset_code4}")
        if self.asset_code12 is not None:
            out.append(f"asset_code12={self.asset_code12}")
        return f"<AssetCode [{', '.join(out)}]>"
