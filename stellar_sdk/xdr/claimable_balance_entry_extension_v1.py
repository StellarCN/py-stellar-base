# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claimable_balance_entry_extension_v1_ext import (
    ClaimableBalanceEntryExtensionV1Ext,
)
from .uint32 import Uint32

__all__ = ["ClaimableBalanceEntryExtensionV1"]


class ClaimableBalanceEntryExtensionV1:
    """
    XDR Source Code::

        struct ClaimableBalanceEntryExtensionV1
        {
            union switch (int v)
            {
            case 0:
                void;
            }
            ext;

            uint32 flags; // see ClaimableBalanceFlags
        };
    """

    def __init__(
        self,
        ext: ClaimableBalanceEntryExtensionV1Ext,
        flags: Uint32,
    ) -> None:
        self.ext = ext
        self.flags = flags

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.flags.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimableBalanceEntryExtensionV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ClaimableBalanceEntryExtensionV1Ext.unpack(unpacker, depth_limit - 1)
        flags = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            flags=flags,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimableBalanceEntryExtensionV1:
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
    def from_xdr(cls, xdr: str) -> ClaimableBalanceEntryExtensionV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimableBalanceEntryExtensionV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "flags": self.flags.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ClaimableBalanceEntryExtensionV1:
        ext = ClaimableBalanceEntryExtensionV1Ext.from_json_dict(json_dict["ext"])
        flags = Uint32.from_json_dict(json_dict["flags"])
        return cls(
            ext=ext,
            flags=flags,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.flags,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext and self.flags == other.flags

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"flags={self.flags}",
        ]
        return f"<ClaimableBalanceEntryExtensionV1 [{', '.join(out)}]>"
