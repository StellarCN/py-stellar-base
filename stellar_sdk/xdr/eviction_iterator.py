# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Boolean
from .uint32 import Uint32
from .uint64 import Uint64

__all__ = ["EvictionIterator"]


class EvictionIterator:
    """
    XDR Source Code::

        struct EvictionIterator {
            uint32 bucketListLevel;
            bool isCurrBucket;
            uint64 bucketFileOffset;
        };
    """

    def __init__(
        self,
        bucket_list_level: Uint32,
        is_curr_bucket: bool,
        bucket_file_offset: Uint64,
    ) -> None:
        self.bucket_list_level = bucket_list_level
        self.is_curr_bucket = is_curr_bucket
        self.bucket_file_offset = bucket_file_offset

    def pack(self, packer: Packer) -> None:
        self.bucket_list_level.pack(packer)
        Boolean(self.is_curr_bucket).pack(packer)
        self.bucket_file_offset.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> EvictionIterator:
        bucket_list_level = Uint32.unpack(unpacker)
        is_curr_bucket = Boolean.unpack(unpacker)
        bucket_file_offset = Uint64.unpack(unpacker)
        return cls(
            bucket_list_level=bucket_list_level,
            is_curr_bucket=is_curr_bucket,
            bucket_file_offset=bucket_file_offset,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> EvictionIterator:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> EvictionIterator:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.bucket_list_level,
                self.is_curr_bucket,
                self.bucket_file_offset,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.bucket_list_level == other.bucket_list_level
            and self.is_curr_bucket == other.is_curr_bucket
            and self.bucket_file_offset == other.bucket_file_offset
        )

    def __repr__(self):
        out = [
            f"bucket_list_level={self.bucket_list_level}",
            f"is_curr_bucket={self.is_curr_bucket}",
            f"bucket_file_offset={self.bucket_file_offset}",
        ]
        return f"<EvictionIterator [{', '.join(out)}]>"
