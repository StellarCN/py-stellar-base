# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .bucket_metadata_ext import BucketMetadataExt
from .uint32 import Uint32

__all__ = ["BucketMetadata"]


class BucketMetadata:
    """
    XDR Source Code::

        struct BucketMetadata
        {
            // Indicates the protocol version used to create / merge this bucket.
            uint32 ledgerVersion;

            // reserved for future use
            union switch (int v)
            {
            case 0:
                void;
            case 1:
                BucketListType bucketListType;
            }
            ext;
        };
    """

    def __init__(
        self,
        ledger_version: Uint32,
        ext: BucketMetadataExt,
    ) -> None:
        self.ledger_version = ledger_version
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BucketMetadata:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ledger_version = Uint32.unpack(unpacker, depth_limit - 1)
        ext = BucketMetadataExt.unpack(unpacker, depth_limit - 1)
        return cls(
            ledger_version=ledger_version,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BucketMetadata:
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
    def from_xdr(cls, xdr: str) -> BucketMetadata:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BucketMetadata:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ledger_version": self.ledger_version.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> BucketMetadata:
        ledger_version = Uint32.from_json_dict(json_dict["ledger_version"])
        ext = BucketMetadataExt.from_json_dict(json_dict["ext"])
        return cls(
            ledger_version=ledger_version,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.ledger_version,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_version == other.ledger_version and self.ext == other.ext

    def __repr__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"ext={self.ext}",
        ]
        return f"<BucketMetadata [{', '.join(out)}]>"
