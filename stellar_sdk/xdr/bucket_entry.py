# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .bucket_entry_type import BucketEntryType
from .bucket_metadata import BucketMetadata
from .ledger_entry import LedgerEntry
from .ledger_key import LedgerKey

__all__ = ["BucketEntry"]


class BucketEntry:
    """
    XDR Source Code::

        union BucketEntry switch (BucketEntryType type)
        {
        case LIVEENTRY:
        case INITENTRY:
            LedgerEntry liveEntry;

        case DEADENTRY:
            LedgerKey deadEntry;
        case METAENTRY:
            BucketMetadata metaEntry;
        };
    """

    def __init__(
        self,
        type: BucketEntryType,
        live_entry: Optional[LedgerEntry] = None,
        dead_entry: Optional[LedgerKey] = None,
        meta_entry: Optional[BucketMetadata] = None,
    ) -> None:
        self.type = type
        self.live_entry = live_entry
        self.dead_entry = dead_entry
        self.meta_entry = meta_entry

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == BucketEntryType.LIVEENTRY:
            if self.live_entry is None:
                raise ValueError("live_entry should not be None.")
            self.live_entry.pack(packer)
            return
        if self.type == BucketEntryType.INITENTRY:
            if self.live_entry is None:
                raise ValueError("live_entry should not be None.")
            self.live_entry.pack(packer)
            return
        if self.type == BucketEntryType.DEADENTRY:
            if self.dead_entry is None:
                raise ValueError("dead_entry should not be None.")
            self.dead_entry.pack(packer)
            return
        if self.type == BucketEntryType.METAENTRY:
            if self.meta_entry is None:
                raise ValueError("meta_entry should not be None.")
            self.meta_entry.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BucketEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = BucketEntryType.unpack(unpacker)
        if type == BucketEntryType.LIVEENTRY:
            live_entry = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, live_entry=live_entry)
        if type == BucketEntryType.INITENTRY:
            live_entry = LedgerEntry.unpack(unpacker, depth_limit - 1)
            return cls(type=type, live_entry=live_entry)
        if type == BucketEntryType.DEADENTRY:
            dead_entry = LedgerKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, dead_entry=dead_entry)
        if type == BucketEntryType.METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker, depth_limit - 1)
            return cls(type=type, meta_entry=meta_entry)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BucketEntry:
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
    def from_xdr(cls, xdr: str) -> BucketEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BucketEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == BucketEntryType.LIVEENTRY:
            assert self.live_entry is not None
            return {"liveentry": self.live_entry.to_json_dict()}
        if self.type == BucketEntryType.INITENTRY:
            assert self.live_entry is not None
            return {"initentry": self.live_entry.to_json_dict()}
        if self.type == BucketEntryType.DEADENTRY:
            assert self.dead_entry is not None
            return {"deadentry": self.dead_entry.to_json_dict()}
        if self.type == BucketEntryType.METAENTRY:
            assert self.meta_entry is not None
            return {"metaentry": self.meta_entry.to_json_dict()}
        raise ValueError(f"Unknown type in BucketEntry: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> BucketEntry:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for BucketEntry, got: {json_value}"
            )
        key = next(iter(json_value))
        type = BucketEntryType.from_json_dict(key)
        if key == "liveentry":
            live_entry = LedgerEntry.from_json_dict(json_value["liveentry"])
            return cls(type=type, live_entry=live_entry)
        if key == "initentry":
            live_entry = LedgerEntry.from_json_dict(json_value["initentry"])
            return cls(type=type, live_entry=live_entry)
        if key == "deadentry":
            dead_entry = LedgerKey.from_json_dict(json_value["deadentry"])
            return cls(type=type, dead_entry=dead_entry)
        if key == "metaentry":
            meta_entry = BucketMetadata.from_json_dict(json_value["metaentry"])
            return cls(type=type, meta_entry=meta_entry)
        raise ValueError(f"Unknown key '{key}' for BucketEntry")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.live_entry,
                self.dead_entry,
                self.meta_entry,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.live_entry == other.live_entry
            and self.dead_entry == other.dead_entry
            and self.meta_entry == other.meta_entry
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.live_entry is not None:
            out.append(f"live_entry={self.live_entry}")
        if self.dead_entry is not None:
            out.append(f"dead_entry={self.dead_entry}")
        if self.meta_entry is not None:
            out.append(f"meta_entry={self.meta_entry}")
        return f"<BucketEntry [{', '.join(out)}]>"
