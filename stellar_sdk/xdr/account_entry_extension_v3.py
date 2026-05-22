# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .extension_point import ExtensionPoint
from .time_point import TimePoint
from .uint32 import Uint32

__all__ = ["AccountEntryExtensionV3"]


class AccountEntryExtensionV3:
    """
    XDR Source Code::

        struct AccountEntryExtensionV3
        {
            // We can use this to add more fields, or because it is first, to
            // change AccountEntryExtensionV3 into a union.
            ExtensionPoint ext;

            // Ledger number at which `seqNum` took on its present value.
            uint32 seqLedger;

            // Time at which `seqNum` took on its present value.
            TimePoint seqTime;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        seq_ledger: Uint32,
        seq_time: TimePoint,
    ) -> None:
        self.ext = ext
        self.seq_ledger = seq_ledger
        self.seq_time = seq_time

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.seq_ledger.pack(packer)
        self.seq_time.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountEntryExtensionV3:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        seq_ledger = Uint32.unpack(unpacker, depth_limit - 1)
        seq_time = TimePoint.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            seq_ledger=seq_ledger,
            seq_time=seq_time,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountEntryExtensionV3:
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
    def from_xdr(cls, xdr: str) -> AccountEntryExtensionV3:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountEntryExtensionV3:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "seq_ledger": self.seq_ledger.to_json_dict(),
            "seq_time": self.seq_time.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> AccountEntryExtensionV3:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        seq_ledger = Uint32.from_json_dict(json_dict["seq_ledger"])
        seq_time = TimePoint.from_json_dict(json_dict["seq_time"])
        return cls(
            ext=ext,
            seq_ledger=seq_ledger,
            seq_time=seq_time,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.seq_ledger,
                self.seq_time,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.seq_ledger == other.seq_ledger
            and self.seq_time == other.seq_time
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"seq_ledger={self.seq_ledger}",
            f"seq_time={self.seq_time}",
        ]
        return f"<AccountEntryExtensionV3 [{', '.join(out)}]>"
