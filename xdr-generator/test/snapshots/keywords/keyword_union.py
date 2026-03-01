# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH, Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .keyword_enum import KeywordEnum
from .pass_ import Pass
__all__ = ['KeywordUnion']
class KeywordUnion:
    """
    XDR Source Code::

        union keyword_union switch (keyword_enum from)
        {
            case from:
                pass class;
            default:
                void;
        };
    """
    def __init__(
        self,
        from_: KeywordEnum,
        class_: Optional[Pass] = None,
    ) -> None:
        self.from_ = from_
        self.class_ = class_
    def pack(self, packer: Packer) -> None:
        self.from_.pack(packer)
        if self.from_ == KeywordEnum.from_:
            if self.class_ is None:
                raise ValueError("class_ should not be None.")
            self.class_.pack(packer)
            return
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> KeywordUnion:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        from_ = KeywordEnum.unpack(unpacker)
        if from_ == KeywordEnum.from_:
            class_ = Pass.unpack(unpacker, depth_limit - 1)
            return cls(from_=from_, class_=class_)
        return cls(from_=from_)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> KeywordUnion:
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
    def from_xdr(cls, xdr: str) -> KeywordUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> KeywordUnion:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self):
        if self.from_ == KeywordEnum.from_:
            assert self.class_ is not None
            return {"from": self.class_.to_json_dict()}
        return self.from_.to_json_dict()
    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> KeywordUnion:
        if isinstance(json_value, str):
            if json_value in ("from",):
                raise ValueError(f"'{json_value}' requires a value for KeywordUnion, use dict form instead")
            from_ = KeywordEnum.from_json_dict(json_value)
            return cls(from_=from_)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(f"Expected a single-key object for KeywordUnion, got: {json_value}")
        key = next(iter(json_value))
        from_ = KeywordEnum.from_json_dict(key)
        if key == "from":
            class_ = Pass.from_json_dict(json_value["from"])
            return cls(from_=from_, class_=class_)
        raise ValueError(f"Unknown key '{key}' for KeywordUnion")
    def __hash__(self):
        return hash((self.from_, self.class_,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.from_ == other.from_ and self.class_ == other.class_
    def __repr__(self):
        out = []
        out.append(f'from_={self.from_}')
        if self.class_ is not None:
            out.append(f'class_={self.class_}')
        return f"<KeywordUnion [{', '.join(out)}]>"
