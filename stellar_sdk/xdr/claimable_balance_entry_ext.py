# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .claimable_balance_entry_extension_v1 import ClaimableBalanceEntryExtensionV1

__all__ = ["ClaimableBalanceEntryExt"]


class ClaimableBalanceEntryExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                ClaimableBalanceEntryExtensionV1 v1;
            }
    """

    def __init__(
        self,
        v: int,
        v1: Optional[ClaimableBalanceEntryExtensionV1] = None,
    ) -> None:
        self.v = v
        self.v1 = v1

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimableBalanceEntryExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            v1 = ClaimableBalanceEntryExtensionV1.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v1=v1)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimableBalanceEntryExt:
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
    def from_xdr(cls, xdr: str) -> ClaimableBalanceEntryExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimableBalanceEntryExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        if self.v == 1:
            assert self.v1 is not None
            return {"v1": self.v1.to_json_dict()}
        raise ValueError(f"Unknown v in ClaimableBalanceEntryExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> ClaimableBalanceEntryExt:
        if isinstance(json_value, str):
            if json_value not in ("v0",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for ClaimableBalanceEntryExt, must be one of: v0"
                )
            v = int(json_value[1:])
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ClaimableBalanceEntryExt, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v1":
            v1 = ClaimableBalanceEntryExtensionV1.from_json_dict(json_value["v1"])
            return cls(v=v, v1=v1)
        raise ValueError(f"Unknown key '{key}' for ClaimableBalanceEntryExt")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v1,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1 == other.v1

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v1 is not None:
            out.append(f"v1={self.v1}")
        return f"<ClaimableBalanceEntryExt [{', '.join(out)}]>"
