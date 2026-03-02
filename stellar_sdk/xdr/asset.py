# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .alpha_num4 import AlphaNum4
from .alpha_num12 import AlphaNum12
from .asset_type import AssetType
from .base import DEFAULT_XDR_MAX_DEPTH

__all__ = ["Asset"]


class Asset:
    """
    XDR Source Code::

        union Asset switch (AssetType type)
        {
        case ASSET_TYPE_NATIVE: // Not credit
            void;

        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AlphaNum4 alphaNum4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AlphaNum12 alphaNum12;

            // add other asset types here in the future
        };
    """

    def __init__(
        self,
        type: AssetType,
        alpha_num4: Optional[AlphaNum4] = None,
        alpha_num12: Optional[AlphaNum12] = None,
    ) -> None:
        self.type = type
        self.alpha_num4 = alpha_num4
        self.alpha_num12 = alpha_num12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_NATIVE:
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            if self.alpha_num4 is None:
                raise ValueError("alpha_num4 should not be None.")
            self.alpha_num4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            if self.alpha_num12 is None:
                raise ValueError("alpha_num12 should not be None.")
            self.alpha_num12.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Asset:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_NATIVE:
            return cls(type=type)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            alpha_num4 = AlphaNum4.unpack(unpacker, depth_limit - 1)
            return cls(type=type, alpha_num4=alpha_num4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            alpha_num12 = AlphaNum12.unpack(unpacker, depth_limit - 1)
            return cls(type=type, alpha_num12=alpha_num12)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Asset:
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
    def from_xdr(cls, xdr: str) -> Asset:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Asset:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == AssetType.ASSET_TYPE_NATIVE:
            return "native"
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            assert self.alpha_num4 is not None
            return {"credit_alphanum4": self.alpha_num4.to_json_dict()}
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            assert self.alpha_num12 is not None
            return {"credit_alphanum12": self.alpha_num12.to_json_dict()}
        raise ValueError(f"Unknown type in Asset: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> Asset:
        if isinstance(json_value, str):
            if json_value not in ("native",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for Asset, must be one of: native"
                )
            type = AssetType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for Asset, got: {json_value}"
            )
        key = next(iter(json_value))
        type = AssetType.from_json_dict(key)
        if key == "credit_alphanum4":
            alpha_num4 = AlphaNum4.from_json_dict(json_value["credit_alphanum4"])
            return cls(type=type, alpha_num4=alpha_num4)
        if key == "credit_alphanum12":
            alpha_num12 = AlphaNum12.from_json_dict(json_value["credit_alphanum12"])
            return cls(type=type, alpha_num12=alpha_num12)
        raise ValueError(f"Unknown key '{key}' for Asset")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.alpha_num4,
                self.alpha_num12,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.alpha_num4 == other.alpha_num4
            and self.alpha_num12 == other.alpha_num12
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.alpha_num4 is not None:
            out.append(f"alpha_num4={self.alpha_num4}")
        if self.alpha_num12 is not None:
            out.append(f"alpha_num12={self.alpha_num12}")
        return f"<Asset [{', '.join(out)}]>"
