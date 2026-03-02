# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_entry_extension_v3 import AccountEntryExtensionV3
from .base import DEFAULT_XDR_MAX_DEPTH, Integer

__all__ = ["AccountEntryExtensionV2Ext"]


class AccountEntryExtensionV2Ext:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 3:
                AccountEntryExtensionV3 v3;
            }
    """

    def __init__(
        self,
        v: int,
        v3: Optional[AccountEntryExtensionV3] = None,
    ) -> None:
        self.v = v
        self.v3 = v3

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 3:
            if self.v3 is None:
                raise ValueError("v3 should not be None.")
            self.v3.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountEntryExtensionV2Ext:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 3:
            v3 = AccountEntryExtensionV3.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v3=v3)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountEntryExtensionV2Ext:
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
    def from_xdr(cls, xdr: str) -> AccountEntryExtensionV2Ext:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountEntryExtensionV2Ext:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        if self.v == 3:
            assert self.v3 is not None
            return {"v3": self.v3.to_json_dict()}
        raise ValueError(f"Unknown v in AccountEntryExtensionV2Ext: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> AccountEntryExtensionV2Ext:
        if isinstance(json_value, str):
            if json_value not in ("v0",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for AccountEntryExtensionV2Ext, must be one of: v0"
                )
            v = int(json_value[1:])
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for AccountEntryExtensionV2Ext, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v3":
            v3 = AccountEntryExtensionV3.from_json_dict(json_value["v3"])
            return cls(v=v, v3=v3)
        raise ValueError(f"Unknown key '{key}' for AccountEntryExtensionV2Ext")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v3,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v3 == other.v3

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v3 is not None:
            out.append(f"v3={self.v3}")
        return f"<AccountEntryExtensionV2Ext [{', '.join(out)}]>"
