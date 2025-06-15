# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .bucket_list_type import BucketListType

__all__ = ["BucketMetadataExt"]


class BucketMetadataExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                BucketListType bucketListType;
            }
    """

    def __init__(
        self,
        v: int,
        bucket_list_type: Optional[BucketListType] = None,
    ) -> None:
        self.v = v
        self.bucket_list_type = bucket_list_type

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.bucket_list_type is None:
                raise ValueError("bucket_list_type should not be None.")
            self.bucket_list_type.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> BucketMetadataExt:
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            bucket_list_type = BucketListType.unpack(unpacker)
            return cls(v=v, bucket_list_type=bucket_list_type)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BucketMetadataExt:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> BucketMetadataExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.bucket_list_type,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.bucket_list_type == other.bucket_list_type

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        (
            out.append(f"bucket_list_type={self.bucket_list_type}")
            if self.bucket_list_type is not None
            else None
        )
        return f"<BucketMetadataExt [{', '.join(out)}]>"
