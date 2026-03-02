# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .soroban_resources_ext_v0 import SorobanResourcesExtV0

__all__ = ["SorobanTransactionDataExt"]


class SorobanTransactionDataExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                SorobanResourcesExtV0 resourceExt;
            }
    """

    def __init__(
        self,
        v: int,
        resource_ext: Optional[SorobanResourcesExtV0] = None,
    ) -> None:
        self.v = v
        self.resource_ext = resource_ext

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.resource_ext is None:
                raise ValueError("resource_ext should not be None.")
            self.resource_ext.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanTransactionDataExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            resource_ext = SorobanResourcesExtV0.unpack(unpacker, depth_limit - 1)
            return cls(v=v, resource_ext=resource_ext)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionDataExt:
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
    def from_xdr(cls, xdr: str) -> SorobanTransactionDataExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanTransactionDataExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        if self.v == 1:
            assert self.resource_ext is not None
            return {"v1": self.resource_ext.to_json_dict()}
        raise ValueError(f"Unknown v in SorobanTransactionDataExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> SorobanTransactionDataExt:
        if isinstance(json_value, str):
            if json_value not in ("v0",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for SorobanTransactionDataExt, must be one of: v0"
                )
            v = int(json_value[1:])
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SorobanTransactionDataExt, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v1":
            resource_ext = SorobanResourcesExtV0.from_json_dict(json_value["v1"])
            return cls(v=v, resource_ext=resource_ext)
        raise ValueError(f"Unknown key '{key}' for SorobanTransactionDataExt")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.resource_ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.resource_ext == other.resource_ext

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.resource_ext is not None:
            out.append(f"resource_ext={self.resource_ext}")
        return f"<SorobanTransactionDataExt [{', '.join(out)}]>"
