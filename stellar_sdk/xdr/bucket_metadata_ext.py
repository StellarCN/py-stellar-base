# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
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
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BucketMetadataExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            bucket_list_type = BucketListType.unpack(unpacker)
            return cls(v=v, bucket_list_type=bucket_list_type)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BucketMetadataExt:
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
    def from_xdr(cls, xdr: str) -> BucketMetadataExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BucketMetadataExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        if self.v == 1:
            assert self.bucket_list_type is not None
            return {"v1": self.bucket_list_type.to_json_dict()}
        raise ValueError(f"Unknown v in BucketMetadataExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> BucketMetadataExt:
        if isinstance(json_value, str):
            if json_value not in ("v0",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for BucketMetadataExt, must be one of: v0"
                )
            v = int(json_value[1:])
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for BucketMetadataExt, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v1":
            bucket_list_type = BucketListType.from_json_dict(json_value["v1"])
            return cls(v=v, bucket_list_type=bucket_list_type)
        raise ValueError(f"Unknown key '{key}' for BucketMetadataExt")

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
        if self.bucket_list_type is not None:
            out.append(f"bucket_list_type={self.bucket_list_type}")
        return f"<BucketMetadataExt [{', '.join(out)}]>"
